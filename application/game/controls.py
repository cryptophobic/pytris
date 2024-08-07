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

        self.movements_map = Movements(
            rotate_left=rotate_left,
            move_right=move_right,
            move_down=move_down,
            move_left=move_left,
        )

        self.data[rotate_left] = Action(self.rotate_left)
        #self.data[move_up] = self.move_up
        self.data[move_left] = Action(self.move_left, 100)
        self.data[move_down] = Action(self.move_down, 30)
        self.data[move_right] = Action(self.move_right, 100)

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
