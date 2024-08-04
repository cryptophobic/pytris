import sys

from application.game.events.Events import KeyPressLog
from application.game.Player import Player
from typing import Dict, List

from application.game.State.Desk import Desk
from application.game.State.KeyMap import KeyMap
from application.game.State.PlayersCollection import PlayersCollection
from application.game.vectors import Vec2


class State:
    def __init__(self):
        self.ready_for_render = True
        self.desk = Desk(30, 15)
        self.place = 3
        self.players = PlayersCollection()
        self.key_map = KeyMap()
        self.changed = False
        pass

    def register_player(self, player: Player):
        player.body.velocity = Vec2(0, 0)
        player.body.coordinates = Vec2(x=self.place, y=0)
        self.players.add(player)
        try:
            self.desk.put_player(player)
        except IndexError as e:
            sys.stderr.write(str(e))

        self.key_map.load_keys_from_player(player)

        self.place += 5

    def draw_players(self):
        for player in self.players.sorted_dirty_players():
            if player.above_threshold():
                player.move_down()
                player.calculate_threshold()

            if self.desk.put_player(player):
                self.ready_for_render = True

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


