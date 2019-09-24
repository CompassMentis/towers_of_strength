class Step:
    def __init__(self, x, y, entry_side, exit_side):
        self.x = x
        self.y = y
        self.entry_side = entry_side
        self.exit_side = exit_side

    def __repr__(self):
        return f'<Step>(x={self.x}, y={self.y}, entry={self.entry_side}, exit={self.exit_side})'
