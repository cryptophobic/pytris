from application.game.objects.Shape import Shape
from application.game.objects.types import *
from dataclasses import dataclass


@dataclass
class Piece:
    shape: Shape = None
    mass: int = 1
    velocity: Vec2 = Vec2(0, 0)
    direction: Vec2 = Vec2(0, 0)
    coordinates: Vec2 = Vec2(0, 0)



