import cv2

from src.common_entities import Point
from src.common_entities.mechanism.Link import Link
from src.cv_module import consts
from src.cv_module.HSV_settings.HSV_settings import hsv_settings
from src.cv_module.cv_utils import *


def main():
    cv2.namedWindow('way')

    video = cv2.VideoCapture('assets/new/mech_1/stable_short.mp4')
    color_bounds = consts.get_bound_colors(consts.BGR.YELLOW)
    while True:
        frame_read, start_frame = video.read()
        if not frame_read:
            break
        start_frame = minimize(start_frame, 2.5)

        frame = prepare_frame(start_frame, color_bounds)

        cv2.imshow('way', frame)
        ch = cv2.waitKey(5)
        if ch == consts.ESC_KEY_CODE:
            break
        if ch == 19:
            hsv_settings(start_frame, color_bounds)

    video.release()
    cv2.destroyAllWindows()


main()
