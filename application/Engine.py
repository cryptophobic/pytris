from application.Events import Events
from application.State import State
from application.Renderer import Renderer
from application.Timer import Timer

import pygame
from pygame.locals import *


class Engine(object):
    def __init__(self):
        self.eventProcessor = Events()
        self.stateManager = State()
        self.renderer = Renderer()
        self.ticker = Timer()
        self.screen = None

    def finalize(self):
        pygame.quit()

    def initialize(self):
        pygame.init()
        self.screen = pygame.display.set_mode((700, 500), 0, 32)
        pygame.display.set_caption("Hello Tetris")
        self.screen.fill((0, 0, 0))

    def run(self):
        self.initialize()
        game_over = False
        count = 0
        pressed_up = False
        while not game_over:
            self.ticker.tick()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True

            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_ESCAPE]:
                game_over = True

            if pressed_up and not pressed[pygame.K_UP]:
                print("KeyUp")

            if not pressed_up and pressed[pygame.K_UP]:
                print("KeyDown")

            pressed_up = pressed[pygame.K_UP]

        self.finalize()
