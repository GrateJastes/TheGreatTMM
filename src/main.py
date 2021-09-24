import sys
from cv2 import cv2
import numpy as np

from consts.consts import MyConsts as consts
from utils.utils import minimize, show


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
    img = minimize(img, 2.5)
    img = cv2.medianBlur(img, 7)
    show('start', img)

    h, w = img.shape[:2]
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    marker = cv2.inRange(hsv, consts.HSV.LOWER_BLUE, consts.HSV.UPPER_BLUE)
    # marker = cv2.medianBlur(marker, 7)
    show('marker', marker)

    circles = cv2.HoughCircles(marker, cv2.HOUGH_GRADIENT, 2, 15, param1=30, param2=90, minRadius=0, maxRadius=-1)

    if circles is not None:
        x = 0
        y = 0

        for c in circles[0]:
            print(c)
            x = int(c[0])
            y = int(c[1])
            cv2.circle(img, (x, y), 3, consts.Color.YELLOW, -1)
            cv2.circle(img, (x, y), int(c[2]), consts.Color.YELLOW, 3)

    show('new', img)
    # contours, hierarchy = cv2.findContours(marker.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    #
    # cv2.drawContours(img, contours, -1, consts.Color.YELLOW, 2, cv2.LINE_AA)
    # cv2.imshow('contours', img)
    #
    # cv2.waitKey()
    cv2.destroyAllWindows()


make_contours()
