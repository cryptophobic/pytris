from application.game.objects.shapes import shapes
import random


class Shape:
    def __init__(self, index: int = -1):
        self.shape = shapes[index] if index >= 0 else shapes[random.randint(0, len(shapes) - 1)]
