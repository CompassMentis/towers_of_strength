import pygame

from mixins import MouseEventHandlerMixin
from settings import Settings

from events import TowerEvent

class Tower(MouseEventHandlerMixin):
    def __init__(self, location, game):
        self.location = location
        self.game = game
        self.raw_image = None
        self.image = None
        self.is_draggable = False


    def draw(self):
        self.game.canvas.blit(self.image, self.location)


    def _is_mouse_event_for_me(self, event):
        mouse_x, mouse_y = event.pos
        tower_x, tower_y = self.location

        return all([
            tower_x <= mouse_x <= (tower_x + self.image.get_width()),
            tower_y <= mouse_y <= (tower_y + self.image.get_height()),
        ])

    def _handle_mousemove(self, event):
        if self._is_mouse_event_for_me(event):
            if self.is_draggable:
                self.location = (
                    self.location[0] + event.rel[0],
                    self.location[1] + event.rel[1],
                )
                self.game.canvas.blit(self.image, self.location)
                pygame.event.post(pygame.event.Event(
                    TowerEvent.TOWERMOTION,
                    {
                        "location": self.location,
                    }
                ))


    def _handle_mousedown(self, event):
        if self._is_mouse_event_for_me(event):
            self.is_draggable = True
            self.image.set_alpha(100)
            pygame.event.post(pygame.event.Event(
                TowerEvent.TOWERDOWN,
                {
                    "location": self.location,
                }
            ))


    def _handle_mouseup(self, event):
        self.is_draggable = False
        self.image.set_alpha(255)
        if self._is_mouse_event_for_me(event):
            pygame.event.post(pygame.event.Event(
                TowerEvent.TOWERUP,
                {
                    "location": self.location,
                }
            ))


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
