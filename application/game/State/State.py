import sys

from application.Events import KeyPressLog
from application.game.Player import Player
from typing import Dict, List, Set

from application.game.State.Desk import Desk
from application.game.State.KeyMap import KeyMap
from application.game.State.PlayersCollection import PlayersCollection
from application.game.objects import shapes
from application.game.objects.Piece import Piece
from application.game.objects.Shape import Shape
from application.game.types import Vec2


class State:
    def __init__(self):
        self.ready_for_render = True
        self.desk = Desk(50, 20)
        self.place = 3
        self.players = PlayersCollection()
        self.key_map = KeyMap()
        self.changed = False
        pass

    def register_player(self, player: Player):
        player.body = Piece(shape=Shape(), velocity=Vec2(x=0, y=0), coordinates=Vec2(x=self.place, y=0), mass=1)
        self.players.add(player)
        try:
            self.desk.put_player(player)
        except IndexError as e:
            sys.stderr.write(str(e))

        self.key_map.load_keys_from_player(player)

        self.place += 5

    def draw_players(self):
        for player in self.players.sorted_dirty_players():
            if player.body.is_dirty():
                self.move_player(player)

            if player.body.rotate != 0:
                self.rotate_player(player)

    def rotate_player(self, player: Player):
        player.body.shape.shape = shapes.rotate(player.body.shape.shape, player.body.rotate)
        try:
            self.desk.put_player(player)
            self.ready_for_render = True
        except IndexError as e:
            player.body.shape.shape = shapes.rotate(player.body.shape.shape, -player.body.rotate)

            sys.stderr.write(f"move_players, cannot rotate {str(e)}\n")
        player.body.rotate = 0

    def move_player(self, player: Player):
        player.body.coordinates.x += player.body.velocity.x
        player.body.coordinates.y += player.body.velocity.y
        try:
            self.desk.put_player(player)
            self.ready_for_render = True
        except IndexError as e:
            player.body.coordinates.x -= player.body.velocity.x
            player.body.coordinates.y -= player.body.velocity.y

            sys.stderr.write(f"move_players, cannot move {str(e)}\n")

        player.body.velocity.y = 0
        player.body.velocity.x = 0

    def update_player(self, player_name: str, key: int, events_log: List[KeyPressLog]):
        for event in events_log:
            if event.down is not True:
                continue

            player = self.players[player_name]
            player.action(key)
            if player.body.is_dirty():
                self.desk.check_on_move(player)

            if player.body.rotate != 0:
                self.desk.check_on_rotate(player)

    def update_players(self, events: Dict[int, List[KeyPressLog]]):
        for key, events_log in events.items():
            if len(events_log) == 0:
                continue
            player_names = self.key_map.get(key)
            if player_names is not None:
                for player_name in player_names:
                    self.update_player(player_name, key, events_log)

        self.draw_players()


