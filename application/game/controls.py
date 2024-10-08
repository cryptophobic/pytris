from dataclasses import dataclass
from enum import Enum
from typing import Callable

import pygame
from collections import UserDict

from application.game.objects.Piece import Piece
from application.game.objects.shapes import *


@dataclass
class Movements:
    rotate_left: int = 0
    rotate_right: int = 0
    move_right: int = 0
    move_left: int = 0
    move_down: int = 0


@dataclass
class Action:
    function: Callable[[Piece], None]
    repeat_delta: int = -1

    def __call__(self, piece: Piece):
        self.function(piece)


class MoveControls(UserDict):

    def __init__(self, move_left, move_right, move_down, rotate_left):
        super().__init__()
        self.gamepad_data = {}

        self.data[rotate_left] = Action(self.rotate_left, 200)
        self.data[move_left] = Action(self.move_left, 150)
        self.data[move_down] = Action(self.move_down, 10)
        self.data[move_right] = Action(self.move_right, 150)

        # alternative
        self.movements_map = Movements(
            rotate_left=rotate_left + 1000,
            move_right=move_right + 1000,
            move_down=move_down + 1000,
            move_left=move_left + 1000,
        )
        self.data[self.movements_map.rotate_left] = Action(self.rotate_left)
        self.data[self.movements_map.move_left] = Action(self.move_left)
        self.data[self.movements_map.move_down] = Action(self.move_down)
        self.data[self.movements_map.move_right] = Action(self.move_right)

    def add_gamepad_mapping(self, move_left, move_right, move_down, rotate_left, rotate_right):
        self.data[2011] = Action(self.rotate_left, 200)
        self.data[rotate_left + 2000] = Action(self.rotate_left, 200)
        self.data[rotate_right + 2000] = Action(self.rotate_right, 200)
        self.data[move_left + 2000] = Action(self.move_left, 150)
        self.data[move_right + 2000] = Action(self.move_right, 150)
        self.data[move_down + 2000] = Action(self.move_down, 10)

    def action(self, key: int, piece: Piece):
        if key in self.data:
            self.data[key](piece)

    def move_left(self, piece: Piece):
        piece.velocity.x -= 1

    def move_right(self, piece: Piece):
        piece.velocity.x += 1

    def move_down(self, piece: Piece):
        piece.velocity.y += 1

    def move_up(self, piece: Piece):
        piece.velocity.y -= 1

    def rotate_left(self, piece: Piece):
        piece.rotate += ROTATE_LEFT

    def rotate_right(self, piece: Piece):
        piece.rotate += ROTATE_RIGHT


wasd = MoveControls(rotate_left=pygame.K_w, move_left=pygame.K_a, move_right=pygame.K_d, move_down=pygame.K_s)
uldr = MoveControls(rotate_left=pygame.K_UP, move_left=pygame.K_LEFT, move_right=pygame.K_RIGHT, move_down=pygame.K_DOWN)
tfgh = MoveControls(rotate_left=pygame.K_t, move_left=pygame.K_f, move_right=pygame.K_h, move_down=pygame.K_g)

uldr.add_gamepad_mapping(move_left=13, move_right=14, move_down=12, rotate_left=2, rotate_right=1)
