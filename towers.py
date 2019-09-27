import pygame

from mixins import MouseEventHandlerMixin
from settings import Settings

from events import TowerEvent
import utils


class TowerType:
    def __init__(self, name, cost, canvas):
        self.name = name
        self.cost = cost
        self.canvas = canvas
        self.images = {
            f'{name}_{direction}': pygame.image.load(f'images/towers/{name}_{direction}.png')
            for direction in 'NESW'
        }
        self.font = pygame.font.SysFont('Arial', 32)
        self.cost_text_active = self.font.render(f'€{self.cost}', True, pygame.Color('yellow'))
        self.cost_text_inactive = self.font.render(f'€{self.cost}', True, pygame.Color('grey'))
        self.image_menu_active = self.images[f'{name}_E']
        self.image_menu_inactive = pygame.image.load(f'images/towers/{name}_E_grey.png')
        self.menu_location = utils.cell_to_isometric(Settings.menu_tower_locations[self.name])
        self.cost_location = utils.cell_to_isometric(
            (Settings.menu_tower_locations[self.name][0] + Settings.tower_cost_offset[0],
             Settings.menu_tower_locations[self.name][1] + Settings.tower_cost_offset[1])
        )

    def draw_menu_image(self, can_afford):
        image = self.image_menu_active if can_afford else self.image_menu_inactive
        location = utils.align_against_bottom(self.menu_location, image)
        self.canvas.blit(image, location)
        cost_image = self.cost_text_active if can_afford else self.cost_text_inactive
        self.canvas.blit(cost_image, self.cost_location)


class Tower(MouseEventHandlerMixin):
    def __init__(self, game, tower_type):
        self.tower_type = tower_type
        self.location = tower_type.menu_location
        self.game = game
        self.state = 'menu'  # menu, dragging, placed
        self.is_draggable = False

    def draw(self):
        if self.state == 'menu':
            self.tower_type.draw_menu_image(True)
        # self.game.canvas.blit(self.image, self.location)

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
                # self.game.canvas.blit(self.image, self.location)
                pygame.event.post(pygame.event.Event(
                    TowerEvent.TOWERMOTION,
                    {
                        "location": self.location,
                    }
                ))

    def _handle_mousedown(self, event):
        if self._is_mouse_event_for_me(event):
            self.is_draggable = True
            # self.image.set_alpha(100)
            pygame.event.post(pygame.event.Event(
                TowerEvent.TOWERDOWN,
                {
                    "location": self.location,
                }
            ))

    def _handle_mouseup(self, event):
        self.is_draggable = False
        # self.image.set_alpha(255)
        if self._is_mouse_event_for_me(event):
            pygame.event.post(pygame.event.Event(
                TowerEvent.TOWERUP,
                {
                    "location": self.location,
                }
            ))



# class BystanderTower(Tower):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.raw_image = pygame.image.load('images/towers/tower_bystander.png').convert()
#         self.image = pygame.transform.scale(
#             self.raw_image,
#             Settings.tower_bystander_size
#         )
#
#
# class MarshallTower(Tower):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.raw_image = pygame.image.load('images/towers/tower_marshall.png').convert()
#         self.image = pygame.transform.scale(
#             self.raw_image,
#             Settings.tower_bystander_size
#         )
