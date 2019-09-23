import pygame

from settings import Settings


class Tile:
    def __init__(self, filename):
        self.raw_image = pygame.image.load(f'images/tiles/{filename}.png')
        self.image = pygame.transform.scale(
            self.raw_image,
            # pygame.transform.rotate(self.raw_image, -45),
            Settings.tile_size
        )


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
        'BS': 'tile_E',
    }
    tiles = dict()
    for codes, filename in sources.items():
        tile = Tile(filename)
        for code in codes.split('/'):
            tiles[code] = tile
    return tiles

