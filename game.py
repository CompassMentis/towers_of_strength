import pygame
import random
import datetime
import time

from tiles import StaticTile, TowerTile
from settings import Settings
from steps import Step
import utils


from components import Components
from vector import Vector


class Game:
    def __init__(self, canvas):

        self.canvas = canvas
        self.font = pygame.font.SysFont('Arial', 48)

        self.components = None
        self.route = None
        self.wealth = 100
        self.score = 0
        self.start_time = None
        self.level_name = ''

        self.levels = ['level01', 'level02', 'level03']
        self.start_level(self.levels[0])

    def next_level(self):
        del self.levels[0]
        self.start_level(self.levels[0])

    def score_point(self):
        self.score += 1
        if self.score >= Settings.target_score:
            self.draw()
            time.sleep(2)
            self.next_level()

    def start_level(self, level):
        self.components = Components(self, level)

        self.route = self.calculate_route()
        self.components.new_runner(self)
        self.level_name = f'Level {level[5:]}'
        self.wealth = 100
        self.score = 0
        self.start_time = datetime.datetime.now()

    @property
    def time(self):
        duration = datetime.datetime.now() - self.start_time
        minutes, seconds = divmod(duration.seconds, 60)
        return f'{minutes}:{seconds:02}'

    @property
    def runners(self):
        return self.components.runners

    def handle_mouse_event(self, event):
        self.components.handle_mouse_event(event)

    def show_wealth(self):
        self.canvas.blit(
            self.font.render(f'{self.wealth}', True, pygame.Color('yellow')),
            utils.cell_to_isometric(Settings.wealth_location).as_int_list
        )

    def show_score(self):
        self.canvas.blit(
            self.font.render(f'{self.score}/{Settings.target_score}', True, pygame.Color('white')),
            utils.cell_to_isometric(Settings.score_location).as_int_list
        )

    def show_time(self):
        time = self.time
        self.canvas.blit(
            self.font.render(time, True, pygame.Color('white')),
            utils.cell_to_isometric(Settings.time_location).as_int_list
        )

    def show_level_name(self):
        self.canvas.blit(
            self.font.render(self.level_name, True, pygame.Color('white')),
            utils.cell_to_isometric(Settings.level_name_location).as_int_list
        )

    def draw(self):
        # TODO: Create background image
        self.canvas.fill((0, 0, 0))

        self.components.draw()

        self.show_wealth()
        self.show_score()
        self.show_time()
        self.show_level_name()

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
        next_tile = self.components.filter(type=StaticTile, grid_location=next_location)[0]
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
        for tile in self.components.filter(type=TowerTile):
            tile.support_runners()
