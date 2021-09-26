from cv2 import cv2
import matplotlib.pyplot as plt

import cv_module.consts as consts
from cv_module.cv_utils import *
import common


def main():
    cv2.namedWindow('way')
    cap = cv2.VideoCapture('assets/video/test4.mp4')
    point = common.Point('Point', is_base=True)
    image = None

    while True:
        flag, start_frame = cap.read()
        if not flag:
            break

        frame = prepare_frame(start_frame, consts.BGR.RED)
        contours, hierarchy = cv2.findContours(frame, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        marker_found, marker_dot = find_marker(contours)

        if marker_found:
            cv2.circle(start_frame, (int(marker_dot[0]), int(marker_dot[1])), 2, consts.BGR.YELLOW, 2)
            # if path_jump_detected(point.path, marker_dot):
            #     show('way', frame)
            point.path.append(marker_dot, frame_high=frame.shape[0])
        else:
            point.path.missed_dots += 1
            # show('way', frame)
            # hsv_settings(start_frame)

        cv2.imshow('way', start_frame)
        ch = cv2.waitKey(consts.TIME_TO_READ_INPUT)
        if ch == consts.ESC_KEY_CODE:
            image = start_frame
            break

    plt.plot([dot[0] for dot in point.path.dots], [dot[1] for dot in point.path.dots])
    plt.show()
    cv2.waitKey(0)

    cap.release()
    cv2.destroyAllWindows()


main()
