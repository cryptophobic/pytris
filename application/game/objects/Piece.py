from typing import List, Tuple

from application.game.objects.Shape import Shape
from application.game.vectors import *
from dataclasses import dataclass


@dataclass
class Pushed:
    mass: int
    direction: Vec2


class Piece:

    def __init__(self,
                 shape: Shape,
                 mass: int = 1,
                 rotate: int = 0,
                 velocity: Vec2 = Vec2(0, 0),
                 pushed: Pushed = None,
                 coordinates: Vec2 = Vec2(0, 0)):
        self.shape: Shape = shape
        self.mass: int = mass
        self.rotate: int = rotate
        self.velocity: Vec2 = velocity
        self.pushed: Pushed = Pushed(mass=0, direction=Vec2(0, 0)) if pushed is None else pushed
        self.coordinates: Vec2 = coordinates

    def is_dirty(self):
        return self.velocity.is_dirty() or self.pushed.direction.is_dirty() or self.rotate != 0

    def push(self, direction: Vec2, mass: int):
        self.pushed.mass += mass
        self.pushed.direction += direction

    def release(self):
        self.pushed.mass = 0
        self.pushed.direction.x = 0
        self.pushed.direction.y = 0
