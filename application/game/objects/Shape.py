from application.game.objects.shapes import shapes
import random


class Shape:
    def __init__(self, index=-1):
        self.shape = shapes[index] if index >= 0 else random.randint(0, len(shapes) - 1)