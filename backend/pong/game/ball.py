import math

from random import random

from .player import Player, Side
from .settings import DEFAULTS, OPTIMIZATION

class Ball():

    # Attributes:
    #   speed: Float
    #   position: tuple[Float, Float]
    #   velocity: tuple[Float, Float]
    #   next_bounce: Side

    def __init__(self):
        self.__radius = DEFAULTS['ball']['radius']

    def reset(self, side: Side):
        angle = DEFAULTS['ball']['reset_angle_bounds']
        angle += random() * DEFAULTS['ball']['reset_angle_range']
        if side == Side.TWO:
            angle += math.pi
        self.__speed = DEFAULTS['ball']['velocity']
        self.__position = (0, 0)
        self.__velocity = (math.cos(angle), math.sin(angle))
        if OPTIMIZATION['disable_paddle']:
            self.__side = side

    def update(self, delta, paddles: tuple[Player, Player], on_lose):
        remaining_distance = self.__speed * delta
        while remaining_distance > 0:
            step = min(remaining_distance, 1)
            remaining_distance -= step
            self.__update_position(step)
            self.__wall_collision()
            loser_id = self.__paddle_collision(paddles)
            if loser_id != None:
                on_lose(loser_id)
                remaining_distance = 0

    def as_json(self):
        return ({
            'position': {
                'x': self.__position[0],
                'y': self.__position[1]
            },
            'velocity': {
                'x': self.__velocity[0],
                'y': self.__velocity[1]
            },
            'speed': self.__speed
        })

    def __update_position(self, step):
        (x, y) = self.__position
        (vx, vy) = self.__velocity
        x += vx * step
        y += vy * step
        self.__position = (x, y)

    def __wall_collision(self):
        (bx, by) = self.__position
        (bvx, bvy) = self.__velocity

        bounds = DEFAULTS['scene']['wall_distance'] - self.__radius
        if abs(by) < bounds:
            return
        by = math.copysign(2 * bounds - abs(by), by)
        bvy = -bvy
        self.__position = (bx, by)
        self.__velocity = (bvx, bvy)

    def __paddle_physics(self, paddle: Player):
        def collides(position, paddle):
            delta = abs(paddle[1] - position)
            return (delta <= DEFAULTS['paddle']['size'] / 2.)

        (bx, by) = self.__position
        (bvx, bvy) = self.__velocity

        if OPTIMIZATION['disable_paddle']:
            if paddle.get_side() != self.__side:
                return (bx, by, bvx, bvy, False)
            self.__side = Side.TWO if self.__side == Side.ONE else Side.ONE

        player = paddle.get_position()

        if not collides(by, player):
            return (bx, by, bvx, bvy, True)

        new_position = DEFAULTS['scene']['paddle_distance']
        new_position -= DEFAULTS['ball']['radius']
        bx = math.copysign(new_position, bx)

        angle = math.atan2(DEFAULTS['paddle']['size'] / 2., player[1] - by)
        angle -= math.pi / 2.
        if paddle.get_side() == Side.TWO:
            angle = math.pi - angle

        self.__speed *= DEFAULTS['ball']['speedup_factor']
        bvx = math.cos(angle)
        bvy = math.sin(angle)

        paddle.increase_velocity()
        return (bx, by, bvx, bvy, False)

    def __paddle_collision(self, paddles: tuple[Player, Player]):
        (bx, by) = self.__position
        (bvx, bvy) = self.__velocity

        if abs(bx) < DEFAULTS['scene']['paddle_distance'] - self.__radius:
            return
        player_id = 0 if bx < 0 else 1
        (bx, by, bvx, bvy, lost) = self.__paddle_physics(paddles[player_id])
        self.__position = (bx, by)
        self.__velocity = (bvx, bvy)
        return (player_id if lost else None)
