import sys
from typing import List, NamedTuple, Dict, Set
import numpy

from application.game.Player import Player
from application.game.objects import shapes
from application.game.types import Vec2


class Position(NamedTuple):
    x: int
    y: int


class ObjectsToMove(NamedTuple):
    mass: int
    objects: Set[Player]


class Desk:
    def __init__(self, height, width):
        self.__width = width
        self.__height = height
        self.__players: Dict[str, List[Position]] = {}
        self.__desk = [[None for x in range(height)] for y in range(width)]  # type: List[List[Player|None]]

    def __validate_position(self, position: Position):
        if not ((0 <= position.x < self.__width) and (position.y < self.__height)):
            raise IndexError(f"Position {position} out of range")

    def put_player(self, player: Player):
        for square in player.body.shape.shape:
            position = Position(x=player.body.coordinates.x + square[0], y=player.body.coordinates.y + square[1])
            self.__validate_position(position)
            place = self.__desk[position.x][position.y]
            if place is not None and place.name != player.name:
                raise IndexError(f"Player {player.name} already occupied")

        self.remove_player(player)
        self.__players[player.name] = []
        for square in player.body.shape.shape:
            position = Position(x=player.body.coordinates.x + square[0], y=player.body.coordinates.y + square[1])
            self.__players[player.name].append(Position(x=position.x, y=position.y))
            self.__desk[position.x][position.y] = player

    def remove_player(self, player: Player):
        current_position = self.__players.get(player.name)
        if current_position is not None:
            for square in current_position:
                self.__desk[square.x][square.y] = None

        self.__players.pop(player.name, None)

    def get_player_on_position(self, player_name: str, shape: numpy.ndarray, coordinates: Vec2) -> ObjectsToMove:
        places = set()
        for square in shape:
            self.__validate_position(Position(x=coordinates.x + square[0], y=coordinates.y + square[1]))
            place = self.__desk[coordinates.x + square[0]][coordinates.y + square[1]]
            if place is not None and place.name != player_name:
                places.update({place})

        return ObjectsToMove(sum(map(lambda x: x.body.mass, places)), places)

    def check_on_move(self, player: Player) -> bool:
        check = player.body.coordinates + player.body.velocity
        try:
            mass_to_move, places = self.get_player_on_position(player.name, player.body.shape.shape, check)
        except IndexError as error:
            sys.stderr.write(f"check_on_move, {str(error)}\n")
            player.body.velocity = Vec2(0, 0)
            return False

        if mass_to_move > player.body.mass:
            player.body.velocity = Vec2(0, 0)
            return False

        for place in places:
            place.prio = player.prio + 1
            place.body.velocity += player.body.velocity

        return True

    def check_on_rotate(self, player: Player) -> bool:
        rotated_shape = shapes.rotate(player.body.shape.shape, player.body.rotate)
        check = player.body.coordinates
        try:
            mass_to_move, places = self.get_player_on_position(player.name, rotated_shape, check)
        except IndexError as error:
            sys.stderr.write(f"check_on_rotate, {str(error)}\n")
            player.body.rotate = 0
            return False

        # TODO: maybe we can try to move nearby objects with rotating
        if mass_to_move > 0:
            player.body.rotate = 0
            return False

        return True
