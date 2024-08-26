import math

from enum import Enum

from .settings import DEFAULTS

Direction = Enum('Direction', ['NONE', 'LEFT', 'RIGHT'])
Side = Enum('Side', ['ONE', 'TWO'])

class Player():
    class AlreadyConnected(Exception):
        pass

    # Attributes
    #   connected: Boolean
    #   consumer: GameConsumer
    #   user: User
    #   position: tuple[Float, Float]
    #   direction: Direction
    #   score: Int

    def __init__(self, side: Side):
        self.__connected = False
        self.__consumer = None
        self.__user = None
        self.__score = 0
        self.__side = side
        self.reset()

    def reset(self):
        self.__direction = Direction.NONE
        self.__velocity = DEFAULTS['paddle']['velocity']
        position = DEFAULTS['scene']['paddle_distance']
        if self.__side == Side.ONE:
            position = -position
        self.__position = (position, 0)

    def update_position(self, delta):
        def get_offset(direction):
            return                                      \
                 0 if direction == Direction.NONE else  \
                 1 if direction == Direction.RIGHT else \
                -1

        def can_move(position):
            half_pad = DEFAULTS['paddle']['size'] / 2.
            limit = DEFAULTS['scene']['wall_distance'] - half_pad
            return abs(position) <= limit

        (x, y) = self.__position
        y += get_offset(self.__direction) * self.__velocity * delta
        if not can_move(y):
            y = math.copysign(DEFAULTS['paddle']['max_position'], y)
        self.__position = (x, y)

    def increase_score(self):
        self.__score += 1

    def increase_velocity(self):
        self.__velocity *= DEFAULTS['paddle']['speedup_factor']

    def get_score(self):
        return (self.__score)

    def get_position(self):
        return (self.__position)
    
    def get_direction(self):
        return (self.__direction)

    def get_side(self):
        return (self.__side)

    def get_user(self):
        return (self.__user)

    def is_connected(self):
        return (self.__connected)

    def is_consumer(self, consumer):
        return (self.__consumer == consumer)

    def as_json(self):
        return ({
            'position': {
                'x': self.__position[0],
                'y': self.__position[1]
            },
            'speed': self.__velocity
        })

    def connect(self, user, consumer):
        if self.is_connected():
            raise self.__AlreadyConnected
        self.__connected = True
        self.__consumer = consumer
        self.__user= user

    async def close_consumer(self, close_code):
        await self.__consumer.close(close_code)

    def disconnect(self):
        self.__connected = False
        self.__consumer = None
        self.__user= None

    def receive(self, data):
        if data['type'] == 'player_direction':
            def invert(direction):
                return                                                  \
                    Direction.RIGHT if direction == Direction.LEFT else \
                    Direction.LEFT if direction == Direction.RIGHT else \
                    Direction.NONE

            payload = data['payload']
            self.__direction =                                              \
                Direction.NONE if payload['right'] and payload['left'] else \
                Direction.RIGHT if payload['right'] else                    \
                Direction.LEFT if payload['left'] else                      \
                Direction.NONE
            if self.__side == Side.TWO:
                self.__direction = invert(self.__direction)

    async def send(self, data):
        await self.__consumer.send_json(data)
