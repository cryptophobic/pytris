import sys
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


class Desk:
    def __init__(self, height, width):
        self.__width = width
        self.__height = height
        self.__players: Dict[str, List[Position]] = {}
        self.__bricks: List[List[Brick]] = [[] for _ in range(height)]
        self.__desk = [[None for x in range(height)] for y in range(width)]  # type: List[List[Player|Brick|None]]

    def __is_valid_position(self, position: Position) -> bool:
        if not ((0 <= position.x < self.__width) and (position.y < self.__height)):
            #sys.stderr.write(f"Position {position} out of range {self.__width}x{self.__height}")
            return False

        return True

    def __fits(self, player_name: str, shape: np.ndarray, check: Vec2) -> bool:
        for square in shape:
            position = Position(x=check.x + square[0], y=check.y + square[1])
            if not self.__is_valid_position(position):
                return False

            place = self.__desk[position.x][position.y]
            if place is not None and place.name != player_name:
                sys.stdout.write(f"Player {player_name} already occupied\n")
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

            move_commit = self.__fits(player.name, shape, check)
            if move_commit:
                approved_position = check

        if player.body.rotate != 0:
            shape = shapes.rotate(player.body.shape.shape, player.body.rotate)

            rotate_commit = self.__fits(player.name, shape, approved_position)
            if not rotate_commit:
                shape = player.body.shape.shape

        if not move_commit and not rotate_commit and self.__players.get(player.name) is not None:
            return False

        self.remove_player(player.name)
        self.__players[player.name] = []

        for square in shape:
            position = Position(x=approved_position.x + square[0], y=approved_position.y + square[1])
            self.__players[player.name].append(Position(x=position.x, y=position.y))
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
                self.__desk[square.x][square.y] = None

        self.__players.pop(player_name, None)

    def get_players_on_position(self, player_name: str, shape: numpy.ndarray, coordinates: Vec2) -> ObjectsToMove:
        places = set()
        for square in shape:
            if not self.__is_valid_position(Position(x=coordinates.x + square[0], y=coordinates.y + square[1])):
                return ObjectsToMove(mass=-1, objects=set())

            place = self.__desk[coordinates.x + square[0]][coordinates.y + square[1]]

            if type(place) is Brick:
                return ObjectsToMove(mass=-1, objects=set())

            if place is not None and place.name != player_name:
                places.update({place})

        return ObjectsToMove(sum(map(lambda x: x.body.mass, places)), places)

    def check_on_move(self, player: Player) -> bool:
        check = player.body.coordinates + player.body.velocity
        try:
            mass_to_move, places = self.get_players_on_position(player.name, player.body.shape.shape, check)
        except IndexError as error:
            sys.stderr.write(f"check_on_move, {str(error)}\n")
            player.body.velocity = Vec2(0, 0)
            return False

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

    def is_grounded(self, player) -> bool:
        if player.body.velocity.y <= 0:
            return False

        place = player.body.coordinates + Vec2(0, 1)
        shape = player.body.shape.shape
        for square in shape:
            if not self.__is_valid_position(Position(x=place.x + square[0], y=place.y + square[1])):
                return True

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
            self.__desk[place.x + square[0]][place.y + square[1]] = brick
            self.__bricks[place.y].append(brick)

        player.body.shape = Shape()
        player.body.coordinates.y = 0
        player.body.velocity = Vec2(0, 0)
        self.__players[player.name] = []

    def check_on_rotate(self, player: Player) -> bool:
        rotated_shape = shapes.rotate(player.body.shape.shape, player.body.rotate)
        check = player.body.coordinates
        try:
            mass_to_move, places = self.get_players_on_position(player.name, rotated_shape, check)
        except IndexError as error:
            sys.stderr.write(f"check_on_rotate, {str(error)}\n")
            player.body.rotate = 0
            return False

        # TODO: maybe we can try to move nearby objects with rotating
        if mass_to_move > 0:
            player.body.rotate = 0
            return False

        return True
