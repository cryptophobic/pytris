from application.game.objects.shapes import shapes, colors
import random


class Shape:
    def __init__(self, index: int = -1):
        index = index if index >= 0 else random.randint(0, len(shapes) - 1)
        self.shape = shapes[index]
        self.color = colors[index]
