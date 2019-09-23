import pygame

from settings import Settings
import utils


class Runner:
    def __init__(self, game):
        # TODO: Multiple runners, moving runners etc
        self.game = game
        self.raw_image = pygame.image.load('images/runners/runner.png')
        self.image = pygame.transform.scale(self.raw_image, Settings.runner_size)

        self.route = self.game.route[:]
        self.location = None
        self.set_location()

    def draw(self):
        self.game.canvas.blit(self.image, self.location)

    def set_location(self):
        self.location = utils.cell_to_isometric(self.route[0].cell)

        # TODO: Calcate offset and/or put in Settings
        self.location = self.location[0] + 20, self.location[1] - 10

    def to_next_tile(self):
        if not self.route:
            return
        del self.route[0]
        self.set_location()