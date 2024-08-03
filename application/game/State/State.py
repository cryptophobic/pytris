import sys

from application.Events import KeyPressLog
from application.game.Player import Player
from typing import Dict, List, Set

from application.game.State.Desk import Desk
from application.game.State.KeyMap import KeyMap
from application.game.State.PlayersCollection import PlayersCollection
from application.game.objects.Piece import Piece
from application.game.objects.Shape import Shape
from application.game.types import Vec2


class State:
    def __init__(self):
        self.desk = Desk(50, 50)
        self.place = 10
        self.players = PlayersCollection()
        self.key_map = KeyMap()
        self.changed = False
        pass

    def register_player(self, player: Player):
        player.body = Piece(shape=Shape(), velocity=Vec2(x=0, y=0), coordinates=Vec2(x=self.place, y=25), mass=1)
        self.players.add(player)
        self.desk.put_player(player)
        self.key_map.load_keys_from_player(player)

        self.place += 20

    def move_players(self):
        for player in self.players.sorted_dirty_players():
            player.body.coordinates.x += player.body.velocity.x
            player.body.coordinates.y += player.body.velocity.y
            try:
                self.desk.put_player(player)
            except IndexError as e:
                sys.stderr.write(f"move_players, cannot move {str(e)}\n")

            player.body.velocity.y = 0
            player.body.velocity.x = 0

    def update_player(self, player_name: str, key: int, events_log: List[KeyPressLog]):
        print(f"{player_name} ")
        for event in events_log:
            if event.down is not True:
                continue

            player = self.players[player_name]
            player.action(key)
            self.desk.check_on_move(player)

    def update_players(self, events: Dict[int, List[KeyPressLog]]):
        for key, events_log in events.items():
            if len(events_log) == 0:
                continue
            player_names = self.key_map.get(key)
            if player_names is not None:
                for player_name in player_names:
                    self.update_player(player_name, key, events_log)

        self.move_players()


