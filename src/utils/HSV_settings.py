from cv2 import cv2
import numpy as np

from settings_utils import *


def main():
    cv2.namedWindow('result')
    cv2.namedWindow('settings')
    create_trackers('settings')

    img = cv2.imread('assets/test.jpg', cv2.IMREAD_COLOR)
    img = minimize(img, 2.5)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    while True:
        h1, s1, v1, h2, s2, v2 = get_trackers_info('settings')

        h_min = np.array((h1, s1, v1), np.uint8)
        h_max = np.array((h2, s2, v2), np.uint8)

        thresh = cv2.inRange(hsv, h_min, h_max)

        cv2.imshow('result', thresh)
        ch = cv2.waitKey(50)
        if ch == 27:
            break

    cv2.destroyAllWindows()


main()
