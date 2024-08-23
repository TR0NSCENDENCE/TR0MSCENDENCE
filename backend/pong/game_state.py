import asyncio
import json
from asgiref.sync import async_to_sync, sync_to_async
from users.models import User
from autobahn.exception import Disconnected
from random import random

from .models import GameInstance
from enum import Enum

from .game_defaults import DEFAULTS

import math

CLOSE_CODE_ERROR = 3000
CLOSE_CODE_OK = 3001

TICK_RATE = 75

OPTIMIZATION = {
    'disable_paddle': False
}

Direction = Enum('Direction', ['NONE', 'LEFT', 'RIGHT'])
Side = Enum('Side', ['ONE', 'TWO'])

class AlreadyConnected(Exception):
    pass

class Player():
    # Attributes
    #   connected: Boolean
    #   consumer: GameConsumer
    #   user: User
    #   position: (Float, Float)
    #   direction: Direction
    #   score: Int
    def __init__(self, side):
        self.connected = False
        self.consumer = None
        self.user = None
        self.score = 0
        self.side = side
        self.reset()

    def reset(self):
        self.direction = Direction.NONE
        self.velocity = DEFAULTS['paddle']['velocity']
        self.position = DEFAULTS['scene']['paddle_distance']
        if self.side == Side.ONE:
            self.position = -self.position

    def update_position(self):
        def get_offset(direction):
            return                                      \
                 0 if direction == Direction.NONE else  \
                 1 if direction == Direction.RIGHT else \
                -1

        def can_move(position):
            half_pad = DEFAULTS['paddle']['size'] / 2.
            limit = DEFAULTS['scene']['wall_distance'] - half_pad
            return abs(position) <= limit

        (x, y) = self.position
        y += get_offset(self.direction) * self.velocity
        if not can_move(y):
            y = math.copysign(DEFAULTS['paddle']['max_position'], y)
        self.position = (x, y)

    def increase_score(self):
        self.score += 1

    def increase_velocity(self):
        self.velocity *= DEFAULTS['paddle']['speedup_factor']

    def get_score(self):
        return (self.score)

    def get_position(self):
        return (self.position)
    
    def get_direction(self):
        return (self.direction)

    def get_user(self):
        return (self.user)

    def is_connected(self):
        return (self.connected)

    def is_consumer(self, consumer):
        return (self.consumer == consumer)

    def as_json(self):
        return ({
            'position': {
                'x': self.position[0],
                'y': self.position[1]
            }
        })

    def connect(self, user, consumer):
        if self.is_connected():
            raise AlreadyConnected
        self.connected = True
        self.consumer = consumer
        self.user= user

    async def close_consumer(self, close_code):
        await self.consumer.close(close_code)

    def disconnect(self):
        self.connected = False
        self.consumer = None
        self.user= None

    def receive(self, data):
        if data['type'] == 'player_direction':
            def invert(direction):
                return                                                  \
                    Direction.RIGHT if direction == Direction.LEFT else \
                    Direction.LEFT if direction == Direction.RIGHT else \
                    Direction.NONE

            payload = data['payload']
            self.direction =                                                \
                Direction.NONE if payload['right'] and payload['left'] else \
                Direction.RIGHT if payload['right'] else                    \
                Direction.LEFT if payload['left'] else                      \
                Direction.NONE
            if self.side == Side.TWO:
                self.direction = invert(self.direction)

    async def send(self, data):
        await self.consumer.send_json(data)

class GameState():
    # Fields:
    #   finished: Boolean
    #   has_round_ended: Boolean
    #   players: [Player, Player]
    #   ball_pos: (float, float)
    #   ball_vel: (float, float)

    def __init__(self, instance: GameInstance):
        self.instance = instance
        self.finished = False
        self.has_round_ended = False
        self.players = [ Player(Side.ONE), Player(Side.TWO) ]
        self.reset_game_state()

    def player_connect(self, player: User, consumer):
        if self.instance.player_one == player:
            self.players[0].connect(player, consumer)
        if self.instance.player_two == player:
            self.players[1].connect(player, consumer)

    def player_disconnect(self, player: User):
        if self.instance.player_one == player:
            self.players[0].disconnect()
        if self.instance.player_two == player:
            self.players[1].disconnect()

    async def player_receive_json(self, consumer, json_data):
        for player in self.players:
            if player.is_consumer(consumer):
                player.receive(json_data)

    async def players_send_json(self, data):
        try:
            for player in self.players:
                if player.is_connected():
                    await player.send(data)
        except Disconnected:
            pass

    def players_connected(self):
        return all(player.is_connected() for player in self.players)

    def running(self):
        return self.players_connected() and not self.finished

    def instance_ingame(self):
        self.log('In-game !')
        self.instance.state = 'IG'
        self.instance.save()

    def instance_finished(self):
        self.log('Game finished !')
        self.instance.state = 'FD'
        self.instance.save()

    def instance_winner(self, player: User):
        self.log(f'Winner: {player.username}' if player else 'Tie')
        self.instance.winner = player
        self.instance.player_one_score = self.players[0].get_score()
        self.instance.player_two_score = self.players[1].get_score()
        self.instance.save()
        async_to_sync(self.players_send_json)({
            'type': 'winner',
            'winner_id': player.pk if player else -1
        })

    async def close_consumers(self, close_code=None):
        for player in self.players:
            if player.is_connected():
                await player.close_consumer(close_code)

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

    async def update_consumers(self):
        await self.players_send_json({
            'type': 'sync',
            'state': {
                'ball': {
                    'position': {
                        'x': self.ball_pos[0],
                        'y': self.ball_pos[1]
                    },
                    'velocity': {
                        'x': self.ball_vel[0],
                        'y': self.ball_vel[1]
                    }
                },
                'paddle_1': self.players[0].as_json(),
                'paddle_2': self.players[1].as_json()
            }
        })

    async def update_score(self):
        await self.players_send_json({
            'type': 'score',
            'scores': {
                'p1': self.players[0].get_score(),
                'p2': self.players[1].get_score()
            }
        })

    async def counter(self):
        await self.players_send_json({'type': 'counter_start'})
        await asyncio.sleep(3)
        await self.players_send_json({'type': 'counter_stop'})

    def update_ball_pos(self):
        (x, y) = self.ball_pos
        (vx, vy) = self.ball_vel
        x += vx
        y += vy
        self.ball_pos = (x, y)

    def update_paddle_pos(self):
        for player in self.players:
            player.update_position()

    def reset_game_state(self, is_ball_on_p1_side=False):
        angle = DEFAULTS['ball']['reset_angle_bounds']
        angle += random() * DEFAULTS['ball']['reset_angle_range']
        if not is_ball_on_p1_side:
            angle += math.pi
        for player in self.players:
            player.reset()
        self.ball_pos = (0, 0)
        self.ball_speed = DEFAULTS['ball']['velocity']
        self.paddle_velocity = DEFAULTS['paddle']['velocity']
        self.ball_vel = (
            self.ball_speed * math.cos(angle),
            self.ball_speed * math.sin(angle)
        )
        if OPTIMIZATION['disable_paddle']:
            self.next_bounce = 0 if is_ball_on_p1_side else 1

    def round_end(self, loser_id):
        winner_player = self.players[1 - loser_id]
        winner_player.increase_score()
        if winner_player.get_score() == DEFAULTS['game']['win_score']:
            self.winner = winner_player.get_user()
            self.finished = True
        else:
            self.has_round_ended = True

    def handle_paddle_physics(self, id):
        def collides(y, player):
            return abs(player[1] - y) <= (DEFAULTS['paddle']['size'] / 2.)

        (bx, by) = self.ball_pos
        (bvx, bvy) = self.ball_vel

        if OPTIMIZATION['disable_paddle']:
            if id != self.next_bounce:
                return (bx, by, bvx, bvy, False)
            self.next_bounce = (self.next_bounce + 1) % 2

        player = self.players[id].get_position()

        if not collides(by, player):
            return (bx, by, bvx, bvy, True)

        new_position = DEFAULTS['scene']['paddle_distance']
        new_position -= DEFAULTS['ball']['radius']
        bx = math.copysign(new_position, bx)

        angle = math.atan2(DEFAULTS['paddle']['size'] / 2., player[1] - by)
        angle = angle - math.pi / 2.
        if id == 1:
            angle = math.pi - angle

        self.ball_speed *= DEFAULTS['ball']['speedup_factor']
        bvx = math.cos(angle) * self.ball_speed
        bvy = math.sin(angle) * self.ball_speed

        self.players[id].increase_velocity()
        return (bx, by, bvx, bvy, False)

    def handle_physics(self):
        (bx, by) = self.ball_pos
        (bvx, bvy) = self.ball_vel

        # Ball bounce on side walls
        ball_radius = DEFAULTS['ball']['radius']
        bounds = DEFAULTS['scene']['wall_distance'] - ball_radius
        if abs(by) >= bounds:
            # Make ball stay within (-WALL_DIST; WALL_DIST)
            by = math.copysign(2 * bounds - abs(by), by)
            # Change path of ball
            bvy = -bvy
            self.ball_pos = (bx, by)
            self.ball_vel = (bvx, bvy)

        # Ball bounce on paddle or win / lose
        bounds = DEFAULTS['scene']['paddle_distance'] - ball_radius
        if abs(bx) >= bounds:
            ball_on_p1_side = bx < 0
            player_id = 0 if ball_on_p1_side else 1
            result = self.handle_paddle_physics(player_id)
            (bx, by, bvx, bvy, lost) = result
            self.ball_pos = (bx, by)
            self.ball_vel = (bvx, bvy)
            if lost:
                self.round_end(player_id)
                self.reset_game_state(ball_on_p1_side)

    async def logic(self):
        self.update_ball_pos()
        self.update_paddle_pos()
        self.handle_physics()
        await self.update_consumers()
        if self.has_round_ended:
            self.has_round_ended = False
            await self.update_score()
            await self.counter()
        else:
            await asyncio.sleep(1. / TICK_RATE)

    async def game_loop(self):
        await self.wait_for_players()
        await sync_to_async(self.instance_ingame)()
        await self.counter()
        while self.running():
            await self.logic()
        if not self.finished:
            # If the game ended before one of the players won,
            # the winner is:
            #   - The last one connected
            #   - If no one is left, the one with the highest score
            #   - If they also have the same score, it's a tie
            winner_player =                                                                                     \
                self.players[0] if self.players[0].is_connected() else                                          \
                self.players[1] if self.players[1].is_connected() else                                          \
                self.players[0].get_score() if self.players[0].get_score() > self.players[1].get_score() else   \
                self.players[1].get_score() if self.players[1].get_score() > self.players[0].get_score() else   \
                None
            self.winner = winner_player.get_user() if winner_player else None
        await sync_to_async(self.instance_winner)(self.winner)
        await sync_to_async(self.instance_finished)()
        await self.close_consumers(CLOSE_CODE_OK)
