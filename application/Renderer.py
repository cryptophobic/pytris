from typing import List

from application import config
from application.game.Player import Player
import pygame

from application.game.State.Desk import Brick


class Renderer:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(config.SCREEN_SIZE, 0, 32)
        pygame.display.set_caption("Hello Tetris")
        self.screen.fill((0, 0, 0))

    def __del__(self):
        pygame.quit()

    def render(self, objects: List[Player], bricks: List[Brick]):
        if len(objects) == 0:
            return

        self.screen.fill((0, 0, 0))

        for obj in objects:
            for square in obj.body.shape.shape:
                rect = pygame.Rect(
                    ((obj.body.coordinates.x + square[0]) * config.BLOCK_WIDTH) + config.BORDERS_WIDTH,
                    ((obj.body.coordinates.y + square[1]) * config.BLOCK_HEIGHT) + config.BORDERS_HEIGHT,
                    config.BLOCK_WIDTH - config.BORDERS_WIDTH  * 2,
                    config.BLOCK_HEIGHT - config.BORDERS_HEIGHT * 2)
                pygame.draw.rect(self.screen, obj.body.shape.color, rect)

        for brick in bricks:
            rect = pygame.Rect(
                (brick.position.x * config.BLOCK_WIDTH) + config.BORDERS_WIDTH,
                (brick.position.y * config.BLOCK_HEIGHT) + config.BORDERS_HEIGHT,
                config.BLOCK_WIDTH - config.BORDERS_WIDTH  * 2,
                config.BLOCK_HEIGHT - config.BORDERS_HEIGHT * 2)
            pygame.draw.rect(self.screen, brick.color, rect)

        pygame.display.update()
