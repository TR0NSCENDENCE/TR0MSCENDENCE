import asyncio
import json
from asgiref.sync import async_to_sync, sync_to_async
from users.models import User
from autobahn.exception import Disconnected
from random import random

from .models import GameInstance

import math

BALL_SPEEDUP_FACTOR = 1.1
BALL_INITIAL_VELOCITY = 0.5

WALL_DIST = 19
PADDLE_DIST = 35
BALL_RADIUS = 1
PADDLE_SIZE = 7
PADDLE_MAX_POS = WALL_DIST - PADDLE_SIZE / 2

BALL_RESET_ANGLE_BOUNDS = math.atan(PADDLE_DIST / WALL_DIST)
BALL_RESET_ANGLE_RANGE = 2 * BALL_RESET_ANGLE_BOUNDS - math.pi

class GameState():
    class AlreadyConnected(Exception):
        pass

    # Fields:
    #   finished: Boolean
    #   has_round_ended: Boolean
    #   p_one_connected: Boolean
    #   p_two_connected: Boolean
    #   p_one_consumer: GameConsumer
    #   p_two_consumer: GameConsumer
    #   p_one_pos: (float, float)
    #   p_two_pos: (float, float)
    #   p_one: User
    #   p_two: User
    #   ball_pos: (float, float)
    #   ball_vel: (float, float)

    def __init__(self, instance: GameInstance):
        self.instance = instance
        self.finished = False
        self.has_round_ended = False

        self.p_one_connected = False
        self.p_one_consumer = None
        self.p_one_score = 0

        self.p_two_connected = False
        self.p_two_consumer = None
        self.p_two_score = 0

        self.reset_game_state()

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
            if json_data['type'] == 'player_move':
                (x, y) = self.p_one_pos
                offset = json_data['payload']['offset']
                y += offset
                if abs(y) + PADDLE_SIZE / 2 > WALL_DIST:
                    tmp = PADDLE_MAX_POS
                    y = math.copysign(tmp, y)
                self.p_one_pos = (x, y)
        if self.p_two_consumer == consumer:
            if json_data['type'] == 'player_move':
                (x, y) = self.p_two_pos
                offset = json_data['payload']['offset']
                y += offset
                if abs(y) + PADDLE_SIZE / 2 > WALL_DIST:
                    tmp = PADDLE_MAX_POS
                    y = math.copysign(tmp, y)
                self.p_two_pos = (x, y)

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
        self.log('Winner :', player.username)
        self.instance.winner = player
        self.instance.player_one_score = self.p_one_score
        self.instance.player_two_score = self.p_two_score
        self.instance.save()
        async_to_sync(self.players_send_json)({
            'type': 'winner',
            'winner_id': player.pk
        })

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

    TICK_RATE = 60

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
                'paddle_1': {
                    'position': {
                        'x': self.p_one_pos[0],
                        'y': self.p_one_pos[1]
                    },
                },
                'paddle_2': {
                    'position': {
                        'x': self.p_two_pos[0],
                        'y': self.p_two_pos[1]
                    },
                }
            }
        })

    async def update_score(self):
        await self.players_send_json({
            'type': 'score',
            'scores': {
                'p1': self.p_one_score,
                'p2': self.p_two_score
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

    def reset_game_state(self, is_ball_on_p1_side=False):
        angle = BALL_RESET_ANGLE_BOUNDS + random() * BALL_RESET_ANGLE_RANGE
        if not is_ball_on_p1_side:
            angle += math.pi
        self.p_one_pos = (-35, 0)
        self.p_two_pos = (35, 0)
        self.ball_pos = (0, 0)
        self.ball_speed = BALL_INITIAL_VELOCITY
        self.ball_vel = (
            self.ball_speed * math.cos(angle),
            self.ball_speed * math.sin(angle)
        )
        self.next_bounce = 1

    def round_end(self, winner: User):
        if winner == self.p_one:
            self.p_one_score = self.p_one_score + 1
        else:
            self.p_two_score = self.p_two_score + 1
        if 3 in [self.p_one_score, self.p_two_score]:
            self.winner = winner
            self.finished = True
            return
        self.has_round_ended = True

    def handle_paddle_physics(self, id):
        assert(id in [1, 2])

        def collides(y, player):
            return abs(player[1] - y) <= (PADDLE_SIZE / 2.)

        (bx, by) = self.ball_pos
        (bvx, bvy) = self.ball_vel

        # if id != self.next_bounce:
        #     return (bx, by, bvx, bvy, False)
        # self.next_bounce = (self.next_bounce % 2) + 1

        player = self.p_one_pos if id == 1 else self.p_two_pos

        if not collides(by, player):
            return (bx, by, bvx, bvy, True)

        bx = math.copysign(PADDLE_DIST - BALL_RADIUS, bx)

        angle = math.atan2(PADDLE_SIZE / 2., player[1] - by)
        angle = angle - math.pi / 2.
        if id == 2:
            angle = math.pi - angle

        self.ball_speed *= BALL_SPEEDUP_FACTOR
        bvx = math.cos(angle) * self.ball_speed
        bvy = math.sin(angle) * self.ball_speed
        return (bx, by, bvx, bvy, False)

    def handle_physics(self):
        (bx, by) = self.ball_pos
        (bvx, bvy) = self.ball_vel

        # Ball bounce on side walls
        if abs(by) >= WALL_DIST - BALL_RADIUS:
            # Make ball stay within (-WALL_DIST; WALL_DIST)
            sign = math.copysign(1, by)
            offset = abs(by) - (WALL_DIST - BALL_RADIUS)
            by = sign * (WALL_DIST - BALL_RADIUS - offset)
            # Change path of ball
            bvy = -bvy
            self.ball_pos = (bx, by)
            self.ball_vel = (bvx, bvy)

        # Ball bounce on paddle or win / lose
        if abs(bx) >= PADDLE_DIST - BALL_RADIUS:
            ball_on_p1_side = bx < 0
            result = self.handle_paddle_physics(1 if ball_on_p1_side else 2)
            (bx, by, bvx, bvy, lost) = result
            self.ball_pos = (bx, by)
            self.ball_vel = (bvx, bvy)
            if lost:
                self.round_end(self.p_two if ball_on_p1_side else self.p_one)
                self.reset_game_state(ball_on_p1_side)

    async def logic(self):
        self.update_ball_pos()
        self.handle_physics()
        await self.update_consumers()
        if self.has_round_ended:
            self.has_round_ended = False
            await self.update_score()
            await self.counter()
        else:
            await asyncio.sleep(1. / self.TICK_RATE)

    async def game_loop(self):
        await self.wait_for_players()
        await sync_to_async(self.instance_ingame)()
        await self.counter()
        while self.running():
            await self.logic()
        await sync_to_async(self.instance_winner)(self.winner)
        await sync_to_async(self.instance_finished)()
        await self.close_consumers()
