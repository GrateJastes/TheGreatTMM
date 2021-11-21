from .Dot import AnalogDot


class Path:
    """Represents the path of the point of interest"""
    missed_dots = int
    last_dot = ()

    def __init__(self):
        self.dots = []
        self.missed_dots = 0
        self.last_dot = (None, None)

    def append(self, coords: tuple):
        self.last_dot = coords
        self.dots.append(AnalogDot((coords[0], coords[1]), None))
