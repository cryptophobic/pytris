from typing import NamedTuple, Set, List, Tuple

import numpy

from application.game.Player import Player
from application.game.State.Ground import Ground, Brick
from application.game.State.PlayersCollection import PlayersCollection
from application.game.vectors import Vec2


class ObjectsToMove(NamedTuple):
    mass: int
    objects: Set[Player | Brick]
    proposed_velocity: Vec2 = Vec2(0, 0)


class Desk:
    def __init__(self, players: PlayersCollection, ground: Ground, width: int, height: int):
        self.__ground: Ground = ground
        self.players = players
        self.__width = width
        self.__height = height
        self.__desk = [[None for x in range(height)] for y in range(width)]  # type: List[List[Player|None]]

    @property
    def height(self):
        return self.__height

    @property
    def width(self):
        return self.__width

    def __is_valid_position(self, position: Vec2) -> bool:
        if not ((0 <= position.x < self.__width) and (0 <= position.y < self.__height)):
            return False

        return True

    def remove_player(self, player_name: str):
        player = self.players.get(player_name)
        if player is None:
            return

        for square in player.body.shape.shape:
            position = player.body.coordinates + square
            if position.y < 0:
                continue
            self.__desk[position.x][position.y] = None

    def set_new_position(self, player: Player, position: Vec2 | None = None, shape: numpy.ndarray | None = None):
        if position is not None and shape is not None:
            self.remove_player(player.name)
        else:
            shape = player.body.shape.shape
            position = player.body.coordinates

        for square in shape:
            square_position = position + square
            if square_position.y < 0:
                continue
            self.__desk[square_position.x][square_position.y] = player

        player.body.coordinates = position
        player.body.shape.shape = shape

    def get_obstacles_on_position(self, player_name: str, shape: numpy.ndarray, check: Vec2) -> ObjectsToMove:
        places = set()
        for square in shape:
            position = check + square
            if position.y < 0:
                continue

            if not self.__is_valid_position(position):
                return ObjectsToMove(mass=-1, objects=set())

            place = self.__ground.bricks[position.y].get(position.x)

            if type(place) is Brick:
                return ObjectsToMove(mass=-1, objects=set())

            place = self.__desk[position.x][position.y]

            if place is not None and place.name != player_name:
                places.update({place})

        return ObjectsToMove(sum(map(lambda x: x.body.mass, places)), places)

    def add_player(self, player) -> bool:
        objects_to_move = self.get_obstacles_on_position(player.name, player.body.shape.shape, player.body.coordinates)
        if objects_to_move.mass != 0:
            return False

        self.set_new_position(player)
        return True
