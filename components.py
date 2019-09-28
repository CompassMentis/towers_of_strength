import pygame

from abstract_tiles import AbstractStaticTile, AbstractTile
from tiles import StaticTile, Tile
from vector import Vector
from spritesheet import SpriteSheet
from runners import ResourceType, Runner
# from towers import TowerType


class Components:
    def __init__(self, canvas, level):
        self.canvas = canvas

        self.abstract_static_tiles = self.load_abstract_static_tiles()
        self.abstract_tiles = list(self.abstract_static_tiles.values())

        self.terrain_tiles, self.grid_size = self.load_terrain(level, canvas)
        self.static_tiles = self.terrain_tiles
        self.tiles = self.static_tiles

        self.spritesheets = [
            SpriteSheet(
                f'images/runners/{name}_animated.png',
                columns=32, rows=8,
                colour_key=pygame.Color(127, 127, 127)
            )
            for name in ['hero', 'heroine']
        ]

        self.resource_types = {
            colour: ResourceType(colour, offset, self.canvas)
            for colour, offset in [
                ('red', Vector(58, 45)),
                ('yellow', Vector(60, 40)),
                ('blue', Vector(62, 43))
            ]
        }

        self.runners = []

        # self.tower_types = {
        #     resource: TowerType(resource, cost, self.canvas)
        #     for cost, resource in [
        #         (70, 'hydration'),
        #         (80, 'nutrition'),
        #         (100, 'supporters')
        #     ]
        # }

        self.all = self.abstract_tiles + self.static_tiles

    def new_runner(self, game):
        self.runners.append(Runner(game))

    @staticmethod
    def load_abstract_static_tiles():
        sources = {
            'O': 'open',
        }
        for code, tile_type in [
            ['CG', 'coins_gold'],
            ['CS', 'coins_silver'],
            ['F', 'finish'],
            ['S', 'straight']
        ]:
            for orientation in ['NS', 'EW']:
                sources[f'{code}_{orientation}'] = f'{tile_type}_{orientation}'

        for orientation in 'NESW':
            sources[f'SP_{orientation}'] = f'spawn_{orientation}'

        for orientation in ['NE', 'NW', 'SE', 'SW']:
            sources[f'C_{orientation}'] = f'corner_{orientation}'

        for id in range(1, 6):
            sources[f'T_0{id}'] = f'terrain_0{id}'

        return {
            code: AbstractStaticTile(code, filename)
            for code, filename in sources.items()
        }

    def load_terrain(self, level, canvas):
        # We're reading a csv file, but the format is so simple
        # that we don't really need python's csv library
        with open(f'levels/{level}.csv') as input_file:
            lines = input_file.readlines()

        tiles = []

        rows, columns = 0, 0
        for row, line in enumerate(lines):
            rows = max(row, rows)
            for column, tile_code in enumerate(line.split(',')):
                columns = max(column, columns)
                tiles.append(
                    StaticTile(
                        self.abstract_static_tiles[tile_code.strip()],
                        Vector(column, row),
                        canvas
                    )
                )
        return tiles, Vector(columns + 1, rows + 1)

    @property
    def grid_spaces(self):
        for x in range(self.grid_size.width - 1, 0, -1):
            for y in range(self.grid_size.height):
                yield Vector(x, y)

    def filter(self, type=None, grid_location=None, neighbour=None):
        result = {
            None: self.all,
            AbstractStaticTile: list(self.abstract_static_tiles.values()),
            AbstractTile: self.abstract_tiles,
            StaticTile: self.static_tiles,
            Tile: self.tiles
        }[type]

        if grid_location:
            result = [
                component
                for component in result
                if component.grid_location == grid_location
            ]

        if neighbour:
            result = [
                component
                for component in result
                if abs(component.grid_location - neighbour.grid_location) in [Vector(0, 1), Vector(1, 0)]
            ]

        return result
