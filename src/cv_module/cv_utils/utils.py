import math

from cv2 import cv2

from .. import consts
from .geometry import bad_circle, bad_ellipse_fitting

__all__ = ['minimize',
           'show',
           'prepare_frame',
           'path_jump_detected',
           'find_marker_signatures',
           'traverse_coordinates',
           'find_omega',
           'find_closest',
           'remove_jumps',
           'distance',
           ]

from ...common_entities import Dot


def minimize(img, scale):
    return cv2.resize(img, (int(img.shape[1] / scale), int(img.shape[0] / scale)), cv2.INTER_AREA)


def show(header, img):
    cv2.imshow(header, img)
    cv2.waitKey()


def find_marker_signatures(contours):
    signatures = []
    for cnt in contours:
        if len(cnt) > consts.MIN_POINTS_FOR_ELLIPSE:
            ellipse = cv2.fitEllipse(cnt)
            if bad_circle(ellipse) or bad_ellipse_fitting(ellipse, cnt):
                continue

            signatures.append(ellipse)
    return signatures


def prepare_frame(frame, hsv_bounds):
    blurred = cv2.medianBlur(frame, consts.MEDIAN_PREP_KERNEL)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    binary = cv2.inRange(hsv, hsv_bounds[0], hsv_bounds[1])

    opened = cv2.morphologyEx(binary, cv2.MORPH_OPEN, consts.MORPH_OPEN_KERNEL)
    closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, consts.MORPH_OPEN_KERNEL)

    smoothed = cv2.medianBlur(closed, consts.MEDIAN_BIN_KERNEL)

    return smoothed


def path_jump_detected(path, marker_dot):
    if not path.dots:
        return False

    dx = path.dots[-1][0] - int(marker_dot[0])
    dy = path.dots[-1][1] - int(marker_dot[1])

    return dx > consts.JUMP_THRESHOLD or dy > consts.JUMP_THRESHOLD


def traverse_coordinates(desired_dot, origin):
    newX = desired_dot[0] - origin[0]
    newY = - desired_dot[1] + origin[1]

    return newX, newY


def find_omega(desired_dot):
    x = desired_dot[0]
    y = desired_dot[1]

    omega = math.atan2(y, x)

    return omega


def find_closest(origin, candidates):
    total_min = None
    result = (None, None)
    for candidate in candidates:
        if candidate is None or candidate[0] is None:
            continue

        dist = math.sqrt((candidate[0] - origin[0]) ** 2 + (candidate[1] - origin[1]) ** 2)
        if total_min is None or dist < total_min:
            total_min = dist
            result = candidate

    return result


def remove_jumps(path: list[Dot]):
    for idx, dot in enumerate(path):
        if idx == 0:
            continue
        if math.sqrt((dot.x - path[idx - 1].x) ** 2 + (dot.y - path[idx - 1].y) ** 2) > 10:
            path.remove(dot)


def distance(dot1: Dot, dot2: Dot) -> float:
    return math.sqrt((dot1.x - dot2.x) ** 2 + (dot1.y - dot2.y) ** 2)


def is_near(dot1: Dot, dot2: Dot) -> bool:
    return distance(dot1, dot2) < consts.MIN_CLOSURE_DIST
