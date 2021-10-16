import numpy as np
from .Path import Path
from .Dot import AnalogDot


class Point:
    def __init__(self, name, is_base=False):
        self.is_base = is_base
        self.name = name
        self.path = Path()

