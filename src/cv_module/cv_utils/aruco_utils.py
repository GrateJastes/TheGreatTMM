from cv2 import cv2
import numpy as np

from src.cv_module import consts


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
    marker_corners, marker_ids, rejected = cv2.aruco.detectMarkers(frame, dictionary, parameters=parameters)
    if not marker_ids or len(marker_ids) != 1 or marker_ids[0] != consts.ARUCO_MARKER_ID:
        return None
    origin = find_aruco_center(marker_corners)

    return origin
