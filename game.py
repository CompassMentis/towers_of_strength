import pygame

from tiles import load_tiles
from spaces import create_spaces


class Game:
    def __init__(self, canvas):
        self.tiles = load_tiles()
        self.canvas = canvas

        # Level hardcoded for now, may support multiple levels later
        self.spaces = create_spaces('level01', self.tiles, self.canvas)

    def draw(self):
        # TODO: Create background image
        self.canvas.fill((0, 0, 0))

        for x, y in sorted(self.spaces, key=lambda xy: (-xy[0], xy[1])):
        # for space in self.spaces.values():
            space = self.spaces[(x, y)]
            space.draw()

        pygame.display.flip()