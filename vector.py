class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __mul__(self, other):
        return Vector(other * self.x, other * self.y)

    def __iter__(self):
        return iter(self.as_list)

    @property
    def width(self):
        return self.x

    @property
    def height(self):
        return self.y

    @property
    def as_list(self):
        return [self.x, self.y]

    @property
    def as_int_list(self):
        return [int(self.x), int(self.y)]

    @property
    def as_tuple(self):
        return self.x, self.y

    def __abs__(self):
        return Vector(abs(self.x), abs(self.y))

    def __repr__(self):
        return f'<Vector>(x={self.x}, y={self.y})'
