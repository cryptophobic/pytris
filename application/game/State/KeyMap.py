from collections import UserDict
from typing import List

from application.game.Player import Player


class KeyMap(UserDict):
    def __init__(self):
        super().__init__()

    def load_keys_from_player(self, player: Player):
        for key in player.controls.keys():
            self.add(key, player.name)

    def add(self, key: int, player_name: str):
        if self.data.get(key) is None:
            self.data[key] = set()
        self.data[key].update({player_name})

    def remove(self, key: int):
        self.data.pop(key, None)
