import sys
from cv2 import cv2
import numpy as np

from consts.consts import MyConsts as consts
from utils.utils import minimize, show


def prepare_frame(frame, marker_color):
    hsv_bounds = {
        consts.Color.RED: (consts.HSV.LOWER_RED, consts.HSV.UPPER_RED),
        consts.Color.BLUE: (consts.HSV.LOWER_BLUE, consts.HSV.UPPER_BLUE),
    }.get(marker_color)

    frame = cv2.medianBlur(frame, consts.MEDIAN_KERNEL)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    thresh = cv2.inRange(hsv, hsv_bounds[0], hsv_bounds[1])
    opened = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, consts.MORPH_OPEN_KERNEL)
    closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, consts.MORPH_OPEN_KERNEL)
    show('binary', closed)

    return closed


def main():
    cv2.namedWindow('result')
    cap = cv2.VideoCapture('assets/video/test.mp4')

    while True:
        flag, frame = cap.read()
        if not flag:
            break

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        marker = cv2.inRange(hsv, consts.HSV.LOWER_BLUE, consts.HSV.UPPER_BLUE)

        moments = cv2.moments(marker)
        dM01 = moments['m01']
        dM10 = moments['m10']
        dArea = moments['m00']

        if dArea > 100:
            x = int(dM10 / dArea)
            y = int(dM01 / dArea)
            cv2.circle(frame, (x, y), 5, consts.Color.YELLOW, 2)
            cv2.putText(frame, '%d-%d' % (x, y), (x + 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, consts.Color.YELLOW, 1)

        cv2.imshow('result', frame)
        ch = cv2.waitKey(5)
        if ch == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


# main()

def make_contours():
    img = cv2.imread('assets/test.jpg', cv2.IMREAD_COLOR)
    show('start', img)

    frame = prepare_frame(img, consts.Color.RED)

    contours, hierarchy = cv2.findContours(frame.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    cv2.drawContours(img, contours, -1, consts.Color.YELLOW, 2, cv2.LINE_AA)
    cv2.imshow('contours', img)

    for cnt in contours:
        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        cv2.drawContours(img, [box], 0, consts.Color.YELLOW, 2)

    show('contours', img)
    cv2.destroyAllWindows()


make_contours()


def draw_haugh_circles(binary, frame):
    circles = cv2.HoughCircles(
        binary,
        cv2.HOUGH_GRADIENT,
        dp=3,
        minDist=15,
        param1=30,
        param2=190,
        minRadius=0,
        maxRadius=-1)

    if circles is not None:
        for c in circles[0]:
            print(c)
            x = int(c[0])
            y = int(c[1])
            cv2.circle(frame, (x, y), 3, consts.Color.YELLOW, -1)
            cv2.circle(frame, (x, y), int(c[2]), consts.Color.YELLOW, 3)
