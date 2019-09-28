import random
import pygame
from spritesheet import Origin

import utils
from settings import Settings
from vector import Vector


class ResourceType:
    def __init__(self, colour, offset, canvas):
        self.colour = colour
        self.offset = offset
        self.canvas = canvas

    def draw(self, location):
        pygame.draw.circle(self.canvas, pygame.Color(self.colour), (location + self.offset).as_int_list, 4)


class ResourceLevel:
    def __init__(self, starting_level, resource_type):
        self.level = starting_level
        self.resource_type = resource_type
        self.leaving = False
        self.leaving_progress = 0
        self.left = False

    def start_leaving(self):
        self.leaving = True
        self.leaving_progress = 0

    def top_up(self, amount):
        self.leaving_progress = 0
        self.leaving = False
        self.level += amount

    def decrease(self):
        if self.leaving:
            self.leaving_progress += Settings.leaving_progress_per_step
            if self.leaving_progress >= Settings.leaving_left:
                self.left = True
            return
        self.level -= Settings.resource_depletion_per_step
        if self.level <= 0:
            self.start_leaving()

    def draw(self, location):
        if not self.critical or self.leaving:
            return
        self.resource_type.draw(location)

    @property
    def critical(self):
        return self.level <= 2

    @property
    def depleted(self):
        return self.level <= 0


class Runner:
    def __init__(self, game):
        self.game = game
        self.sprites = random.choice(game.components.spritesheets)

        self.route = self.game.route[:]
        self.location = None
        self.resource_levels = {
            colour: ResourceLevel(starting_level, game.components.resource_types[colour])
            for colour, starting_level in [
                ('red', 3),
                ('blue', 6),
                ('yellow', 6)
            ]
        }
        self.progress_on_tile = 0.5  # Start half way along the first tile
        self.step_size = 0.03 + 0.01 * random.randint(0, 3)
        self.set_location()
        self.direction = 0
        self.present = True

    def draw_circle(self, offset, colour):
        pygame.draw.circle(self.game.canvas, pygame.Color(colour),
                           (int(self.location[0] + offset[0]), int(self.location[1] + offset[1])), 4)

    @property
    def leaving(self):
        return any(r.leaving for r in self.resource_levels.values())

    @property
    def leaving_step(self):
        return int(max(r.leaving_progress for r in self.resource_levels.values() if r.leaving))

    @property
    def slow(self):
        return any(r.critical for r in self.resource_levels.values())

    @property
    def left(self):
        return any(r.left for r in self.resource_levels.values())

    def draw(self):
        if not self.present:
            return

        if self.leaving:
            # Falling 18 - 23
            running_step = self.leaving_step + 18
        else:
            running_step = int(8 * self.progress_on_tile) + 4
        self.sprites.blit(self.game.canvas, self.direction * 32 + running_step, position=self.location, origin=Origin.TopLeft)
        for resource_level in self.resource_levels.values():
            resource_level.draw(self.location)

    def offset_and_direction_on_tile(self):
        step = self.route[0]

        side_locations = {
            'N': Vector(0.5, 0),
            'E': Vector(1, 0.5),
            'S': Vector(0.5, 1),
            'W': Vector(0, 0.5),
            'C': Vector(0.5, 0.5)
        }
        entry_point = side_locations['C'] if step.entry_side is None else side_locations[step.entry_side]
        exit_point = side_locations['C'] if step.exit_side is None else side_locations[step.exit_side]

        delta = exit_point - entry_point

        offset = entry_point + delta * self.progress_on_tile

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
        self.location = utils.cell_to_isometric(self.route[0].grid_location + offset + Vector(0.9, -2.3))
        self.direction = direction

    def take_a_step(self):
        if not self.present:
            return
        if not self.leaving:
            if self.slow:
                self.progress_on_tile += self.step_size / 2
            else:
                self.progress_on_tile += self.step_size
            if self.progress_on_tile >= 1:
                self.progress_on_tile -= 1
                self.to_next_tile()
        self.set_location()
        for resource_level in self.resource_levels.values():
            resource_level.decrease()
        if self.left:
            self.present = False

    @property
    def on_last_tile(self):
        return len(self.route) <= 1

    def to_next_tile(self):
        if self.on_last_tile:
            return
        del self.route[0]
