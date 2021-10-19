import math

import cv2.aruco
from cv2 import cv2

from src import common
from src.cv_module import consts
from src.cv_module.cv_utils import *
from src.diff import diff_utils
from src.mpl_graphs import graphs


def main():
    dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_50)
    parameters = cv2.aruco.DetectorParameters_create()

    initial_link = common.Point('A', is_base=True)
    desired_link = common.Point('B')

    cv2.namedWindow('way')
    cap = cv2.VideoCapture('assets/video/test1.mp4')
    missed_in_a_row = 0
    while True:
        if missed_in_a_row >= 10:
            break
        flag, start_frame = cap.read()
        if not flag:
            break

        origin = find_aruco_origin(start_frame, dictionary, parameters)
        if not origin:
            missed_in_a_row += 1
            continue

        initial_ok, omega = research_link(start_frame, origin, initial_link)
        if not initial_ok or not omega:
            missed_in_a_row += 1
            continue

        desired_ok, _ = research_link(start_frame, origin, desired_link, omega)
        if not desired_ok:
            missed_in_a_row += 1
            continue

        cv2.imshow('way', start_frame)
        ch = cv2.waitKey(consts.TIME_TO_READ_INPUT)
        if ch == consts.ESC_KEY_CODE:
            break

    graphs.print_path(initial_link, desired_link)

    step = math.pi / 15
    inter_scale = diff_utils.interpolate(initial_link, initial_link, step)
    desired_scale = diff_utils.interpolate(desired_link, initial_link, step)

    graphs.print_path(inter_scale, desired_scale)

    initial_link.speed = diff_utils.diff1(initial_link, initial_link, step)
    desired_link.speed = diff_utils.diff1(desired_link, initial_link, step)

    graphs.print_analog_v(step, initial_link, desired_link)

    step = math.pi / 13

    initial_link.acceleration = diff_utils.diff2(initial_link, initial_link, step)
    desired_link.acceleration = diff_utils.diff2(desired_link, initial_link, step)

    graphs.print_analog_a(step, initial_link, desired_link)

    cv2.waitKey(0)

    cap.release()
    cv2.destroyAllWindows()


main()
