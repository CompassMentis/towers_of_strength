import random

from vector import Vector


class Flutter:
    def __init__(self, image):
        self.image = image
        self.offset = Vector(random.randint(-20, 20), random.randint(-20, 20))
        self.countdown = 100
