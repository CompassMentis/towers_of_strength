import pygame

from tiles import load_tiles
from spaces import create_spaces
from runners import Runner


class Game:
    def __init__(self, canvas):
        self.tiles = load_tiles()
        self.canvas = canvas
        self._start_tile = None

        # Level hardcoded for now, may support multiple levels later
        self.spaces = create_spaces('level01', self.tiles, self.canvas)
        self.grid_size = self.calculate_grid_size()
        self.start_space = self.find_start_space()
        self.route = self.calculate_route()
        print(self.route)
        self.runners = [Runner(self)]

    def calculate_grid_size(self):
        max_x, max_y = 0, 0
        for x, y in self.spaces:
            max_x = max(max_x, x)
            max_y = max(max_y, y)
        return max_x, max_y

    def draw(self):
        # TODO: Create background image
        self.canvas.fill((0, 0, 0))

        for x, y in sorted(self.spaces, key=lambda xy: (-xy[0], xy[1])):
            space = self.spaces[(x, y)]
            space.draw()

        for runner in self.runners:
            runner.draw()

        pygame.display.flip()

    def find_start_space(self):
        for space in self.spaces.values():
            if space.start_space:
                return space

    def neighbours(self, x, y):
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if 0 <= i < self.grid_size[0] and 0 <= j < self.grid_size[1]:
                    yield i, j

    def find_next_path_space(self, space, route):
        x, y = space.x, space.y
        for i, j in self.neighbours(x, y):
            if self.spaces[(i, j)] not in route and self.spaces[(i, j)].is_path:
                return self.spaces[(i, j)]
        return None

    def calculate_route(self):
        route = []
        current = self.start_space
        while current is not None:
            route.append(current)
            current = self.find_next_path_space(current, route)

        return route

    def tick(self):
        for runner in self.runners:
            runner.to_next_tile()
