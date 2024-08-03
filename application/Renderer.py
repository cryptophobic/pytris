from typing import List
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

    def render(self, objects: List[Piece]):
        #color = (255, 255, 255)
        self.screen.fill((0, 0, 0))

        for obj in objects:
            for square in obj.shape.shape:
                rect = pygame.Rect((obj.coordinates.x + square[0]) * 20, (obj.coordinates.y + square[1]) * 20, 20, 20)
                pygame.draw.rect(self.screen, obj.color, rect)
            pygame.display.update()

            #pygame.display.flip()
