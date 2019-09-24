class Settings:
    # To do: calculate these number
    scaling_factor = 0.7

    tile_size = (int(100 * scaling_factor), int(100 * scaling_factor))
    cell_width = int(88 * scaling_factor)
    cell_height = cell_width

    # To do: improve this
    canvas_width = 1000
    canvas_height = 700

    tiles_offset_x = 90
    tiles_offset_y = 310

    runner_size = (int(69 * scaling_factor), int(83 * scaling_factor))

    tower_bystander_size = (int(70 * scaling_factor), int(70 * scaling_factor))
    tower_marshall_size = tower_bystander_size
