import pygame

from settings import Settings
from vector import Vector


class AbstractTile:
    pass


class AbstractStaticTile(AbstractTile):
    IMAGE_FOLDER = 'static_tiles'

    def __init__(self, code, filename):
        self.code = code
        self.filename = filename
        self.image = pygame.image.load(f'{Settings.image_folder}/{self.IMAGE_FOLDER}/{filename}.png')

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

    def __repr__(self):
        return f'<Tile>(code={self.code}, filename={self.IMAGE_FOLDER}/{self.filename})'

    @property
    def is_start(self):
        return self.code_type == 'SP'

    @property
    def is_end(self):
        return self.code_type == 'F'
