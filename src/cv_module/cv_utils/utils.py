import math
from statistics import mean

import numpy as np
from cv2 import cv2

from .. import consts
from ... import common

__all__ = ['minimize',
           'show',
           'find_marker',
           'prepare_frame',
           'path_jump_detected',
           'find_aruco_origin',
           'research_link',
           ]


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


def find_aruco_center(marker_corners):
    box = np.int0(marker_corners[0][0])
    m10 = 0
    m01 = 0
    m00 = len(box)

    for dot in box:
        m10 += dot[0]
        m01 += dot[1]

    centerX = m10 / m00
    centerY = m01 / m00

    return int(centerX), int(centerY)


def find_aruco_origin(frame, dictionary, parameters):
    marker_corners, marker_ids, _ = cv2.aruco.detectMarkers(frame, dictionary, parameters=parameters)
    if len(marker_ids) != 1 or marker_ids[0] != consts.ARUCO_MARKER_ID:
        return None
    origin = find_aruco_center(marker_corners)

    return origin


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


def research_link(start_frame, origin, link, omega=None):
    marker_color = consts.DESIRED_MARKER_COLOR if omega else consts.INITIAL_MARKER_COLOR
    circle_color = consts.BGR.GREEN if omega else consts.BGR.YELLOW

    frame = prepare_frame(start_frame, marker_color)
    contours, _ = cv2.findContours(frame, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    marker_found, marker_dot = find_marker(contours)

    if marker_found:
        coords = traverse_coordinates(marker_dot, origin)
        cv2.circle(start_frame, (int(marker_dot[0]), int(marker_dot[1])), 2, circle_color, 2)

        if not omega:
            omega = find_omega(coords)

        link.path.dots.append(common.AnalogDot(coords, omega))
    else:
        link.path.missed_dots += 1
        link.path.dots.append(common.AnalogDot((None, None), None))

    return marker_found, omega
