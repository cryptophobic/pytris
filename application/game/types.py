from dataclasses import dataclass
import math

@dataclass
class Vec2:
    x: int
    y: int

    def __add__(self, other):
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vec2(self.x - other.x, self.y - other.y)

    def distance_to(self, other):
        return math.dist([self.x, self. y], [other.x, other.y])

    def scalar_multiply(self, scalar):
        return Vec2(self.x * scalar, self.y * scalar)


