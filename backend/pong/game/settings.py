from math import atan2, pi

GAME___WIN_SCORE            = 3

SCENE__WALL_DISTANCE        = 19.
SCENE__PADDLE_DISTANCE      = 35.

PADDLE_SIZE                 = 8.
PADDLE_MAX_POSITION         = SCENE__WALL_DISTANCE - PADDLE_SIZE / 2.
PADDLE_VELOCITY             = 37.5
PADDLE_SPEEDUP_FACTOR       = 1.03

BALL___RADIUS               = 1.
BALL___SPEEDUP_FACTOR       = 1.1
BALL___VELOCITY             = 22.5
BALL___RESET_ANGLE_BOUNDS   = atan2(SCENE__PADDLE_DISTANCE, SCENE__WALL_DISTANCE)
BALL___RESET_ANGLE_RANGE    = 2. * BALL___RESET_ANGLE_BOUNDS - pi

DEFAULTS = {
    'game': {
        'win_score': GAME___WIN_SCORE
    },
    'scene': {
        'wall_distance': SCENE__WALL_DISTANCE,
        'paddle_distance': SCENE__PADDLE_DISTANCE
    },
    'paddle': {
        'size': PADDLE_SIZE,
        'max_position': PADDLE_MAX_POSITION,
        'velocity': PADDLE_VELOCITY,
        'speedup_factor': PADDLE_SPEEDUP_FACTOR
    },
    'ball': {
        'radius': BALL___RADIUS,
        'speedup_factor': BALL___SPEEDUP_FACTOR,
        'velocity': BALL___VELOCITY,
        'reset_angle_bounds': BALL___RESET_ANGLE_BOUNDS,
        'reset_angle_range': BALL___RESET_ANGLE_RANGE
    }
}

OPTIMIZATION = {
    'disable_paddle': False
}
