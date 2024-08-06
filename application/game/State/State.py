import sys

from application import config
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
        self.desk = Desk(config.DESK_HEIGHT, config.DESK_WIDTH)
        self.players = PlayersCollection()
        self.key_map = KeyMap()
        self.changed = False
        pass

    def register_player(self, player: Player):
        player.body.velocity = Vec2(0, 0)
        player.body.coordinates = Vec2(x=config.DESK_WIDTH // 2, y=-1)
        self.players.add(player)
        self.key_map.load_keys_from_player(player)

    def draw_players(self):
        for player in self.players.idle_players():
            self.desk.activate_player(player)

        for player in self.players.sorted_dirty_players():
            if player.above_threshold():
                player.move_down()
                self.desk.check_on_move(player)
                player.calculate_threshold()

            if self.desk.put_player(player):
                self.ready_for_render = True

    def update_player(self, player_name: str, key: int, events_log: List[KeyPressLog]):
        for event in events_log:
            if event.down is not True:
                continue

            player = self.players[player_name]
            if player.idle:
                continue

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
