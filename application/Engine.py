from application.Events import Events
from application.State import State
from application.Renderer import Renderer
from application.Timer import Timer

import pygame
from pygame.locals import *


class Engine(object):

    fps = 60

    def __init__(self):
        self.eventProcessor = Events()
        self.stateManager = State()
        self.renderer = Renderer()
        self.ticker = Timer()
        self.screen = None
        self.interval = 1000 / Engine.fps

    def finalize(self):
        pygame.quit()

    def initialize(self):
        pygame.init()
        self.screen = pygame.display.set_mode((500, 900), 0, 32)
        pygame.display.set_caption("Hello Tetris")
        self.screen.fill((0, 0, 0))

    def check_exit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_ESCAPE]:
            return True

        return False

    def run(self):
        self.initialize()
        game_over = False

        player1 = (pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d)
        player2 = (pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT)
        self.eventProcessor.subscribe('player1', player1)
        self.eventProcessor.subscribe('player2', player2)

        threshold = self.ticker.last_timestamp + self.interval
        first_timestamp = self.ticker.last_timestamp

        while not game_over:
            self.ticker.tick()
            self.eventProcessor.listen(self.ticker.last_timestamp)
            game_over = self.check_exit()
            events = self.eventProcessor.slice(first_timestamp, self.ticker.last_timestamp)
            first_timestamp = self.ticker.last_timestamp

            if self.ticker.last_timestamp >= threshold:
                threshold += self.interval
                self.renderer.render()

        self.finalize()
