import copy

import numpy as np

ROTATE_LEFT = -1
ROTATE_RIGHT = 1

_rotation_matrix = {
    ROTATE_LEFT: np.array([[0, 1], [-1, 0]]),
    ROTATE_RIGHT: np.array([[0, -1], [1, 0]]),
}

shapes = np.array([
    [[0, 0], [-1, 1], [-1, 0], [1, 0]],  # ge
    [[0, 0], [-1, 0], [-1, -1], [1, 0]],  # reverted ge
    [[0, 0], [-1, 0], [0, 1], [1, 0]],  # triple
    [[0, 0], [0, 1], [1, 1], [1, 0]],  # square
    [[0, 0], [-1, 0], [-1, -1], [0, 1]],  # twice
    [[0, 0], [-1, 0], [-1, 1], [0, -1]],  # twice reverted
    [[0, -1], [0, 0], [0, 1], [0, 2]],  # stick
])

print(type(shapes[0]))


def rotate(shape_array, times_direction=ROTATE_LEFT):
    res = copy.copy(shape_array)
    times = abs(times_direction)
    direction = ROTATE_LEFT if times_direction <= ROTATE_LEFT else ROTATE_RIGHT
    for _ in range(times):
        res = np.matmul(res, _rotation_matrix[direction])
    return res


def _move(shape_array, times_x, times_y):
    return np.array([[pair[0] + times_x, pair[1] + times_y] for pair in shape_array])


def move_shape_left(shape_array, times=1):
    return _move(shape_array, -times, 0)


def move_shape_right(shape_array, times=1):
    return _move(shape_array, times, 0)


def move_shape_up(shape_array, times=1):
    return _move(shape_array, 0, times)


def move_shape_down(shape_array, times=1):
    return _move(shape_array, 0, -times)
