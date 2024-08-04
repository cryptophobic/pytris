from typing import List

from application.game.events.Events import Events
from application.game.Player import Player
from application.game.State.State import State
from application.Renderer import Renderer
from application.Timer import Timer

import pygame

from application.game.controls import wasd, uldr, tfgh


class Engine(object):

    fps = 60
    initial_speed_of_falling_down = 1000

    def __init__(self):
        self.eventProcessor = Events()
        self.stateManager = State()
        self.renderer = Renderer()
        self.ticker = Timer()
        self.game_over = False
        self.interval = 1000 / Engine.fps
        self.down_interval = Engine.initial_speed_of_falling_down

    def init_players(self) -> List[Player]:
        player1 = Player(name='player1', controls=wasd, speed=1.5)
        player2 = Player(name='player2', controls=uldr, speed=2.1)
        player3 = Player(name='player3', controls=tfgh, speed=1.8)
        self.eventProcessor.subscribe(player1.name, player1.controls)
        self.eventProcessor.subscribe(player2.name, player2.controls)
        self.eventProcessor.subscribe(player3.name, player3.controls)

        self.stateManager.register_player(player1)
        self.stateManager.register_player(player2)
        self.stateManager.register_player(player3)

        player1.body.color = (100, 150, 0)
        player2.body.color = (150, 100, 0)
        player3.body.color = (0, 100, 150)

        down_threshold = self.ticker.last_timestamp + self.down_interval

        for player in [player1, player2, player3]:
            self.eventProcessor.scheduler.schedule_key_pressed(
                down_threshold,
                player.controls.movements_map.move_down,
                self.down_interval // player.speed)

        return [player1, player2, player3]

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
                    self.renderer.render(players)
                    self.stateManager.ready_for_render = False
