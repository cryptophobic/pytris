from typing import List

from application.game.Player import Player
from application.game.State.Desk import Brick, Desk
from application.game.vectors import Vec2


class Ground:
    def __init__(self, desk: Desk):
        self.desk = desk
        self.__bricks: List[List[Brick]] = [[] for _ in range(self.desk.height)]

    @property
    def bricks(self) -> List[Brick]:
        return [x for n in self.__bricks for x in n]

    def is_grounded(self, player: Player) -> bool:
        place = player.body.coordinates + Vec2(0, 1)
        shape = player.body.shape.shape

        objects_to_move = self.desk.get_obstacles_on_position(player.name, shape, place)
        return objects_to_move.mass == -1

    def ground(self, player):
        shape = player.body.shape.shape
        place = player.body.coordinates
        for square in shape:
            brick_position = place + square
            if brick_position.y < 0:
                continue
            self.__bricks[brick_position.y].append(Brick(
                color=player.body.shape.color,
                name=player.name,
                position=brick_position))
