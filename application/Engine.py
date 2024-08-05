from typing import List

from application import config
from application.game.events.Events import Events
from application.game.Player import Player
from application.game.State.State import State
from application.Renderer import Renderer
from application.Timer import Timer

import pygame


class Engine(object):

    def __init__(self):
        self.eventProcessor = Events()
        self.stateManager = State()
        self.renderer = Renderer()
        self.ticker = Timer()
        self.game_over = False
        self.interval = 1000 / config.FPS
        self.down_interval = config.INITIAL_SPEED_OF_FALLING_DOWN

    def init_players(self) -> List[Player]:
        players = config.players
        for player in players:
            self.eventProcessor.subscribe(player.name, player.controls)
            self.stateManager.register_player(player)

        return players

    def check_exit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_ESCAPE]:
            self.game_over = True

    def run(self):

        players = self.init_players()

        render_threshold = self.ticker.last_timestamp + self.interval
        first_timestamp = self.ticker.last_timestamp

        while not self.game_over:
            self.ticker.tick()
            self.check_exit()
            self.eventProcessor.listen(self.ticker.last_timestamp)

            if self.ticker.last_timestamp >= render_threshold:
                render_threshold += self.interval
                events = self.eventProcessor.slice(first_timestamp, render_threshold)
                self.stateManager.update_players(events)
                first_timestamp = self.ticker.last_timestamp
                if self.stateManager.ready_for_render is True:
                    self.renderer.render(players, self.stateManager.desk.bricks)
                    self.stateManager.ready_for_render = False
