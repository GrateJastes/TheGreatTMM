import numpy as np
from .Dot import Dot, AnalogDot


class Path:
    """Represents the path of the point of interest"""
    missed_dots = int

    def __init__(self):
        self.dots = []
        self.missed_dots = 0

    def append(self, coords, frame_high, origin):
        self.dots.append((coords[0], frame_high - coords[1]))
