import pygame

from settings import Settings
from vector import Vector
import utils


class AbstractTile:
    pass


class AbstractStaticTile(AbstractTile):
    IMAGE_FOLDER = 'static_tiles'

    def __init__(self, code, filename, with_sparkle=False):
        self.code = code
        self.filename = filename
        self.image = pygame.image.load(f'{Settings.image_folder}/{self.IMAGE_FOLDER}/{filename}.png')

        if with_sparkle:
            self.spark_image = pygame.image.load(f'{Settings.image_folder}/{self.IMAGE_FOLDER}/{filename}_sparkle.png')

        self.offset = Vector(0, Settings.tile_height - self.image.get_rect().height)

    @property
    def code_type(self):
        return self.code.split('_')[0]

    @property
    def direction(self):
        return self.code.split('_')[-1]

    @property
    def is_path(self):
        return self.code_type in ['CG', 'CS', 'C', 'F', 'S', 'L']

    @property
    def is_coins(self):
        return self.code_type in ['CG', 'CS']

    @property
    def value(self):
        if self.code_type == 'CG':
            return Settings.gold_value

        if self.code_type == 'CS':
            return Settings.silver_value

        return 0

    def __repr__(self):
        return f'<Tile>(code={self.code}, filename={self.IMAGE_FOLDER}/{self.filename})'

    @property
    def is_start(self):
        return self.code_type == 'SP'

    @property
    def is_end(self):
        return self.code_type == 'F'

    @property
    def is_empty(self):
        return self.code_type == 'O'


class AbstractTowerTile:
    def __init__(self, type):
        self.type = type
        self.cost = Settings.tower_costs[type]

        self.images = {
            f'{direction}': pygame.image.load(f'images/tower_tiles/{type}_{direction}.png')
            for direction in 'NESW'
        }

        self.font = pygame.font.SysFont('Arial', 24)
        self.cost_text_active = self.font.render(f'({self.cost})', True, pygame.Color('yellow'))
        self.cost_text_inactive = self.font.render(f'({self.cost})', True, pygame.Color('grey'))
        self.image_menu_active = pygame.image.load(f'images/tower_tiles/{type}_menu.png')
        self.image_menu_inactive = pygame.image.load(f'images/tower_tiles/{type}_menu_grey.png')
        self.image_heart = pygame.image.load(f'images/misc/heart_{type}.png')

        self.menu_location = utils.cell_to_isometric(Settings.menu_tower_locations[type]) + \
            Vector(0, Settings.tile_height - self.image_menu_active.get_rect().height)

        self.cost_location = utils.cell_to_isometric(
            Settings.menu_tower_locations[type] + Settings.tower_cost_offset
        )

        self.offset = Vector(0, Settings.tile_height - self.images['E'].get_rect().height)
