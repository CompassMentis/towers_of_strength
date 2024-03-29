from vector import Vector


class Settings:
    cell_width = 63
    cell_height = 63

    canvas_width = 1020
    canvas_height = 700

    tiles_offset_x = 2
    tiles_offset_y = 310

    tile_height = 56
    tile_width = 91

    clock_speed = 30  # 30 frames per second

    resource_increase_by_tower = 3
    resource_depletion_per_step = 0.01
    leaving_progress_per_step = 0.1
    leaving_left = 6

    menu_tower_locations = {
        'nutrition': Vector(-1.5, 6),
        'hydration': Vector(-1.5, 3),
        'supporters': Vector(-1.5, 4.5)
    }

    tower_costs = {
        'nutrition': 50,
        'hydration': 40,
        'supporters': 60
    }

    tower_cost_offset = Vector(-1.5, 0.5)

    image_folder = 'images'

    wealth_location = Vector(-5, 5)

    gold_value = 10
    silver_value = 5
    sparkle_duration = 20

    score_location = Vector(5, 16)
    time_location = Vector(3, 18)

    target_score = 15

    level_name_location = Vector(16, 3)
