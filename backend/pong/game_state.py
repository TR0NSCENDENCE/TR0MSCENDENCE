import asyncio
import json
from users.models import User

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
        if self.instance.player_two == player:
            if self.p_two_connected:
                raise self.AlreadyConnected
            self.p_two_connected = True
            self.p_two_consumer = consumer

    def player_disconnect(self, player: User):
        if self.instance.player_one == player:
            self.p_one_connected = False
        if self.instance.player_two == player:
            self.p_two_connected = False

    async def player_receive_json(self, consumer, json_data):
        if self.p_one_consumer == consumer:
            print('p one data :', json_data)
        if self.p_two_consumer == consumer:
            print('p two data :', json_data)

    async def players_send_json(self, data):
        if self.p_one_connected:
            await self.p_one_consumer.send_json(data)
        if self.p_two_connected:
            await self.p_two_consumer.send_json(data)

    def players_connected(self):
        return self.p_one_connected and self.p_two_connected

    def running(self):
        return self.players_connected()

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
        while not self.players_connected():
            self.log("Waiting for player to connect...")
            await asyncio.sleep(3.)

    async def logic(self):
        while self.running():
            self.log("Waiting for player to disconnect")
            await self.players_send_json({'type': 'update-position'})
            await asyncio.sleep(3.)

    async def game_loop(self):
        self.log('Starting')
        await self.wait_for_players()
        self.log('All player connected')
        await self.logic()
        self.log('One player disconnected')
        await self.close_consumers()
