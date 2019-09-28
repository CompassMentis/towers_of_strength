from settings import Settings
from vector import Vector


def cell_to_isometric(cell):
    """
    The whole grid is rotated clockwise by 45 degrees

    Multiply by cell size
    x2 = x * cell_width
    y2 = y * cell_height

    Top left hand corner of cell (0, 0), i.e. pre-rotated coordinate (0, 0)
    is the rotation point

    For 45 degrees this means:

    x'' = x2/2 - y2/2
    y'' = y2/2 - x2/2
    """
    return location_to_isometric((cell.x * Settings.cell_width, cell.y * Settings.cell_height))


def location_to_isometric(location):
    x2, y2 = location
    # Not sure why, but the factors needed a bit tweaking to match up the tiles correctly
    return Vector(x2 * 0.666 + y2 * 0.666 + Settings.tiles_offset_x,
                  x2 * -0.333 + y2 * 0.333 + Settings.tiles_offset_y)


def align_against_bottom(menu_location, image):
    return (
        menu_location[0],
        menu_location[1] + Settings.tile_height - image.get_rect().height
    )


def next_door(grid_location_1, grid_location_2):
    return abs(grid_location_1 - grid_location_2) in [Vector(0, 1), Vector(1, 0)]
