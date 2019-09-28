import pygame
import random

from tiles import StaticTile
# from towers import BystanderTower, MarshallTower
# from towers import TowerType, Tower
from steps import Step


from components import Components
from vector import Vector


class Game:
    def __init__(self, canvas):

        self.canvas = canvas
        self.components = Components(canvas, 'level01')

        self.route = self.calculate_route()
        self.components.new_runner(self)
        # self.towers = [Tower(tower_type=tower_type, game=self) for tower_type in self.tower_types.values()]
        #

        # self.towers = [
        #     # TODO Tower locations hard-coded - load from file?
        #     BystanderTower((1,1), self),
        #     MarshallTower((1, 80), self),
        # ]

    @property
    def runners(self):
        return self.components.runners

    def draw(self):
        # TODO: Create background image
        self.canvas.fill((0, 0, 0))

        for static_tile in sorted(
            self.components.filter(type=StaticTile),
            key=lambda tile: (-tile.grid_location.x, tile.grid_location.y)
        ):
            static_tile.draw()

        for runner in self.components.runners:
            runner.draw()
        #
        # for tower in self.towers:
        #     tower.draw()
        #
        pygame.display.flip()

    def find_start_tile(self):
        for tile in self.components.filter(type=StaticTile):
            if tile.abstract_tile.is_start:
                return tile

    def neighbours(self, x, y):
        for i, j in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
            if 0 <= i < self.grid_size[0] and 0 <= j < self.grid_size[1]:
                yield i, j

    def find_neighbour_tile_on_path(self, tile):
        for tile in self.components.filter(type=StaticTile, neighbour=tile):
            if tile.abstract_tile.is_path:
                return tile

    def find_next_step(self, step):
        if step.tile.abstract_tile.is_end:
            return None

        delta = {
            'E': Vector(1, 0),
            'S': Vector(0, 1),
            'W': Vector(-1, 0),
            'N': Vector(0, -1)
        }[step.exit_side]
        next_location = step.grid_location + delta
        # next_x, next_y = step.x + delta[0], step.y + delta[1]
        next_tile = self.components.filter(type=StaticTile, grid_location=next_location)[0]
        # next_tile = self.spaces[(next_x, next_y)].tile
        assert next_tile.is_path

        next_entry_side = {
            'E': 'W',
            'W': 'E',
            'N': 'S',
            'S': 'N'
        }[step.exit_side]

        if next_tile.direction in ['EW', 'NS']:
            # Can move in a straight line
            next_exit_side = step.exit_side
        else:
            # Take code (consisting in entry + exit side, but may be in wrong order)
            # remove the entry side, to be left with the exit side
            next_exit_side = [c for c in next_tile.direction if c is not next_entry_side][0]

        return Step(next_location, next_entry_side, next_exit_side, next_tile)

    def calculate_route(self):
        route = []
        start_tile = self.find_start_tile()
        next_tile = self.find_neighbour_tile_on_path(start_tile)
        delta_to_next = next_tile.grid_location -start_tile.grid_location
        exit_side = {
            (1, 0): 'E',
            (0, 1): 'S',
            (-1, 0): 'W',
            (0, -1): 'N'
        }[delta_to_next.as_tuple]

        step = Step(grid_location=start_tile.grid_location, entry_side=None, exit_side=exit_side, tile=start_tile)

        while step is not None:
            route.append(step)
            step = self.find_next_step(step)

        return route

    def tick(self):
        if random.randint(1, 100) == 1:
            self.components.new_runner(self)
        for runner in self.runners:
            runner.take_a_step()
