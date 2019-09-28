import utils


class Tile:
    def draw(self):
        raise NotImplementedError

    @property
    def is_path(self):
        return self.abstract_tile.is_path

    @property
    def code(self):
        return self.abstract_tile.code

    @property
    def direction(self):
        return self.abstract_tile.direction


class StaticTile(Tile):
    def __init__(self, abstract_tile, grid_location, canvas):
        self.abstract_tile = abstract_tile
        self.grid_location = grid_location
        self.location = utils.cell_to_isometric(self.grid_location) + self.abstract_tile.offset
        self.canvas = canvas

    def draw(self):
        self.canvas.blit(self.abstract_tile.image, self.location.as_list)

    def __repr__(self):
        return f'<StaticTile>(abstract_tile={self.abstract_tile}, grid_location={self.grid_location})'
