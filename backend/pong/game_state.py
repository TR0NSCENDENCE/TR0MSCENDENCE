import asyncio
import json
from asgiref.sync import async_to_sync, sync_to_async
from users.models import User
from autobahn.exception import Disconnected

from .models import GameInstance

class GameState():
    class AlreadyConnected(Exception):
        pass

    # Fields:
    # p_one_connected: Boolean
    # p_two_connected: Boolean
    # p_one_consumer: GameConsumer
    # p_two_consumer: GameConsumer

    def __init__(self, instance: GameInstance):
        self.instance = instance
        self.p_one_connected = False
        self.p_two_connected = False
        self.p_one_consumer = None
        self.p_two_consumer = None

    def player_connect(self, player: User, consumer):
        if self.instance.player_one == player:
            if self.p_one_connected:
                raise self.AlreadyConnected
            self.p_one_connected = True
            self.p_one_consumer = consumer
            self.p_one = player
        if self.instance.player_two == player:
            if self.p_two_connected:
                raise self.AlreadyConnected
            self.p_two_connected = True
            self.p_two_consumer = consumer
            self.p_two = player

    def player_disconnect(self, player: User):
        if self.instance.player_one == player:
            self.p_one_connected = False
        if self.instance.player_two == player:
            self.p_two_connected = False

    async def player_receive_json(self, consumer, json_data):
        if self.p_one_consumer == consumer:
            self.log('p one data :', json_data)
        if self.p_two_consumer == consumer:
            self.log('p two data :', json_data)

    async def players_send_json(self, data):
        try:
            if self.p_one_connected:
                await self.p_one_consumer.send_json(data)
            if self.p_two_connected:
                await self.p_two_consumer.send_json(data)
        except Disconnected:
            pass

    def players_connected(self):
        return self.p_one_connected and self.p_two_connected

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

    tick_rate = 150

    async def logic(self):
        self.log("Waiting for player to disconnect")
        while self.running():
            await self.players_send_json({'type': 'update-position'})
            await asyncio.sleep(1. / self.tick_rate)

    async def game_loop(self):
        await self.wait_for_players()
        await sync_to_async(self.instance_ingame)()
        await self.logic()
        await sync_to_async(self.instance_finished)()
        await sync_to_async(self.instance_winner)(self.p_one)
        await self.close_consumers()
