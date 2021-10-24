from .Path import Path
from ..diff import diff_utils


class Point:
    def __init__(self, name, is_base=False):
        self.is_base = is_base
        self.name = name
        self.path = Path()
        self.speed = []
        self.acceleration = []

    def point_analysis(self, base):
        self.speed = diff_utils.diff1(self, base)
        self.acceleration = diff_utils.diff2(self, base)
