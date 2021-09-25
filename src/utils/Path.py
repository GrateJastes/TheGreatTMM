import numpy as np
from Dot import Dot


class Path:
    """Represents the path of the point of interest"""

    def __init__(self):
        self.dots = np.array([], Dot)

    def append(self, dot):
        np.append(self.dots, [dot])
