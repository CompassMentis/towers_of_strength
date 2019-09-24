import pygame

from mixins import MouseEventHandlerMixin
from settings import Settings

class Tower(MouseEventHandlerMixin):
    def __init__(self, location, game):
        self.location = location
        self.game = game
        self.raw_image = None
        self.image = None

    def draw(self):
        self.game.canvas.blit(self.image, self.location)


class BystanderTower(Tower):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.raw_image = pygame.image.load('images/towers/tower_bystander.png').convert()
        self.image = pygame.transform.scale(
            self.raw_image,
            Settings.tower_bystander_size
        )


class MarshallTower(Tower):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.raw_image = pygame.image.load('images/towers/tower_marshall.png').convert()
        self.image = pygame.transform.scale(
            self.raw_image,
            Settings.tower_bystander_size
        )
