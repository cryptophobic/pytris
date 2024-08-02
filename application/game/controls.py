import pygame
from collections import UserDict

from application.game.objects.Piece import Piece
from application.game.objects.shapes import *


class MoveControls(UserDict):
    def __init__(self, move_left, move_right, move_down, move_up, rotate_left=0):
        super().__init__()

        #self.data[rotate_left] = self.rotate_left
        self.data[move_up] = self.move_up
        self.data[move_left] = self.move_left
        self.data[move_down] = self.move_down
        self.data[move_right] = self.move_right

    def action(self, key: int, piece: Piece):
        if key in self.data:
            self.data[key](piece)

    def move_left(self, piece: Piece):
        piece.velocity.x -= 10

    def move_right(self, piece: Piece):
        piece.velocity.x += 10

    def move_down(self, piece: Piece):
        piece.velocity.y += 10

    def move_up(self, piece: Piece):
        piece.velocity.y -= 10

    def rotate_left(self, piece: Piece):
        piece.rotate += ROTATE_LEFT

    def rotate_right(self, piece: Piece):
        piece.rotate += ROTATE_RIGHT


wasd = MoveControls(move_up=pygame.K_w, move_left=pygame.K_a, move_right=pygame.K_d, move_down=pygame.K_s)
uldr = MoveControls(move_up=pygame.K_UP, move_left=pygame.K_LEFT, move_right=pygame.K_RIGHT, move_down=pygame.K_DOWN)
