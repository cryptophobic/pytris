from typing import List
from application.game.objects.Piece import Piece
import pygame


class Renderer:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((500, 900), 0, 32)
        pygame.display.set_caption("Hello Tetris")
        self.screen.fill((0, 0, 0))

    def __del__(self):
        pygame.quit()

    def render(self, objects: List[Piece]):
        #color = (255, 255, 255)
        self.screen.fill((0, 0, 0))

        for obj in objects:
            pygame.draw.rect(self.screen, obj.color, pygame.Rect(obj.coordinates.x * 10, obj.coordinates.y * 10, 10, 10))
            pygame.display.flip()
