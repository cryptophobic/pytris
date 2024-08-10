from typing import Dict, List

from application import config
from application.game.Player import Player
from application.game.State.Desk import Desk
from application.game.State.EventsHandler import EventsHandler
from application.game.State.Gateway import Gateway
from application.game.State.Ground import Ground
from application.game.State.Movement import Movement
from application.game.State.PlayersCollection import PlayersCollection
from application.game.events.Events import KeyPressLog


class State:
    def __init__(self):
        self.players = PlayersCollection()
        self.desk = Desk(self.players, width=config.DESK_WIDTH, height=config.DESK_HEIGHT)
        self.gateway = Gateway(self.desk, self.players)
        self.__events_handler = EventsHandler(self.players)
        self.__movement = Movement(self.desk)
        self.ground = Ground(self.desk)
        self.ready_for_render = False

    def register_player(self, player: Player):
        self.players.add(player)
        self.gateway.enqueue(player)
        self.__events_handler.load_keys_from_player(player)

    def update_state(self, events: Dict[int, List[KeyPressLog]]):
        self.__events_handler.dispatch_events(events)
        self.draw_players()
        return self.ready_for_render

    def draw_players(self):

        while self.gateway.let_player_go() is True:
            self.ready_for_render = True

        for player in self.players.sorted_dirty_players():
            [is_applied, possibly_grounded] = self.__movement.apply(player)
            print(player.body.coordinates)
            if is_applied:
                self.ready_for_render = True

            if possibly_grounded:
                if self.ground.is_grounded(player):
                    self.ground.ground(player)
                    self.desk.astonish_player(player.name)
                    self.gateway.enqueue(player)
