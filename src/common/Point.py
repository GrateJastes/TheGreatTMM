import numpy as np
from .Path import Path


class Point:
    def __init__(self, name, is_base=False):
        self.name = name
        self.path = Path()
