import sys
from dataclasses import dataclass
from typing import List, NamedTuple, Dict, Set, Tuple
import numpy
import numpy as np

from application.game.Player import Player
from application.game.objects import shapes
from application.game.objects.Shape import Shape
from application.game.vectors import Vec2


class Position(NamedTuple):
    x: int
    y: int


class Brick(NamedTuple):
    color: Tuple[int, int, int]
    position: Position
    name: str


class ObjectsToMove(NamedTuple):
    mass: int
    objects: Set[Player | Brick] | None


@dataclass
class Cell:
    borders: int = 0
    entity: Player | Brick | None = None


class Desk:
    def __init__(self, height, width):
        self.__gateway: Player|None = None
        self.__width = width
        self.__height = height
        self.__players: Dict[str, List[Position]] = {}
        self.__bricks: List[List[Brick]] = [[] for _ in range(height)]
        self.__desk = [[None for x in range(height)] for y in range(width)]  # type: List[List[Player|Brick|None]]

    def __is_valid_position(self, position: Position) -> bool:
        if not ((0 <= position.x < self.__width) and (position.y < self.__height)):
            return False

        return True

    @property
    def bricks(self) -> List[Brick]:
        return [x for n in self.__bricks for x in n]

    def put_player(self, player: Player) -> bool:
        approved_position = player.body.coordinates
        move_commit = rotate_commit = False
        shape = player.body.shape.shape
        if player.body.is_dirty():
            check = approved_position + player.body.velocity

            [mass, places] = self.get_obstacles_on_position(player.name, shape, check)
            if mass == 0:
                move_commit = True
                approved_position = check

        if player.body.rotate != 0:
            shape = shapes.rotate(player.body.shape.shape, player.body.rotate)

            [mass, places] = self.get_obstacles_on_position(player.name, shape, approved_position)
            if mass != 0:
                shape = player.body.shape.shape
            else:
                rotate_commit = True

        if not move_commit and not rotate_commit and self.__players.get(player.name) is not None:
            return False

        self.remove_player(player.name)
        self.__players[player.name] = []

        for square in shape:
            position = Position(x=approved_position.x + square[0], y=approved_position.y + square[1])
            self.__players[player.name].append(Position(x=position.x, y=position.y))
            if position.y < 0:
                continue
            self.__desk[position.x][position.y] = player

        player.body.coordinates = approved_position
        player.body.shape.shape = shape
        player.body.rotate = 0
        player.body.velocity = Vec2(0, 0)
        return True

    def remove_player(self, player_name: str):
        current_position = self.__players.get(player_name)
        if current_position is not None:
            for square in current_position:
                if square.y < 0:
                    continue
                self.__desk[square.x][square.y] = None

        self.__players.pop(player_name, None)

    def get_obstacles_on_position(self, player_name: str, shape: numpy.ndarray, check: Vec2) -> ObjectsToMove:
        places = set()
        for square in shape:

            if check.y + square[1] < 0:
                continue

            if not self.__is_valid_position(Position(x=check.x + square[0], y=check.y + square[1])):
                return ObjectsToMove(mass=-1, objects=set())

            place = self.__desk[check.x + square[0]][check.y + square[1]]

            if type(place) is Brick:
                return ObjectsToMove(mass=-1, objects=set())

            if place is not None and place.name != player_name:
                places.update({place})

        return ObjectsToMove(sum(map(lambda x: x.body.mass, places)), places)

    def __reserve_gateway(self, player: Player):
        if self.__gateway is None:
            self.__gateway = player
            return True

        if self.__gateway.name == player.name:
            return True

        if self.__gateway.body.coordinates.y >= 2:
            self.__gateway = player
            return True

        return False

    def activate_player(self, player: Player):
        if not self.__reserve_gateway(player):
            return False

        [mass, places] = self.get_obstacles_on_position(player.name, player.body.shape.shape, player.body.coordinates)
        if mass != 0:
            return False

        player.idle = False
        self.put_player(player)
        return True

    def is_grounded(self, player) -> bool:
        if player.body.velocity.y <= 0:
            return False

        place = player.body.coordinates + Vec2(0, 1)
        shape = player.body.shape.shape
        for square in shape:
            if not self.__is_valid_position(Position(x=place.x + square[0], y=place.y + square[1])):
                return True

            if place.y + square[1] < 0:
                continue

            is_ground = self.__desk[place.x + square[0]][place.y + square[1]]
            if is_ground is not None and type(is_ground) is Brick:
                return True

        return False

    def ground(self, player):
        shape = player.body.shape.shape
        place = player.body.coordinates
        for square in shape:
            brick = Brick(
                color=player.body.color,
                name=player.name,
                position=Position(x=place.x + square[0], y=place.y + square[1]))
            if place.y + square[1] < 0:
                continue

            self.__desk[place.x + square[0]][place.y + square[1]] = brick
            self.__bricks[place.y].append(brick)

        player.body.shape = Shape()
        player.body.velocity = Vec2(0, 0)
        player.body.coordinates = Vec2(self.__width // 2, -1)
        player.idle = True

        self.__players[player.name] = []

    def check_on_move(self, player: Player) -> bool:
        check = player.body.coordinates + player.body.velocity
        mass_to_move, places = self.get_obstacles_on_position(player.name, player.body.shape.shape, check)

        if mass_to_move > player.body.mass:
            player.body.velocity = Vec2(0, 0)
            return False

        if mass_to_move < 0:
            if self.is_grounded(player):
                self.ground(player)
            else:
                player.body.velocity.x = 0

            return False

        for place in places:
            place.prio = player.prio + 1
            place.body.velocity += player.body.velocity

        return True

    def check_on_rotate(self, player: Player) -> bool:
        rotated_shape = shapes.rotate(player.body.shape.shape, player.body.rotate)
        mass_to_move, places = self.get_obstacles_on_position(player.name, rotated_shape, player.body.coordinates)

        # TODO: maybe we can try to move nearby objects with rotating
        if mass_to_move > 0:
            player.body.rotate = 0
            return False

        return True
