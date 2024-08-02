from application.Events import KeyPressLog
from application.game.Player import Player
from typing import Dict, List, Set
import numpy as np
import math


from application.game.objects.Piece import Piece
from application.game.objects.Shape import Shape
from application.game.types import Vec2


class State:
    def __init__(self):
        self.desk = [[None for x in range(50)] for y in range(50)]
        self.place = 10
        self.players: Dict[str, Player] = {}
        self.key_map: Dict[int, Set[str]] = {}
        self.changed = False
        pass

    def register_player(self, player: Player):
        self.players[player.name] = player
        player.body = Piece(shape=Shape(), velocity=Vec2(x=0, y=0), coordinates=Vec2(x=self.place, y=25))
        self.desk[player.body.coordinates.x][player.body.coordinates.y] = player
        self.place += 20
        for key in player.controls.keys():
            if self.key_map.get(key) is None:
                self.key_map[key] = set()
            self.key_map[key].update({player.name})

    def move_players(self):
        for player in self.players.values():
            check = Vec2(player.body.coordinates.x, player.body.coordinates.y)
            if 0 < player.body.velocity.y < 10:
                player.body.velocity.y = 10
            if 0 < player.body.velocity.x < 10:
                player.body.velocity.x = 10

            player.body.coordinates.x += player.body.velocity.scalar_multiply(0.1).x
            player.body.coordinates.y += player.body.velocity.scalar_multiply(0.1).y
            self.desk[check.x][check.y] = None
            self.desk[player.body.coordinates.x][player.body.coordinates.y] = player
            player.body.velocity.y = 0
            player.body.velocity.x = 0

    def update_player(self, player_name: str, key: int, events_log: List[KeyPressLog]):
        print(f"{player_name} ")
        for event in events_log:
            if event.down is True:
                self.changed = True
                player = self.players[player_name]
                player.action(key)
                check = player.body.coordinates + player.body.velocity.scalar_multiply(0.1)
                place = self.desk[check.x][check.y] # type: Player
                if place is not None:
                    distance = player.body.coordinates.distance_to(check)
                    if distance >= place.body.mass:
                        place.body.velocity += player.body.velocity.scalar_multiply(0.5)

    def update_players(self, events: Dict[int, List[KeyPressLog]]):
        for key, events_log in events.items():
            if len(events_log) == 0:
                continue
            player_names = self.key_map.get(key)
            if player_names is not None:
                for player_name in player_names:
                    self.update_player(player_name, key, events_log)

        if self.changed is True:
            self.move_players()


