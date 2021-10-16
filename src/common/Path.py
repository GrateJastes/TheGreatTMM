from .Dot import AnalogDot


class Path:
    """Represents the path of the point of interest"""
    missed_dots = int
    last_dot = ()

    def __init__(self):
        self.dots = []
        self.missed_dots = 0
        self.last_dot = None

    def append(self, coords, omega):
        self.last_dot = coords
        self.dots.append(AnalogDot((coords[0], coords[1]), omega))
