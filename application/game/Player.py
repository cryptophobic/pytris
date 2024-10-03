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
        self.__speed: float = speed
        self.__dirty_speed = True
        self.grounded_number: int = 0
        self.__idle: bool = True
        self.name = name
        self.prio = 0
        self.controls = controls
        self.score: int = 0

    @property
    def speed(self):
#        print(self.__speed, self.grounded_number * 0.3, self.score * 0.4)
        if ((self.__speed + self.grounded_number * 0.3) - self.score * 0.4) <= 0:
            return self.__speed

        return self.__speed + self.grounded_number * 0.3 - self.score * 0.4

    def update_speed(self, update: float) -> None:
        self.__dirty_speed = update

    def commit_speed(self):
        self.update_speed(False)

    def speed_pending(self):
        return self.__dirty_speed

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


