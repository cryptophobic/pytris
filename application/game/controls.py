import pygame
from collections import UserDict


class MoveControls(UserDict):
    def __init__(self, rotate_left, move_left, move_right, move_down):
        super().__init__()
        self.rotate_left: int = rotate_left
        self.move_left: int = move_left
        self.move_right: int = move_right
        self.move_down: int = move_down
        #self.data[rotate_left] = move_down

    def keys(self) -> tuple:
        return self.move_left, self.move_right, self.move_down, self.rotate_left


wasd = MoveControls(rotate_left=pygame.K_w, move_left=pygame.K_a, move_right=pygame.K_d, move_down=pygame.K_s)
uldr = MoveControls(rotate_left=pygame.K_UP, move_left=pygame.K_LEFT, move_right=pygame.K_RIGHT, move_down=pygame.K_DOWN)
