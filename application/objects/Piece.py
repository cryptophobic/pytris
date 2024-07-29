from application.objects.Shape import Shape
from application.objects.types import *
from dataclasses import dataclass


@dataclass
class Piece:
    shape: Shape
    mass: int
    velocity: Vec2
    direction: Vec2
    coordinates: Vec2
