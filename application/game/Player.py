from typing import Tuple

from application import config
from application.Timer import Timer
from application.game.controls import MoveControls
from application.game.objects.Piece import Piece
from application.game.objects.Shape import Shape
from application.game.vectors import Vec2


class Player:

    def __init__(self, name: str, controls: MoveControls, speed: float = 1, color: Tuple[int, int, int] = (255, 255, 255),):
        self.speed = speed
        self.down_threshold = Timer.current_timestamp()
        self.name = name
        self.ready_for_render = True
        self.prio = 0
        self.body: Piece = Piece(
            shape=Shape(),
            velocity=Vec2(x=0, y=0),
            coordinates=Vec2(x=0, y=0),
            color=color
        )
        self.controls = controls
        self.score: int = 0

    def above_threshold(self):
        return Timer.current_timestamp() > self.down_threshold

    def calculate_threshold(self):
        down_interval = config.INITIAL_SPEED_OF_FALLING_DOWN // self.speed
        self.down_threshold = Timer.current_timestamp() + down_interval

    def action(self, key: int):
        self.controls.action(key, self.body)

    def move_down(self):
        self.controls.move_down(self.body)


