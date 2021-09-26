import numpy as np
from .Path import Path


class Point:
    def __init__(self, name, is_base=False):
        self.is_base = is_base
        self.name = name
        self.path = Path()

    # def add_trajectory_dot(self, coords, omega):