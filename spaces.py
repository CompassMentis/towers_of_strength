from settings import Settings


class Space:
    def __init__(self, x, y, tile):
        self.x = x
        self.y = y
        self.tile = tile
        self.location = self.calculate_location()

    def calculate_location(self):
        """
        The whole grid is rotated clockwise by 45 degrees

        Multiply by cell size
        x2 = x * cell_width
        y2 = y * cell_height

        Top left hand corner of cell (0, 0), i.e. pre-rotated coordinate (0, 0)
        is the rotation point

        For 45 degrees this means:

        x'' = x2/2 - y2/2
        y'' = y2/2 - x2/2
        """

        x2 = self.x * Settings.cell_width
        y2 = self.y * Settings.cell_height

        return x2 / 2 - y2 / 2, y2 / 2 - x2 / 2


def create_spaces(level, tiles):
    # We're reading a csv file, but the format is so simple
    # that we don't really need python's csv library
    with open(f'levels/{level}.csv') as input_file:
        lines = input_file.readlines()

    result = dict()

    for row, line in enumerate(lines):
        for column, tile_code in enumerate(line.split(',')):
            tile_code = tile_code.strip()   # Remove EOL character
            result[(column, row)] = Space(column, row, tiles[tile_code])
    return result
