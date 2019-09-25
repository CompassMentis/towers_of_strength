import pygame
import random
from spritesheet import Origin

import utils


class Runner:
    def __init__(self, game):
        self.game = game
        self.sprites = random.choice(game.spritesheets)

        self.route = self.game.route[:]
        self.location = None
        self.happiness = 3
        self.hydration = 6
        self.energy = 6
        self.progress_on_tile = 0.5  # Start half way along the first tile
        self.step_size = 0.03  # Initial speed: 10 steps to cross a tile
        self.set_location()
        self.direction = 0

    def draw(self):
        running_step = int(8 * self.progress_on_tile)
        self.sprites.blit(self.game.canvas, self.direction * 32 + running_step + 4, position=self.location, origin=Origin.TopLeft)

    def offset_and_direction_on_tile(self):
        step = self.route[0]

        side_locations = {
            'N': (0.5, 0),
            'E': (1, 0.5),
            'S': (0.5, 1),
            'W': (0, 0.5),
            'C': (0.5, 0.5)
        }
        entry_point = side_locations['C'] if step.entry_side is None else side_locations[step.entry_side]
        exit_point = side_locations['C'] if step.exit_side is None else side_locations[step.exit_side]

        delta = exit_point[0] - entry_point[0], exit_point[1] - entry_point[1]

        offset = entry_point[0] + self.progress_on_tile * delta[0], entry_point[1] + self.progress_on_tile * delta[1]

        delta_x, delta_y = delta
        delta_x = 2 * delta_x if abs(delta_x) == 0.5 else delta_x
        delta_y = 2 * delta_y if abs(delta_y) == 0.5 else delta_y

        direction = {-1: 'W', 0: '', 1: 'E'}[delta_x] + {-1: 'N', 0: '', 1: 'S'}[delta_y]
        direction = {
            'W': 0,
            'WN': 1,
            'N': 2,
            'EN': 3,
            'E': 4,
            'ES': 5,
            'S': 6,
            'WS': 7
        }[direction]
        direction = (direction - 1) % 8

        return offset, direction

    def set_location(self):
        offset, direction = self.offset_and_direction_on_tile()
        self.location = utils.cell_to_isometric((self.route[0].x + offset[0] + 0.9, self.route[0].y + offset[1] - 2.3))
        self.direction = direction

    def take_a_step(self):
        self.progress_on_tile += self.step_size
        if self.progress_on_tile >= 1:
            self.progress_on_tile -= 1
            self.to_next_tile()
        self.set_location()

    @property
    def on_last_tile(self):
        return len(self.route) <= 1

    def to_next_tile(self):
        if self.on_last_tile:
            return
        del self.route[0]
