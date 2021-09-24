import numpy as np


class MyConsts:
    class HSV:
        LOWER_RED = np.array([0, 70, 70])
        UPPER_RED = np.array([5, 255, 255])
        LOWER_BLUE = np.array([109, 70, 68])
        UPPER_BLUE = np.array([149, 255, 255])

    class Color:
        YELLOW = (0, 255, 255)
        BLUE = (255, 0, 0)
    