import math
import numpy as np
from statistics import mean
from cv2 import cv2

from src.cv_module import consts


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
