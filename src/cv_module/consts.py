import numpy as np


class HSV:
    LOWER_RED = np.array([0, 150, 133])
    UPPER_RED = np.array([255, 255, 255])
    LOWER_BLUE = np.array([109, 11, 68])
    UPPER_BLUE = np.array([149, 255, 255])


class BGR:
    YELLOW = (0, 255, 255)
    BLUE = (255, 0, 0)
    RED = (0, 0, 255)
    GREEN = (0, 255, 0)


ESC_KEY_CODE = 27
TIME_TO_READ_INPUT = 5

# for my cv-utils
MAX_ECCENTRICITY = 0.5
MAX_AREAS_DEVIATION = 0.09
MIN_POINTS_FOR_ELLIPSE = 4

MEDIAN_PREP_KERNEL = 5
MEDIAN_BIN_KERNEL = 13
MORPH_OPEN_KERNEL = np.ones((7, 7), np.uint8)
MORPH_CLOSE_KERNEL = np.ones((9, 9), np.uint8)


JUMP_THRESHOLD = 200

ARUCO_MARKER_ID = 42

INITIAL_MARKER_COLOR = BGR.RED
DESIRED_MARKER_COLOR = BGR.BLUE

MIN_FPS_REQUIRED = 30
MIN_FRAMES_COUNT = 100


class DebugMode:
    DEBUG_OFF = 0
    DEBUG_VIDEO_SHOW = 1
    DEBUG_FULL = 2


def get_bound_colors(color):
    return {
        BGR.RED: (HSV.LOWER_RED, HSV.UPPER_RED),
        BGR.BLUE: (HSV.LOWER_BLUE, HSV.UPPER_BLUE),
    }.get(color)

