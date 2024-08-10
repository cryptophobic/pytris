from typing import List, NamedTuple, Set, Tuple
import numpy

from application.game.Player import Player
from application.game.State.PlayersCollection import PlayersCollection
from application.game.objects import shapes
from application.game.objects.Shape import Shape
from application.game.vectors import Vec2


class Brick(NamedTuple):
    color: Tuple[int, int, int]
    position: Vec2
    name: str
    mass: int = -1


class ObjectsToMove(NamedTuple):
    mass: int
    objects: Set[Player | Brick]
    proposed_velocity: Vec2 = Vec2(0, 0)


class Desk:
    def __init__(self, height, width, players: PlayersCollection):
        self.__gateway: Player | None = None
        self.__width = width
        self.__height = height
        self.__players: PlayersCollection = players
        self.__bricks: List[List[Brick]] = [[] for _ in range(height)]
        self.__desk = [[None for x in range(height)] for y in range(width)]  # type: List[List[Player|Brick|None]]

    def __is_valid_position(self, position: Vec2) -> bool:
        if not ((0 <= position.x < self.__width) and (position.y < self.__height)):
            return False

        return True

    @property
    def bricks(self) -> List[Brick]:
        return [x for n in self.__bricks for x in n]

    def remove_player(self, player_name: str):
        player = self.__players.get(player_name)
        if player is None:
            return

        for square in player.body.shape.shape:
            position = player.body.coordinates + square
            if position.y < 0:
                continue
            self.__desk[position.x][position.y] = None

    def get_obstacles_on_position(self, player_name: str, shape: numpy.ndarray, check: Vec2) -> ObjectsToMove:
        places = set()
        for square in shape:
            position = check + square
            if position.y < 0:
                continue

            if not self.__is_valid_position(position):
                return ObjectsToMove(mass=-1, objects=set())

            place = self.__desk[position.x][position.y]

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

        objects_to_move = self.get_obstacles_on_position(player.name, player.body.shape.shape, player.body.coordinates)
        if objects_to_move.mass != 0:
            return False

        player.idle = False
        self.set_new_position(player)
        return True

    def is_grounded(self, player) -> bool:
        place = player.body.coordinates + Vec2(0, 1)
        shape = player.body.shape.shape

        objects_to_move = self.get_obstacles_on_position(player.name, shape, place)
        return objects_to_move.mass == -1

    def ground(self, player):
        shape = player.body.shape.shape
        place = player.body.coordinates
        for square in shape:
            brick_position = place + square
            brick = Brick(
                color=player.body.shape.color,
                name=player.name,
                position=brick_position)
            if place.y + square[1] < 0:
                continue

            self.__desk[brick_position.x][brick_position.y] = brick
            self.__bricks[brick_position.y].append(brick)

        player.body.shape = Shape()
        player.body.velocity = Vec2(0, 0)
        player.body.rotate = 0
        player.body.coordinates = Vec2(self.__width // 2, -1)
        player.idle = True

    def remove_lines(self):
        pass

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

    def rotate(self, player, with_mass) -> tuple[bool, int]:
        rotated_shape = shapes.rotate(player.body.shape.shape, player.body.rotate)
        objects_to_move = self.get_obstacles_on_position(player.name, rotated_shape, player.body.coordinates)
        is_place_available = 0 <= objects_to_move.mass <= with_mass

        if not is_place_available:
            return False, -1

        self.set_new_position(player, player.body.coordinates, rotated_shape)
        player.body.rotate = 0

        return True, objects_to_move.mass

    def move(self, player, with_mass: int = 0) -> tuple[bool, int]:
        player_body_velocity = player.body.velocity
        place = player.body.coordinates + player_body_velocity
        player.body.velocity = Vec2(0, 0)

        objects_to_move = self.get_obstacles_on_position(player.name, player.body.shape.shape, place)
        is_place_available = 0 <= objects_to_move.mass <= with_mass

        if not is_place_available:
            return False, -1

        if is_place_available:
            for moveable_object in objects_to_move.objects:
                moveable_object_velocity = moveable_object.body.velocity
                moveable_object.body.velocity = player_body_velocity
                is_place_available, mass = self.move(moveable_object, with_mass - moveable_object.body.mass)
                moveable_object.body.velocity = moveable_object_velocity
                if not is_place_available:
                    return False, mass

        self.set_new_position(player, place, player.body.shape.shape)

        return True, with_mass - objects_to_move.mass

    def apply(self, player: Player) -> bool:
        possible_grounded = False

        applied = False

        if player.body.velocity.is_dirty():
            to = player.body.velocity
            push_mass = player.body.mass
            last_velocity = Vec2(0, 0)
            for possible_velocity in Vec2(0, 0).iterate_to(to):
                player_velocity = possible_velocity - last_velocity
                player.body.velocity = player_velocity
                last_velocity = possible_velocity
                [is_moved, push_mass] = self.move(player, with_mass=push_mass)
                applied |= is_moved

                if not is_moved:
                    possible_grounded = player_velocity.y > 0
                    break

        if player.body.rotate != 0:
            rotate = player.body.rotate
            direction = 1 if rotate > 0 else -1
            push_mass = player.body.mass
            for _ in range(0, rotate, direction):
                player.body.rotate = direction
                [is_rotated, push_mass] = self.rotate(player, with_mass=push_mass)
                applied |= is_rotated
                if not is_rotated:
                    break

        if possible_grounded and self.is_grounded(player):
            self.ground(player)

        return applied
