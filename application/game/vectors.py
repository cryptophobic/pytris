from dataclasses import dataclass
import math


@dataclass
class Vec2:
    x: int
    y: int

    X = 0
    Y = 1

    def is_dirty(self) -> bool:
        return self.x != 0 or self.y != 0

    def __getitem__(self, item: int) -> int:
        if item > 1:
            raise IndexError("Out of range of 2 dimensional vector")

        return (self.x, self.y)[item]

    def __add__(self, other):
        return Vec2(self.x + other[Vec2.X], self.y + other[Vec2.Y])

    def __sub__(self, other):
        return Vec2(self.x - other[Vec2.X], self.y - other[Vec2.Y])

    def __neg__(self):
        return Vec2(-self.x, -self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return self.x != other.x or self.y != other.y

    def iterate_to(self, other):
        return iterate_path(self, other)

    def iterate_from(self, other):
        return iterate_path(other, self)

    def distance_to(self, other):
        return math.dist([self.x, self. y], [other[Vec2.X], other[Vec2.Y]])

    def scalar_multiply(self, scalar):
        return Vec2(int(self.x * scalar), int(self.y * scalar))


def iterate_path(from_vec: Vec2, to_vec: Vec2):
    incr = Vec2(1 if to_vec.x > from_vec.x else -1, 1 if to_vec.y > from_vec.y else -1)
    res = Vec2(from_vec.x, from_vec.y)

    while res != to_vec:
        if res.x != to_vec.x:
            res.x += incr.x
            yield res

        if res.y != to_vec.y:
            res.y += incr.y
            yield res
