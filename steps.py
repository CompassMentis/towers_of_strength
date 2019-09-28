class Step:
    def __init__(self, grid_location, entry_side, exit_side, tile):
        self.grid_location = grid_location
        # self.x = x
        # self.y = y
        self.entry_side = entry_side
        self.exit_side = exit_side
        self.tile = tile

    def __repr__(self):
        return f'<Step>(grid_location={self.grid_location}, entry={self.entry_side}, exit={self.exit_side}, tile={self.tile})'
