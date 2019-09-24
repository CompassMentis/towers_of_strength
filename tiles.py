import pygame
import glob

from settings import Settings


class Tile:
    def __init__(self, code, filename):
        self.code = code
        self.filename = filename
        self.image = pygame.image.load(f'images/tiles/{filename}.png')
        self.v_offset = Settings.tile_height - self.image.get_rect().height

    @property
    def is_path(self):
        for x in ['corner', 'straight', 'crossing']:
            if x in self.filename:
                return True
        return False


def load_tiles():
    sources = {
        'ES/SE': 'tile_cornerRound_E',
        'EN/NE': 'tile_cornerRound_N',
        'SW/WS': 'tile_cornerRound_S',
        'NW/WN': 'tile_cornerRound_W',
        'SPN': 'tile_endRoundSpawn_E',
        'T': 'tile_E',
        'NS/SN': 'tile_straight_E',
        'EW/WE': 'tile_straight_N',
        'NESW': 'tile_crossing_E',

        # TODO: Create base/finish tile
        'BS': 'tile_finish',

        # Empty tile
        'H': 'tile_hole',
    }
    tiles = dict()
    for codes, filename in sources.items():
        for code in codes.split('/'):
            # A bit wasteful - we're loading the same image multiple times
            tiles[code] = Tile(code, filename)

    for i in range(1, 4):
        code = f'X{i}'
        tiles[code] = Tile(code, f'tile_terrain0{i}')

    return tiles
