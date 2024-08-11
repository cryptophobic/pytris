from typing import List

from application.game.controls import MoveControls
from application.game.objects.Piece import Piece
from application.game.objects.Shape import Shape
from application.game.vectors import Vec2


class Player:

    def __init__(self,
                 name: str,
                 controls: MoveControls,
                 speed: float = 1.0):

        self.body: Piece = Piece(shape=Shape(), velocity=Vec2(x=0, y=0), coordinates=Vec2(x=0, y=0))
        self.__speed: List = [speed, False]
        self.__idle: bool = True
        self.name = name
        self.prio = 0
        self.controls = controls
        self.score: int = 0

    @property
    def speed(self):
        return self.__speed[0] + self.score * 0.01

    @speed.setter
    def speed(self, speed: float) -> None:
        self.__speed = [speed, False]

    def commit_speed(self):
        self.__speed[1] = True

    def speed_pending(self):
        return self.__speed[1]

    @property
    def idle(self) -> bool:
        return self.__idle

    @idle.setter
    def idle(self, value: bool):
        self.__idle = value

    def dispatch(self, key: int):
        self.controls.action(key, self.body)

    def move_down(self):
        self.controls.move_down(self.body)


