import asyncio
import json
import math
import time

from asgiref.sync import async_to_sync, sync_to_async
from users.models import User
from autobahn.exception import Disconnected
from random import random

from ..models import GameInstance
from .settings import DEFAULTS
from .player import Player, Side
from .ball import Ball

CLOSE_CODE_ERROR = 3000
CLOSE_CODE_OK = 3001

TICK_RATE = 75
PULLING_RATE = 10

class Timer:
    def __init__(self):
        self.__start = None

    def start(self):
        self.__start = time.perf_counter()

    def get_elapsed_time(self):
        now = time.perf_counter()
        elapsed_time = now - self.__start
        self.__start = now
        return (elapsed_time)

class GameState():

    # Attributes:
    #   instance: GameInstance
    #   finished: Boolean
    #   has_round_ended: Boolean
    #   players: tuple[Player, Player]
    #   ball: Ball

    def __init__(self, instance: GameInstance):
        self.__instance = instance
        self.__finished = False
        self.__has_round_ended = True
        self.__players = [ Player(Side.ONE), Player(Side.TWO) ]
        self.__ball = Ball()
        self.__loser_id = 1

    def player_connect(self, player: User, consumer):
        if self.__instance.player_one == player:
            self.__players[0].connect(player, consumer)
        if self.__instance.player_two == player:
            self.__players[1].connect(player, consumer)

    def player_disconnect(self, player: User):
        if self.__instance.player_one == player:
            self.__players[0].disconnect()
        if self.__instance.player_two == player:
            self.__players[1].disconnect()

    async def player_receive_json(self, consumer, json_data):
        for player in self.__players:
            if player.is_consumer(consumer):
                player.receive(json_data)

    async def __players_send_json(self, data):
        try:
            for player in self.__players:
                if player.is_connected():
                    await player.send(data)
        except Disconnected:
            pass

    def __players_connected(self):
        return all(player.is_connected() for player in self.__players)

    def __running(self):
        return self.__players_connected() and not self.__finished

    def __instance_ingame(self):
        self.__log('In-game !')
        self.__instance.state = 'IG'
        self.__instance.save()

    def __instance_finished(self):
        self.__log('Game finished !')
        self.__instance.state = 'FD'
        self.__instance.save()

    def __instance_winner(self, player: User):
        self.__log(f'Winner: {player.username}' if player else 'Tie')
        self.__instance.winner = player
        self.__instance.player_one_score = self.__players[0].get_score()
        self.__instance.player_two_score = self.__players[1].get_score()
        self.__instance.save()
        async_to_sync(self.__players_send_json)({
            'type': 'winner',
            'winner_id': player.pk if player else -1
        })

    async def __close_consumers(self, close_code=None):
        for player in self.__players:
            if player.is_connected():
                await player.close_consumer(close_code)

    #==========================================================================#
    # Pure game logic
    #==========================================================================#

    def __log(self, *args):
        RED = '\033[0;31m'
        BLUE = '\033[0;34m'
        RESET = '\033[0m'
        message = f'{RED}[{BLUE}GI#{self.__instance.uuid}{RED}]{RESET}'
        print(message, *args)

    async def __wait_for_players(self):
        self.__log("Waiting for player to connect...")
        while not self.__players_connected():
            await asyncio.sleep(1. / PULLING_RATE)

    async def __update_consumers(self):
        await self.__players_send_json({
            'type': 'sync',
            'state': {
                'ball': self.__ball.as_json(),
                'paddles': [self.__players[0].as_json(), self.__players[1].as_json()]
            }
        })

    async def __update_score(self):
        await self.__players_send_json({
            'type': 'score',
            'scores': {
                'p1': self.__players[0].get_score(),
                'p2': self.__players[1].get_score()
            }
        })

    async def __counter(self):
        SECONDS_TO_WAIT = 3
        PULL_RATE = 20

        await self.__players_send_json({'type': 'counter_start'})
        for _ in range(PULL_RATE):
            await asyncio.sleep(SECONDS_TO_WAIT / PULL_RATE)
        await self.__players_send_json({'type': 'counter_stop'})

    def __reset_game_state(self):
        for player in self.__players:
            player.reset()
        self.__ball.reset((Side.ONE, Side.TWO)[self.__loser_id])

    def __round_end(self, loser_id):
        self.__loser_id = loser_id
        winner_player = self.__players[1 - loser_id]
        winner_player.increase_score()
        if winner_player.get_score() == DEFAULTS['game']['win_score']:
            self.__finished = True
        else:
            self.__has_round_ended = True

    def __handle_physics(self, delta):
        for player in self.__players:
            player.update_position(delta)
        self.__ball.update(delta, self.__players, self.__round_end)

    def __set_winner(self):
        # If the game ended before one of the players won,
        # the winner is:
        #   - The player who's score is 3
        #   - If none has a score of 3, the last one connected
        #   - If no one is left, the one with the highest score
        #   - If they also have the same score, it's a tie
        score_delta = self.__players[0].get_score() - self.__players[1].get_score()
        winner_player =                                                     \
            self.__players[0] if self.__players[0].get_score() == 3 else    \
            self.__players[1] if self.__players[1].get_score() == 3 else    \
            self.__players[0] if self.__players[0].is_connected() else      \
            self.__players[1] if self.__players[1].is_connected() else      \
            self.__players[0] if score_delta > 0 else                       \
            self.__players[1] if score_delta < 0 else                       \
            None
        self.__winner = winner_player.get_user() if winner_player else None

    async def __game_loop(self):
        SIMULATION_STEP = 1. / TICK_RATE

        timer = Timer()
        timer.start()

        while self.__running():
            if self.__has_round_ended:
                self.__has_round_ended = False
                self.__reset_game_state()
                await self.__update_consumers()
                await self.__update_score()
                await self.__counter()
                timer.get_elapsed_time()
            await self.__update_consumers()
            delta = timer.get_elapsed_time()
            self.__handle_physics(delta)
            await asyncio.sleep(SIMULATION_STEP)

    async def game_loop(self):
        await self.__wait_for_players()
        await sync_to_async(self.__instance_ingame)()
        await self.__game_loop()
        self.__set_winner()
        await sync_to_async(self.__instance_winner)(self.__winner)
        await sync_to_async(self.__instance_finished)()
        # await self.__close_consumers(CLOSE_CODE_OK) DO NOT UNCOMMENT
