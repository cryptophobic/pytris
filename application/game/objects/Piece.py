from application.game.objects.Shape import Shape
from application.game.types import *


class Piece:

    def __init__(self, shape: Shape, mass: int = 10, rotate: int = 0, velocity: Vec2 = Vec2(0, 0), direction: Vec2 = Vec2(0, 0), coordinates: Vec2 = Vec2(0, 0)):
        self.shape: Shape = shape
        self.mass: int = mass
        self.rotate: int = rotate
        self.velocity: Vec2 = velocity
        self.direction: Vec2 = direction
        self.coordinates: Vec2 = coordinates



