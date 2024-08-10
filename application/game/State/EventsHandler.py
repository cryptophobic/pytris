from typing import Dict, List

from application.game.Player import Player
from application.game.State.PlayersCollection import PlayersCollection
from application.game.events.Events import KeyPressLog


class EventsHandler:
    def __init__(self, players: PlayersCollection):
        self.players: PlayersCollection = players
        self.__keys: Dict[str: set[str]] = {}

    def dispatch_events(self, events: Dict[int, List[KeyPressLog]]):
        for key, events_log in events.items():
            if len(events_log) == 0:
                continue
            player_names = self.__keys.get(key)
            if player_names is None:
                continue

            for player_name in player_names:
                self.update_player(player_name, key, events_log)

    def update_player(self, player_name: str, key: int, events_log: List[KeyPressLog]):
        for event in events_log:
            if event.down is not True:
                continue

            player = self.players.get(player_name)
            if player is None or player.idle:
                continue

            player.dispatch(key)

    def load_keys_from_player(self, player: Player):
        for key in player.controls.keys():
            self.add_key(key, player.name)

    def add_key(self, key: int, player_name: str):
        if self.__keys.get(key) is None:
            self.__keys[key] = set()
        self.__keys[key].update({player_name})

    def remove_key(self, key: int, player_name: str = ""):
        if player_name == "":
            self.__keys.pop(key, None)
            return

        set_of_players = self.__keys.get(key)
        if set_of_players is not None and player_name in set_of_players:
            set_of_players.remove(player_name)

        if len(set_of_players) == 0:
            self.__keys.pop(key, None)
