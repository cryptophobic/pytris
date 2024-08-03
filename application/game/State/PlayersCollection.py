from collections import UserDict
from dataclasses import dataclass

from application.game.Player import Player


class PlayersCollection(UserDict):
    def __init__(self):
        super().__init__()

    def sorted_dirty_players(self):
        def is_dirty(player: Player) -> bool:
            return player.body.is_dirty()

        return sorted(filter(is_dirty, self.data.values()), key=lambda x: x.prio, reverse=True)

    def add(self, player: Player):
        self.data[player.name] = player

    def remove(self, player: Player):
        self.data.pop(player.name, None)
