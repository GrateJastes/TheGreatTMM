import numpy as np


class MyConsts:
    class HSV:
        LOWER_RED = np.array([0, 70, 70])
        UPPER_RED = np.array([8, 255, 255])
        LOWER_BLUE = np.array([109, 70, 68])
        UPPER_BLUE = np.array([149, 255, 255])

    class Color:
        YELLOW = (0, 255, 255)
        BLUE = (255, 0, 0)
        RED = (0, 0, 255)

    MEDIAN_KERNEL = 7
    MORPH_OPEN_KERNEL = np.ones((7, 7), np.uint8)
    MORPH_CLOSE_KERNEL = np.ones((7, 7), np.uint8)

    