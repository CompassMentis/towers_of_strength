from settings import Settings


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

    x, y = cell

    return location_to_isometric((x * Settings.cell_width, y * Settings.cell_height))


def location_to_isometric(location):
    x2, y2 = location
    # Not sure why, but the factors needed a bit tweaking to match up the tiles correctly
    return x2 * 0.666 + y2 * 0.666 + Settings.tiles_offset_x, \
           x2 * -0.333 + y2 * 0.333 + Settings.tiles_offset_y
