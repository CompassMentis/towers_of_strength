import pygame
import random
from spritesheet import SpriteSheet

from tiles import load_tiles
from spaces import create_spaces
from runners import Runner
from towers import BystanderTower, MarshallTower
from steps import Step


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
        self.spritesheets = [
            SpriteSheet(
                f'images/runners/{name}_animated.png',
                columns=32, rows=8,
                colour_key=pygame.Color(127, 127, 127)
            )
            for name in ['hero', 'heroine']
        ]
        self.runners = [Runner(self)]

        self.towers = [
            # TODO Tower locations hard-coded - load from file?
            BystanderTower((1,1), self),
            MarshallTower((1, 80), self),
        ]

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

        for tower in self.towers:
            tower.draw()

        pygame.display.flip()

    def find_start_space(self):
        for space in self.spaces.values():
            if space.start_space:
                return space

    def neighbours(self, x, y):
        for i, j in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
            if 0 <= i < self.grid_size[0] and 0 <= j < self.grid_size[1]:
                yield i, j

    def find_neighbour_path(self, space):
        x, y = space.x, space.y
        for i, j in self.neighbours(x, y):
            if self.spaces[(i, j)].is_path:
                return self.spaces[(i, j)]
        return None

    def find_next_step(self, step):
        if self.spaces[(step.x, step.y)].end_space:
            return None

        delta = {
            'E': (1, 0),
            'S': (0, 1),
            'W': (-1, 0),
            'N': (0, -1)
        }[step.exit_side]
        next_x, next_y = step.x + delta[0], step.y + delta[1]
        next_tile = self.spaces[(next_x, next_y)].tile
        print(next_x, next_y, next_tile)
        assert next_tile.is_path

        next_entry_side = {
            'E': 'W',
            'W': 'E',
            'N': 'S',
            'S': 'N'
        }[step.exit_side]

        if next_tile.code in ['NESW', 'NS', 'SN', 'EW', 'WE']:
            # Can move in a straight line
            next_exit_side = step.exit_side
        else:
            # Take code (consisting in entry + exit side, but may be in wrong order)
            # remove the entry side, to be left with the exit side
            next_exit_side = [c for c in next_tile.code if c is not next_entry_side][0]

        return Step(next_x, next_y, next_entry_side, next_exit_side)

    def calculate_route(self):
        route = []
        start_space = self.start_space
        next_space = self.find_neighbour_path(start_space)
        delta_to_next = (next_space.x - start_space.x, next_space.y - start_space.y)
        exit_side = {
            (1, 0): 'E',
            (0, 1): 'S',
            (-1, 0): 'W',
            (0, -1): 'N'
        }[delta_to_next]

        step = Step(x=start_space.x, y=start_space.y, entry_side=None, exit_side=exit_side)

        while step is not None:
            route.append(step)
            step = self.find_next_step(step)

        print(route)
        return route

    def tick(self):
        if random.randint(1, 100) == 1:
            self.runners.append(Runner(self))
        for runner in self.runners:
            runner.take_a_step()
