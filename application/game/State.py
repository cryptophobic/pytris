from application.Events import KeyPressLog
from application.game.Player import Player
from typing import Dict, List, Set

from application.game.objects.Piece import Piece
from application.game.objects.Shape import Shape
from application.game.objects.types import Vec2


class State:
    def __init__(self):

        self.place = 0

        self.players: Dict[str, Player] = {}
        self.key_map: Dict[int, Set[str]] = {}
        pass

    def register_player(self, player: Player):
        self.players[player.name] = player
        player.body = Piece(shape=Shape(), coordinates=Vec2(x=self.place, y=0))
        self.place += 40
        for key in player.controls.keys():
            self.key_map[key].update(player.name)

    def update_player(self, player_name: str, events_log: List[KeyPressLog]):
        pass

    def update_players(self, events: Dict[int, List[KeyPressLog]]):
        for key, events_log in events.items():
            player_names = self.key_map.get(key)
            if player_names is not None:
                for player_name in player_names:
                    self.update_player(player_name, events_log)


