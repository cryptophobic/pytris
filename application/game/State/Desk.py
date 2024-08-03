from typing import List, NamedTuple, Dict

from application.game.Player import Player
from application.game.types import Vec2


class Position(NamedTuple):
    x: int
    y: int


class Desk:
    def __init__(self, height, width):
        self.__width = width
        self.__height = height
        self.__players: Dict[str, Position] = {}
        self.__desk = [[None for x in range(height)] for y in range(width)]  # type: List[List[Player|None]]

    def __validate_position(self, position: Position):
        if (0 > position.x > self.__width) or (0 > position.y > self.__height):
            raise IndexError(f"Position {position} out of range")

    def put_player(self, player: Player):
        position = Position(x=player.body.coordinates.x, y=player.body.coordinates.y)
        place = self.__desk[position.x][position.y]
        if place is not None:
            raise IndexError(f"Player {player.name} already occupied")

        self.__validate_position(position)
        self.remove_player(player)
        self.__players[player.name] = Position(x=position.x, y=position.y)
        self.__desk[position.x][position.y] = player

    def remove_player(self, player: Player):
        current_position = self.__players.get(player.name)
        if current_position is not None:
            self.__desk[current_position.x][current_position.y] = None

        self.__players.pop(player.name, None)

    def get_player_on_position(self, coordinates: Vec2) -> Player:
        self.__validate_position(Position(x=coordinates.x, y=coordinates.y))
        return self.__desk[coordinates.x][coordinates.y]

    def check_on_move(self, player: Player):
        check = player.body.coordinates + player.body.velocity
        place = self.get_player_on_position(check)
        if place is not None:
            if player.body.mass >= place.body.mass:
                place.prio = player.prio + 1
                place.body.velocity += player.body.velocity
                # TODO: get rid of 2 or more objects to move
                # place.body.push(player.body.velocity, player.body.mass)
            else:
                player.body.velocity = Vec2(0, 0)
