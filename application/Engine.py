from application.Events import Events
from application.game.Player import Player
from application.game.State.State import State
from application.Renderer import Renderer
from application.Timer import Timer

import pygame

from application.game.controls import wasd, uldr, tfgh


class Engine(object):

    fps = 60

    def __init__(self):
        self.eventProcessor = Events()
        self.stateManager = State()
        self.renderer = Renderer()
        self.ticker = Timer()
        self.game_over = False
        self.interval = 1000 / Engine.fps

    def check_exit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_ESCAPE]:
            self.game_over = True

    def run(self):
        player1 = Player('player1', wasd)
        player2 = Player('player2', uldr)
        player3 = Player('player3', tfgh)
        self.eventProcessor.subscribe(player1.name, player1.controls)
        self.eventProcessor.subscribe(player2.name, player2.controls)
        self.eventProcessor.subscribe(player3.name, player3.controls)

        self.stateManager.register_player(player1)
        self.stateManager.register_player(player2)
        self.stateManager.register_player(player3)

        threshold = self.ticker.last_timestamp + self.interval
        first_timestamp = self.ticker.last_timestamp
        player1.body.color = (100, 150, 0)
        player2.body.color = (150, 100, 0)
        player3.body.color = (0, 100, 150)

        while not self.game_over:
            self.ticker.tick()
            self.check_exit()
            self.eventProcessor.listen(self.ticker.last_timestamp)
            events = self.eventProcessor.slice(first_timestamp, self.ticker.last_timestamp)
            self.stateManager.update_players(events)
            first_timestamp = self.ticker.last_timestamp

            if self.ticker.last_timestamp >= threshold:
                threshold += self.interval
                self.renderer.render([player1.body, player2.body, player3.body])
