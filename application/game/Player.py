from application.game.controls import MoveControls
from application.game.objects.Piece import Piece
from application.game.objects.Shape import Shape
from application.game.types import Vec2


class Player:

    def __init__(self, name: str, controls: MoveControls):
        self.name = name
        self.ready_for_render = True
        self.prio = 0
        self.body: Piece = Piece(
            shape=Shape(),
            velocity=Vec2(x=0, y=0),
            coordinates=Vec2(x=0, y=0),
        )
        self.controls = controls
        self.score: int = 0

    def action(self, key: int):
        self.controls.action(key, self.body)

