import math
from statistics import mean

import numpy as np
from cv2 import cv2

from .. import consts


__all__ = ['minimize', 'show', 'find_marker', 'prepare_frame', 'path_jump_detected']


def minimize(img, scale):
    return cv2.resize(img, (int(img.shape[1] / scale), int(img.shape[0] / scale)), cv2.INTER_AREA)


def show(header, img):
    cv2.imshow(header, img)
    cv2.waitKey()


def ellipse_area(ellipse):
    return math.pi * ellipse[1][0] * ellipse[1][1] / 4


def eccentricity(ellipse):
    a = ellipse[1][1] / 2
    b = ellipse[1][0] / 2
    c = np.sqrt(a ** 2 - b ** 2)
    return c / a


def bad_ellipse_fitting(ellipse, cnt):
    area_c = cv2.contourArea(cnt)
    area_e = ellipse_area(ellipse)
    diff = np.abs(area_e - area_c)
    middle_area = mean([area_c, area_e])

    return diff / middle_area > consts.MAX_AREAS_DEVIATION


def bad_circle(ellipse):
    return eccentricity(ellipse) > consts.MAX_ECCENTRICITY


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


def prepare_frame(frame, marker_color):
    hsv_bounds = {
        consts.BGR.RED: (consts.HSV.LOWER_RED, consts.HSV.UPPER_RED),
        consts.BGR.BLUE: (consts.HSV.LOWER_BLUE, consts.HSV.UPPER_BLUE),
    }.get(marker_color)

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
