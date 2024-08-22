import asyncio
import json
from asgiref.sync import async_to_sync, sync_to_async
from users.models import User
from autobahn.exception import Disconnected
from functools import reduce

from .consummers import TournamentConsumer
from .models import GameInstance, TournamentInstance

class UserConnection():
    class AlreadyConnected(Exception):
        pass

    def __int__(self):
        self.connected = False
        self.consumer = None
        self.user = None
    
    def connect(self, consumer: TournamentConsumer):
        if self.connected:
            raise self.AlreadyConnected
        self.consumer = consumer
        self.user = consumer.user
        self.connected = True

    def disconnect(self):
        self.connected = False
        self.consumer = None

    def send_json(self, json_data):
        if self.connected:
            self.consumer.send_json(json_data)

class TournamentState():

    # Fields:
    #   players: UserConnection


    def __init__(self, instance: GameInstance):
        self.instance = instance
        self.player_connections = [UserConnection() for _ in range(4)]

    def player_connect(self, consumer: TournamentConsumer):
        if self.instance.player_one == consumer.user:
            self.player_connections[0].connect(consumer)
        if self.instance.player_two == consumer.user:
            self.player_connections[1].connect(consumer)
        if self.instance.player_thr == consumer.user:
            self.player_connections[2].connect(consumer)
        if self.instance.player_fou == consumer.user:
            self.player_connections[3].connect(consumer)

    def player_disconnect(self, player: User):
        if self.instance.player_one == player:
            self.player_connections[0].disconnect()
        if self.instance.player_two == player:
            self.player_connections[1].disconnect()
        if self.instance.player_thr == player:
            self.player_connections[2].disconnect()
        if self.instance.player_fou == player:
            self.player_connections[3].disconnect()

    async def player_receive_json(self, consumer, json_data):
        pass

    async def players_send_json(self, data):
        for player_connection in self.player_connections:
            try:
                player_connection.send_json(data)
            except Disconnected:
                pass

    #==========================================================================#
    # Utils
    #==========================================================================#

    def players_connected(self):
        return reduce(lambda a, b: a.connected and b.connected, self.player_connections)

    def running(self):
        return self.players_connected()

    def instance_finished(self):
        self.log('Tournament finished !')
        self.instance.state = 'FD'
        self.instance.save()

    async def close_consumers(self):
        for c in self.player_connections:
            asyncio.create_task(c.consumer.close())
            c.disconnect()

    #==========================================================================#
    # Pure game logic
    #==========================================================================#

    def log(self, *args):
        RED = '\033[0;31m'
        BLUE = '\033[0;34m'
        RESET = '\033[0m'
        message = f'{RED}[{BLUE}GI#{self.instance.uuid}{RED}]{RESET}'
        print(message, *args)

    async def wait_for_players(self):
        self.log("Waiting for player to connect...")
        while not self.players_connected():
            await asyncio.sleep(1. / 10)

    async def logic(self):
        self.log('waiting for player to disconnect...')
        while self.running():
            await asyncio.sleep(1. / 10)

    async def tournament_loop(self):
        await self.wait_for_players()
        await sync_to_async(self.instance_ingame)()
        self.log("Waiting for player to disconnect")
        while self.running():
            await self.logic()
        await sync_to_async(self.instance_finished)()
        await self.close_consumers()
