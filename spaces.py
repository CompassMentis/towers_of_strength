from settings import Settings
import utils


class Space:
    def __init__(self, x, y, tile, canvas):
        self.x = x
        self.y = y
        self.tile = tile
        self.canvas = canvas
        # self.location = self.calculate_location()
        self.location = utils.cell_to_isometric((x, y))

    def __repr__(self):
        return f'<Space>(x={self.x}, y={self.y})'

    @property
    def start_space(self):
        return self.tile.code in ['SPN', 'SPW']

    @property
    def end_space(self):
        return self.tile.code == 'BS'

    @property
    def is_path(self):
        return self.tile.is_path

    def draw(self):
        self.canvas.blit(self.tile.image, (self.location[0], self.location[1] + self.tile.v_offset))

    @property
    def cell(self):
        return self.x, self.y


def create_spaces(level, tiles, canvas):
    # We're reading a csv file, but the format is so simple
    # that we don't really need python's csv library
    with open(f'levels/{level}.csv') as input_file:
        lines = input_file.readlines()

    result = dict()

    for row, line in enumerate(lines):
        for column, tile_code in enumerate(line.split(',')):
            tile_code = tile_code.strip()   # Remove EOL character
            result[(column, row)] = Space(column, row, tiles[tile_code], canvas)
    return result
