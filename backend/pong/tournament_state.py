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

    def players_connected(self):
        return reduce(lambda a, b: a.connected and b.connected, self.player_connections)

    def running(self):
        return self.players_connected()

    def instance_ingame(self):
        self.log('In-game !')
        self.instance.state = 'IG'
        self.instance.save()

    def instance_finished(self):
        self.log('Game finished !')
        self.instance.state = 'FD'
        self.instance.save()

    def instance_winner(self, player: User):
        self.log('Winner :', player.username)
        self.instance.winner = player
        self.instance.player_one_score = 69
        self.instance.player_two_score = 42
        self.instance.save()
        async_to_sync(self.players_send_json)({'type': 'winner', 'winner_id': player.pk})

    async def close_consumers(self):
        if self.p_one_connected:
            await self.p_one_consumer.close()
        if self.p_two_connected:
            await self.p_two_consumer.close()

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

    async def tournament_loop(self):
        await self.wait_for_players()
        await sync_to_async(self.instance_ingame)()
        self.log("Waiting for player to disconnect")
        while self.running():
            await self.logic()
        await sync_to_async(self.instance_finished)()
        await sync_to_async(self.instance_winner)(self.p_one)
        await self.close_consumers()
