import utils
from mixins import MouseEventHandlerMixin
from vector import Vector
from settings import Settings
from flutter import Flutter


class Tile:
    def __init__(self):
        self.active = True
        self.grid_location = None
        self.location = None
        self.abstract_tile = None

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

    @property
    def is_empty(self):
        return self.abstract_tile.is_empty

    @property
    def image(self):
        return self.abstract_tile.image

    @property
    def value(self):
        return self.abstract_tile.value

    @property
    def is_coins(self):
        return self.abstract_tile.is_coins

    def set_location(self):
        self.location = utils.cell_to_isometric(self.grid_location) + self.abstract_tile.offset


class StaticTile(Tile):
    def __init__(self, abstract_tile, grid_location, canvas):
        super().__init__()
        self.abstract_tile = abstract_tile
        self.grid_location = grid_location
        self.set_location()
        self.canvas = canvas
        self.replacement_tile = None
        self.sparkle_countdown = 0

    @property
    def is_empty(self):
        return self.abstract_tile.is_empty and self.replacement_tile is None

    def draw(self):
        if self.sparkle_countdown:
            self.canvas.blit(self.abstract_tile.spark_image, self.location.as_list)
        else:
            self.canvas.blit(self.abstract_tile.image, self.location.as_list)

    def __repr__(self):
        return f'<StaticTile>(abstract_tile={self.abstract_tile}, grid_location={self.grid_location})'


class TowerTile(Tile, MouseEventHandlerMixin):
    def __init__(self, components, abstract_tile):
        Tile.__init__(self)
        self.abstract_tile = abstract_tile
        self.canvas = components.canvas
        self.components = components
        self.state = 'menu'  # menu, dragging, placed
        self.is_draggable = False
        self.location = self.abstract_tile.menu_location
        self.orientation = None
        self.supported = set()
        self.replaces = None

    def support_one_runner(self, runner):
        increase = runner.resource_levels[self.abstract_tile.type].top_up(Settings.resource_increase_by_tower)
        for i in range(int(increase)):
            runner.flutters.append(Flutter(self.abstract_tile.image_heart))
        self.supported.add(runner)

    def support_runners(self):
        if self.state == 'menu':
            return

        for runner in self.components.runners:
            if runner not in self.supported:
                if utils.next_door(runner.route[0].tile.grid_location, self.replaces.grid_location):
                    self.support_one_runner(runner)

    @property
    def is_active(self):
        return self.components.game.wealth >= self.abstract_tile.cost

    @property
    def image(self):
        if self.state == 'menu':
            if self.is_active:
                return self.abstract_tile.image_menu_active
            else:
                return self.abstract_tile.image_menu_inactive
        elif self.state == 'placed':
            return self.abstract_tile.images[self.orientation]

    def empty_tile_below_me(self):
        centre_x = self.location.x + int(self.image.get_width() / 2)
        centre_y = self.location.y + int(self.image.get_height() / 2)

        # TODO: Calculate grid location backwards - to speed this up
        for tile in self.components.static_tiles:
            if tile.is_empty and \
                (tile.location.x <= centre_x <= tile.location.x + tile.image.get_width()) and \
                (tile.location.y <= centre_y <= tile.location.y + tile.image.get_height()):
                return tile

    def draw(self):
        if self.state == 'menu':
            self.canvas.blit(self.abstract_tile.cost_text_active, self.abstract_tile.cost_location.as_int_list)

        if self.is_draggable:
            empty_tile = self.empty_tile_below_me()
            if empty_tile:
                self.canvas.blit(self.components.tile_selected_border_image, empty_tile.location.as_int_list)

        self.canvas.blit(self.image, self.location.as_int_list)

    def _is_mouse_event_for_me(self, event):
        if self.state is not 'menu' or not self.is_active:
            return False

        mouse_x, mouse_y = event.pos
        tower_x, tower_y = self.location

        return all([
            tower_x <= mouse_x <= (tower_x + self.image.get_width()),
            tower_y <= mouse_y <= (tower_y + self.image.get_height()),
        ])

    def _handle_mousemove(self, event):
        if self._is_mouse_event_for_me(event):
            if self.is_draggable:
                self.location += Vector(event.rel[0], event.rel[1])

    def _handle_mousedown(self, event):
        if self._is_mouse_event_for_me(event):
            self.is_draggable = True

            # TODO: This makes the tile transparent -
            #  but only if I .convert() the image first - and this loses the background transparency
            # self.image.set_alpha(100)

    def _handle_mouseup(self, event):
        if self.is_draggable:
            self.is_draggable = False
            empty_tile = self.empty_tile_below_me()
            if empty_tile:
                self.components.place_tower(self, empty_tile)
            else:
                self.location = self.abstract_tile.menu_location


        # TODO: Restore once background transparency is fixed - see above
        # self.image.set_alpha(255)
