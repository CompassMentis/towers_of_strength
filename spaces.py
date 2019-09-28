import utils


class Space:
    def __init__(self, x, y, tile, canvas):
        self.x = x
        self.y = y
        self.tile = tile
        self.canvas = canvas
        self.location = utils.cell_to_isometric((x, y))

    def __repr__(self):
        return f'<Space>(x={self.x}, y={self.y})'

    @property
    def start_space(self):
        return self.tile.code in ['SPN', 'SPW']

    @property
    def end_space(self):
        return self.tile.code in ['FE', 'FN']

    @property
    def is_path(self):
        return self.tile.is_path

    def draw(self):
        self.canvas.blit(self.tile.image, (self.location[0], self.location[1] + self.tile.v_offset))

    @property
    def cell(self):
        return self.x, self.y
