from application.game.controls import MoveControls
from application.game.objects.Piece import Piece


class Player:

    def __init__(self, name: str, controls: MoveControls):
        self.name = name
        self.body: Piece = None
        self.controls = controls
        self.score: int = 0
