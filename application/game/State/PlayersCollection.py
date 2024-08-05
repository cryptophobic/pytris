from collections import UserDict

from application.game.Player import Player


class PlayersCollection(UserDict):
    def __init__(self):
        super().__init__()

    def idle_players(self):
        return filter(lambda x: x.idle, self.data.values())

    def to_render_players(self):
        return list(filter(lambda x: x.idle is False, self.data.values()))

    def sorted_dirty_players(self):
        def is_dirty(player: Player) -> bool:
            return player.idle is False and (player.body.is_dirty() or player.above_threshold())

        return sorted(filter(is_dirty, self.data.values()), key=lambda x: x.prio, reverse=True)

    def add(self, player: Player):
        self.data[player.name] = player

    def remove(self, player: Player):
        self.data.pop(player.name, None)
