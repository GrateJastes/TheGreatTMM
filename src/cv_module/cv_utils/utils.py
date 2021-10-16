import math

from cv2 import cv2

from .. import consts
from .geometry import bad_circle, bad_ellipse_fitting, ellipse_area

__all__ = ['minimize',
           'show',
           'find_marker',
           'prepare_frame',
           'path_jump_detected',
           'find_marker_signatures',
           'traverse_coordinates',
           'find_closest',
           'find_omega',
           ]


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


def find_marker(contours):
    marker_found = False
    if not contours:
        return marker_found, None

    if len(contours) == 1:
        if len(contours[0]) > consts.MIN_POINTS_FOR_ELLIPSE:
            marker_found = True
            ellipse = cv2.fitEllipse(contours[0])
            return marker_found, (int(ellipse[0][0]), int(ellipse[0][1]))
        return marker_found, None

    signatures = find_marker_signatures(contours)

    if not signatures:
        return marker_found, None

    if len(signatures) == 1:
        marker = signatures[0]
    else:
        marker = max(signatures, key=ellipse_area)
    marker_found = True

    return marker_found, (int(marker[0][0]), int(marker[0][1]))


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

    omega = {
        x > 0 and y >= 0: math.atan(y / x),
        x > 0 and y < 0: math.atan(y / x) + 2 * math.pi,
        x < 0: math.atan(y / x) + math.pi,
        x == 0 and y > 0: math.pi / 2,
        x == 0 and y < 0: - math.pi / 2,
        x == 0 and y == 0: None,
    }.get(True)

    return omega


def find_closest(last_dot, candidates):
    total_min = None
    result = None
    for candidate in candidates:
        if candidate is None:
            continue

        dist = math.sqrt((candidate[0] - last_dot[0]) ** 2 + (candidate[1] - last_dot[1]) ** 2)
        if total_min is None or dist < total_min:
            total_min = dist
            result = candidate

    return result
