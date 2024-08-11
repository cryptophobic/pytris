from typing import List, Dict, NamedTuple, Tuple

import numpy

from application import config
from application.game.Player import Player
from application.game.vectors import Vec2


class Brick(NamedTuple):
    color: Tuple[int, int, int]
    name: str
    position: Vec2 = Vec2(0, 0)
    mass: int = -1


class Ground:
    def __init__(self):
        self.lines_to_erase = set()
        self.__bricks: List[Dict[int, Brick]] = [{} for _ in range(config.DESK_HEIGHT)]
        self.__bricks_in_line: List[Brick] = []

    @property
    def bricks_in_line(self) -> List[Brick]:
        return self.__bricks_in_line

    @property
    def bricks(self) -> List[Dict[int, Brick]]:
        return self.__bricks

    def __rebuild_bricks_in_line(self):
        self.__bricks_in_line = list()
        for y, line_bricks in enumerate(self.__bricks):
            for x, brick in line_bricks.items():
                self.__bricks_in_line.append(Brick(color=brick.color, name=brick.name, position=Vec2(x, y)))

    def is_lines_erased(self) -> int:
        erased = 0
        for line in sorted(self.lines_to_erase):
            erased += 1
            self.__bricks.pop(line)
            self.__bricks = [{}] + self.__bricks

        self.lines_to_erase = set()
        if erased > 0:
            self.__rebuild_bricks_in_line()
        return erased

    def get_bricks_or_ground_on_position(self, shape: numpy.ndarray, check: Vec2) -> bool:
        for square in shape:
            position = check + square
            if position.y < 0:
                continue

            if position.y >= config.DESK_HEIGHT:
                return True

            if self.__bricks[position.y].get(position.x) is not None:
                return True

        return False

    def is_grounded(self, player: Player) -> bool:
        place = player.body.coordinates + Vec2(0, 1)
        shape = player.body.shape.shape

        is_bricks_or_ground = self.get_bricks_or_ground_on_position(shape, place)

        if is_bricks_or_ground is False:
            return False

        for square in shape:
            brick_position = player.body.coordinates + square
            if brick_position.y < 0:
                continue
            self.__bricks[brick_position.y][brick_position.x] = Brick(
                color=player.body.shape.color,
                name=player.name)

            if len(self.__bricks[brick_position.y]) == config.DESK_WIDTH:
                self.lines_to_erase.update({brick_position.y})

        self.__rebuild_bricks_in_line()

        return True
