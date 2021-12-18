import numpy as np


# Here is file with most of constant values we will be using in the entire project. They can be divided into classes
# or dictionaries to keep this file more structured


# HSV bounds for extracting presented color from the frame in preparing process.
# Is being used in get_bound_colors() method
class HSV:
    LOWER_RED = np.array([150, 80, 125])
    UPPER_RED = np.array([255, 255, 255])

    LOWER_BLUE = np.array([102, 100, 32])
    UPPER_BLUE = np.array([149, 255, 255])

    LOWER_GREEN = np.array([57, 100, 32])
    UPPER_GREEN = np.array([80, 255, 255])

    LOWER_YELLOW = np.array([20, 90, 136])
    UPPER_YELLOW = np.array([50, 255, 255])

    LOWER_RED_L = np.array([0, 90, 136])
    UPPER_RED_L = np.array([3, 255, 255])


# Just colors preset in BGR (Blue--Green--Red) color scheme
class BGR:
    YELLOW = (0, 255, 255)
    BLUE = (255, 0, 0)
    RED = (0, 0, 255)
    GREEN = (0, 255, 0)


# For cv2.waitKey(), debugging purpose
ESC_KEY_CODE = 27
TIME_TO_READ_INPUT = 5

# Geometry constants to evaluate proper markers' signatures
MAX_ECCENTRICITY = 0.5
MAX_AREAS_DEVIATION = 0.09
MIN_POINTS_FOR_ELLIPSE = 4

# Frame preparing settings. Preprocessing frame before looking for signatures in it
MEDIAN_PREP_KERNEL = 5
MEDIAN_BIN_KERNEL = 13
MORPH_OPEN_KERNEL = np.ones((3, 3), np.uint8)
MORPH_CLOSE_KERNEL = np.ones((21, 21), np.uint8)

JUMP_THRESHOLD = 200

# Constant aruco center marker's ID, which we are using
ARUCO_MARKER_ID = 42

# We need some minimum requirements for the video input. We check it when Mechanism is being created
MIN_FPS_REQUIRED = 25
MIN_FRAMES_COUNT = 100


# Just debugging mode flag, used in Mechanism creation. It allows running Mechanism's methods in different modes
class DebugMode:
    DEBUG_OFF = 0
    DEBUG_VIDEO_SHOW = 1
    DEBUG_FULL = 2


# Chose the right HSV color bounds to prepare frame for processing. It depends on link, which is being researching now,
# and it's predefined color
def get_bound_colors(
        color: tuple[int, int, int],
        alternative_red: bool = False,
        color_bounds=None,
) -> tuple[np.ndarray, np.ndarray]:
    if alternative_red:
        if all(color_bounds[0] == HSV.LOWER_RED):
            return HSV.LOWER_RED_L, HSV.UPPER_RED_L

    return {
        BGR.RED: (HSV.LOWER_RED, HSV.UPPER_RED),
        BGR.BLUE: (HSV.LOWER_BLUE, HSV.UPPER_BLUE),
        BGR.GREEN: (HSV.LOWER_GREEN, HSV.UPPER_GREEN),
        BGR.YELLOW: (HSV.LOWER_YELLOW, HSV.UPPER_YELLOW),
    }.get(color)


PROGRESS_BAR_MAX = 100

MIN_CLOSURE_DIST = 10.0
MIN_DIST_TO_START = MIN_CLOSURE_DIST * 1.5
DOTS_AFTER_CIRCLE = 1

MIN_DIST_TO_MOVE = 2.0

PREVIEW_POINT_CENTRE_RADIUS = 5
PREVIEW_POINT_CENTRE_THICKNESS = 2
PREVIEW_POINT_TEXT_THICKNESS = 2
PREVIEW_POINT_TEXT_SHIFT = 10
PREVIEW_POINT_FONT_SCALE = 1
PREVIEW_WINDOW_W = 960
PREVIEW_WINDOW_H = 540

ARUCO_SCALING_DIAG_MM = 70.

MIN_ANGLE = np.pi / 2
