import numpy as np

LEFT = 0
RIGHT = 1

_rotation_matrix = {
    LEFT: np.array([[0, 1], [-1, 0]]),
    RIGHT: np.array([[0, -1], [1, 0]]),
}

shapes = np.array([
    [[0, 0], [-1, 1], [-1, 0], [1, 0]],  # ge
    [[0, 0], [-1, 0], [-1, -1], [1, 0]],  # reverted ge
    [[0, 0], [-1, 0], [0, 1], [1, 0]],  # triple
    [[0, 0], [0, 1], [1, 1], [1, 0]],  # square
    [[0, 0], [-1, 0], [-1, -1], [0, 1]],  # twice
    [[0, 0], [-1, 0], [-1, 1], [0, -1]],  # twice reverted
    [[0, 0], [-1, 0], [1, 0], [2, 0]],  # stick
])


def rotate(shape_array, direction=LEFT):
    return np.matmul(shape_array, _rotation_matrix[direction])


def _move(shape_array, times_x, times_y):
    return np.array([[pair[0] + times_x, pair[1] + times_y] for pair in shape_array])


def move_left(shape_array, times=1):
    return _move(shape_array, -times, 0)


def move_right(shape_array, times=1):
    return _move(shape_array, times, 0)


def move_top(shape_array, times=1):
    return _move(shape_array, 0, times)


def move_bottom(shape_array, times=1):
    return _move(shape_array, 0, -times)