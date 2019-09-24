import pygame

import utils


class Runner:
    def __init__(self, game):
        # TODO: Multiple runners, moving runners etc
        self.game = game
        self.image = pygame.image.load('images/runners/runner01.png')

        self.route = self.game.route[:]
        self.location = None
        self.happiness = 3
        self.hydration = 6
        self.energy = 6
        self.set_location()

    def draw(self):
        self.game.canvas.blit(self.image, self.location)

    def set_location(self):
        self.location = utils.cell_to_isometric((self.route[0].x, self.route[0].y))

        # TODO: Calcate offset and/or put in Settings
        self.location = self.location[0] + 20, self.location[1] - 10

    def to_next_tile(self):
        if not self.route:
            return
        del self.route[0]
        if self.route:
            self.set_location()
