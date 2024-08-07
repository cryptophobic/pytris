import copy

import numpy as np

ROTATE_LEFT = -1
ROTATE_RIGHT = 1

_rotation_matrix = {
    ROTATE_LEFT: np.array([[0, 1], [-1, 0]]),
    ROTATE_RIGHT: np.array([[0, -1], [1, 0]]),
}


shapes = np.array([
    [[-1, -1], [0, -1], [0, 0], [0, 1]],  # ge
    [[0, -1], [1, -1], [0, 0], [0, 1]],  # reverted ge
    [[0, 0], [-1, 0], [0, 1], [0, -1]],  # triple
    [[0, 0], [0, 1], [1, 1], [1, 0]],  # square
    [[0, 0], [-1, 0], [-1, -1], [0, 1]],  # twice
    [[0, 0], [-1, 0], [-1, 1], [0, -1]],  # twice reverted
    [[0, -1], [0, 0], [0, 1], [0, -2]],  # stick
])

borders = [
    np.array([[-1, -2], [0, -2], [-2, -1], [1, -1], [-1, 0], [1, 0], [-1, 1], [1, 1], [0, 2]]),  # ge
    np.array([[-1, -1], [0, -2], [2, -1], [1, -2], [1, 0], [-1, 0], [1, 1], [-1, 1], [0, 2]]),  # reverted ge
    np.array([[1, 0], [-2, 0], [-1, 1], [-1, -1], [1, 1], [0, 2], [1, -1], [0, -2]]),  # triple
    np.array([[0, -1], [1, -1], [-1, 0], [2, 0], [-1, 1], [2, 1], [0, 2], [1, 2]]),  # square
    np.array([[-1, -2], [-2, -1], [0, -1], [-2, 0], [1, 0], [-1, 1], [1, 1], [0, 2]]),  # twice
    np.array([[0, -2], [-1, -1], [1, -1], [-2, 0], [1, 0], [-2, 1], [0, 1], [-1, 2]]),  # twice reverted
    np.array([[0, -3], [-1, -2], [1, -2], [-1, -1], [1, -1], [-1, 0], [1, 0], [-1, 1], [1, 1], [0, 2]]),  # stick
]


def rotate(shape_array, times_direction=ROTATE_LEFT):
    res = copy.copy(shape_array)
    times = abs(times_direction)
    direction = ROTATE_LEFT if times_direction <= ROTATE_LEFT else ROTATE_RIGHT
    for _ in range(times):
        res = np.matmul(res, _rotation_matrix[direction])
    return res

