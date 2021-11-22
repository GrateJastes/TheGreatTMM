import numpy as np

from .Path import Path
from src.diff import diff_utils
from src.diff import consts as diff_consts


class Point:
    path: Path
    is_base: bool
    name: str
    speed: list
    acceleration: list

    def __init__(self, name: str, is_base=False):
        self.is_base = is_base
        self.name = name
        self.path = Path()
        self.speed = []
        self.acceleration = []

    def point_analysis(self, base):
        self.speed = diff_utils.diff1(self, base)
        self.acceleration = diff_utils.diff2(self, base)

    def analog_angle(self):
        return [i * diff_consts.STEP_SPLITTING for i in range(len(self.speed))]

# returns a path object - [dot, dot, dot, ...] for an interpolated path
    def interpolated_path(self, base):
        return diff_utils.linear_interpolate(self, base).path

    # restores missing points by the closest points in the list
    def restore_dots(self):
        for i in range(len(self.path.dots) - 1):
            if self.path.dots[i].x is None:
                j = i
                k = 1
                while (j < len(self.path.dots) - 1) and (self.path.dots[j].x is None):
                    j += 1
                    k += 1
                self.fill_dots(i, k)

    # fills the segment with averaged dots
    def fill_dots(self, first_occurrence, num_of_gaps):
        difference_x = self.path.dots[first_occurrence + num_of_gaps - 1].x - self.path.dots[first_occurrence - 1].x
        difference_y = self.path.dots[first_occurrence + num_of_gaps - 1].y - self.path.dots[first_occurrence - 1].y
        delta_x = difference_x / num_of_gaps
        delta_y = difference_y / num_of_gaps
        j = first_occurrence
        while j <= first_occurrence + num_of_gaps - 1:
            self.path.dots[j].x = self.path.dots[first_occurrence - 1].x + delta_x * (j - first_occurrence + 1)
            self.path.dots[j].y = self.path.dots[first_occurrence - 1].y + delta_y * (j - first_occurrence + 1)
            j += 1

    def remove_dot_repeat(self):
        # print(self.name, ':', [(self.path.dots[i].x, self.path.dots[i].y) for i in range(len(self.path.dots))])
        for i in range(len(self.path.dots) - 1):
            if ((self.path.dots[i].x == self.path.dots[i + 1].x)
                    and (self.path.dots[i].y == self.path.dots[i + 1].y)):
                j = i
                k = 1
                while ((j < len(self.path.dots) - 1)
                       and (self.path.dots[j].x == self.path.dots[j + 1].x)
                       and (self.path.dots[j].y == self.path.dots[j + 1].y)):
                    j += 1
                    k += 1
                self.fill_dots(i, k)
                # print(self.name, i, [(self.path.dots[i].x, self.path.dots[i].y) for i in range(len(self.path.dots))])

    def get_coord_for_plot(self, coord_name: str) -> np.array:
        if coord_name == 'x':
            return np.array([dot.x if dot.x is not None else np.nan for dot in self.path.dots])
        else:
            return np.array([dot.y if dot.y is not None else np.nan for dot in self.path.dots])
