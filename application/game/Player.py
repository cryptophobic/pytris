from dataclasses import dataclass

from application.game.controls import Controls
from application.objects.Piece import Piece


@dataclass
class Player:
    body:  Piece
    controls: Controls
    score: int = 0
