import pygame

from settings import Settings


class Tile:
    def __init__(self, code, filename):
        self._code = code
        self.filename = filename
        self.image = pygame.image.load(f'images/tiles/{filename}.png')

        # TODO: Replace with call to: utils.align_against_bottom(self.menu_location, image) ??
        self.v_offset = Settings.tile_height - self.image.get_rect().height

    @property
    def code(self):
        if len(self._code) == 3 and self._code[:2] in ['NS', 'SN', 'WE', 'EW']:
            return self._code[:2]

        return self._code

    @property
    def is_path(self):
        if self.code in ['FE', 'FN']:
            return True
        for x in ['corner', 'straight', 'crossing', 'coin']:
            if x in self.filename:
                return True
        return False

    def __repr__(self):
        return f'<Tile>(code={self.code}, filename={self.filename})'


def load_tiles():
    sources = {
        'ES/SE': 'tile_cornerRound_E',
        'EN/NE': 'tile_cornerRound_N',
        'SW/WS': 'tile_cornerRound_S',
        'NW/WN': 'tile_cornerRound_W',
        'SPN': 'tile_endRoundSpawn_E',
        'SPW': 'tile_endRoundSpawn_N',
        'T': 'tile_E',
        'NS/SN': 'tile_straight_E',
        'EW/WE': 'tile_straight_N',
        'NESW': 'tile_crossing_E',
        'NSG/SNG': 'tile_coin_gold_N',
        'NSS/SNS': 'tile_coin_silver_N',
        'EWG/WEG': 'tile_coin_gold_E',
        'EWS/WES': 'tile_coin_silver_E',

        'FN': 'tile_finish_N',
        'FE': 'tile_finish_E',

        # Empty tile
        'H': 'tile_hole',
    }
    tiles = dict()
    for codes, filename in sources.items():
        for code in codes.split('/'):
            # A bit wasteful - we're loading the same image multiple times
            tiles[code] = Tile(code, filename)

    for i in range(1, 6):
        code = f'X{i}'
        tiles[code] = Tile(code, f'tile_terrain0{i}')

    return tiles
