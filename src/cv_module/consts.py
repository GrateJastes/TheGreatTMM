import numpy as np


class HSV:
    LOWER_RED = np.array([0, 59, 133])
    UPPER_RED = np.array([255, 255, 255])
    LOWER_BLUE = np.array([109, 11, 68])
    UPPER_BLUE = np.array([149, 255, 255])


class BGR:
    YELLOW = (0, 255, 255)
    BLUE = (255, 0, 0)
    RED = (0, 0, 255)


ESC_KEY_CODE = 27
TIME_TO_READ_INPUT = 5

# for my cv-utils
MAX_ECCENTRICITY = 0.4
MAX_AREAS_DEVIATION = 0.03
MIN_POINTS_FOR_ELLIPSE = 4

MEDIAN_PREP_KERNEL = 5
MEDIAN_BIN_KERNEL = 13
MORPH_OPEN_KERNEL = np.ones((7, 7), np.uint8)
MORPH_CLOSE_KERNEL = np.ones((9, 9), np.uint8)


JUMP_THRESHOLD = 200
