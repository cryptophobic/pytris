from collections import UserDict

from application.Timer import Timer
from application.game.Player import Player


class PlayersCollection(UserDict):
    def __init__(self):
        super().__init__()

    def idle_players(self):
        return filter(lambda x: x.idle, self.data.values())

    def to_render_players(self):
        return list(filter(lambda x: x.idle is False, self.data.values()))

    def to_apply_speed_players(self):
        return list(filter(lambda x: x.speed_pending() is False, self.data.values()))

    def sorted_dirty_players(self):
        def is_dirty(player: Player) -> bool:
            return player.idle is False and (player.body.is_dirty())

        return sorted(filter(is_dirty, self.data.values()), key=lambda x: x.prio, reverse=True)

    def add(self, player: Player):
        self.data[player.name] = player

    def remove(self, player: Player):
        self.data.pop(player.name, None)
