import numpy as np

from settings_utils import *
from .. import consts
from .. import cv_utils


FRAME_TIME = 50


def hsv_settings(img):
    cv2.namedWindow('result')
    cv2.namedWindow('settings')
    create_trackers('settings')
    cv_utils.show('result', img)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    while True:
        h1, s1, v1, h2, s2, v2 = get_trackers_info('settings')

        h_min = np.array((h1, s1, v1), np.uint8)
        h_max = np.array((h2, s2, v2), np.uint8)

        thresh = cv2.inRange(hsv, h_min, h_max)

        cv2.imshow('result', thresh)
        ch = cv2.waitKey(FRAME_TIME)
        if ch == consts.ESC_KEY_CODE:
            break

    cv2.destroyWindow('result')
    cv2.destroyWindow('settings')
