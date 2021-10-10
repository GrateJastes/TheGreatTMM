import math

import cv2.aruco
import numpy
from cv2 import cv2
import matplotlib.pyplot as plt

from src import common
from src.cv_module import consts
from src.cv_module.cv_utils import *
from src.diff import diff_utils


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

    plt.title('Результат распознавания')
    plt.plot([dot.x for dot in initial_link.path.dots], [dot.y for dot in initial_link.path.dots])
    plt.xlabel("x")
    plt.ylabel("y")
    plt.show()

    step = math.pi / 40
    inter_scale = diff_utils.interpolate(initial_link, initial_link, step)

    plt.title('Траектория с учетом интерполяции')
    plt.plot([dot.x for dot in inter_scale.path.dots], [dot.y for dot in inter_scale.path.dots])
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True)
    plt.show()

    v_scale = diff_utils.diff1(initial_link, initial_link, step)

    plt.subplot(211)
    plt.title('Цикловые графики аналогов скоростей')
    plt.plot([item * step for item in range(len(v_scale))], [dot[0] for dot in v_scale])
    plt.ylabel("v_x")
    plt.grid(True)

    plt.subplot(212)
    plt.plot([item * step for item in range(len(v_scale))], [dot[1] for dot in v_scale])
    plt.xlabel("phi")
    plt.ylabel("v_y")
    plt.grid(True)

    plt.show()

    step = math.pi / 11

    a_scale = diff_utils.diff2(initial_link, initial_link, step)

    plt.subplot(211)
    plt.plot([item * step for item in range(len(a_scale))], [dot[0] for dot in a_scale])
    plt.title('Цикловые графики аналогов ускорений')
    plt.ylabel("a_x")
    plt.grid(True)

    plt.subplot(212)
    plt.plot([item * step for item in range(len(a_scale))], [dot[1] for dot in a_scale])
    plt.xlabel("phi")
    plt.ylabel("a_y")
    plt.grid(True)

    plt.show()

    cv2.waitKey(0)

    cap.release()
    cv2.destroyAllWindows()


main()
