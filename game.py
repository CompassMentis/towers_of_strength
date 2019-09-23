from tiles import load_tiles
from spaces import create_spaces


class Game:
    def __init__(self):
        self.tiles = load_tiles()

        # Level hardcoded for now, may support multiple levels later
        self.spaces = create_spaces('level01', self.tiles)
