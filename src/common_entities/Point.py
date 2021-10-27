import math

from .Path import Path
from src.diff import diff_utils
from src.diff import consts as diff_consts


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

    def analog_angle(self):
        return [i * diff_consts.STEP_SPLITTING for i in range(2 * math.pi / diff_consts.STEP_SPLITTING)]
