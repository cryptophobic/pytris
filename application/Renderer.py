from typing import List

from application.game.Player import Player
from application.game.objects.Piece import Piece
import pygame


class Renderer:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1000, 1000), 0, 32)
        pygame.display.set_caption("Hello Tetris")
        self.screen.fill((0, 0, 0))

    def __del__(self):
        pygame.quit()

    def render(self, objects: List[Player]):
        if len(objects) == 0:
            return

        self.screen.fill((0, 0, 0))

        for obj in objects:
            for square in obj.body.shape.shape:
                rect = pygame.Rect((obj.body.coordinates.x + square[0]) * 20, (obj.body.coordinates.y + square[1]) * 20, 20, 20)
                pygame.draw.rect(self.screen, obj.body.color, rect)
            obj.ready_for_render = False

        pygame.display.update()
