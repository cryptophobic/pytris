import pygame
from dataclasses import dataclass


@dataclass
class Controls:
    rotate_left: int
    move_left: int
    move_right: int
    move_down: int


wasd = Controls(rotate_left=pygame.K_w, move_left=pygame.K_a, move_right=pygame.K_d, move_down=pygame.K_s)
uldr = Controls(rotate_left=pygame.K_UP, move_left=pygame.K_LEFT, move_right=pygame.K_RIGHT, move_down=pygame.K_DOWN)
