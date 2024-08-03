from typing import List, NamedTuple, Dict

from application.game.Player import Player
from application.game.objects.Shape import Shape
from application.game.types import Vec2


class Position(NamedTuple):
    x: int
    y: int


class Desk:
    def __init__(self, height, width):
        self.__width = width
        self.__height = height
        self.__players: Dict[str, List[Position]] = {}
        self.__desk = [[None for x in range(height)] for y in range(width)]  # type: List[List[Player|None]]

    def __validate_position(self, position: Position):
        if (0 > position.x > self.__width) or (0 > position.y > self.__height):
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

    # TODO: return array of possible players
    def get_player_on_position(self, player: Player, coordinates: Vec2) -> Player | None:
        for square in player.body.shape.shape:
            self.__validate_position(Position(x=coordinates.x + square[0], y=coordinates.y + square[1]))
            place = self.__desk[coordinates.x + square[0]][coordinates.y + square[1]]
            if place is not None and place.name != player.name:
                return place

        return None

    def check_on_move(self, player: Player):
        check = player.body.coordinates + player.body.velocity
        place = self.get_player_on_position(player, check)
        if place is not None:
            # place.prio = player.prio + 1
            # place.body.push(player.body.velocity, player.body.mass)
            if player.body.mass >= place.body.mass:
                place.prio = player.prio + 1
                place.body.velocity += player.body.velocity
                # TODO: get rid of 2 or more objects to move
                # place.body.push(player.body.velocity, player.body.mass)
            else:
                player.body.velocity = Vec2(0, 0)
