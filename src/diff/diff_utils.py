import math

import numpy as np

import consts
from .. import common_entities
from ..common_entities.Unit import Unit
from ..mpl_graphs import graphs


def interpolate(point, base, step):
    ip_point = common_entities.Point(point.name + '(ip)')
    dot_list = []
    for i in np.arange(0, 2 * math.pi + step, step):
        dot_list.append(common_entities.Dot(np.interp(i, [dot.omega for dot in base.path.dots],
                                                      [dot.x for dot in point.path.dots], period=2 * math.pi),
                                            np.interp(i, [dot.omega for dot in base.path.dots],
                                             [dot.y for dot in point.path.dots], period=2 * math.pi)))
    ip_point.path.dots = dot_list
    return ip_point


def forward_difference_1(ip_point, type_of_coord):
    difference = None
    if type_of_coord == 'x':
        difference = (-1.5 * ip_point.path.dots[0].x + 2 * ip_point.path.dots[1].x -
                      0.5 * ip_point.path.dots[2].x) / consts.STEP_SPLITTING
    elif type_of_coord == 'y':
        difference = (-1.5 * ip_point.path.dots[0].y + 2 * ip_point.path.dots[1].y -
                      0.5 * ip_point.path.dots[2].y) / consts.STEP_SPLITTING
    return difference


def central_difference_1(ip_point, num, type_of_coord):
    difference = None
    if type_of_coord == 'x':
        difference = (-0.5 * ip_point.path.dots[num - 1].x + 0.5 * ip_point.path.dots[
            num + 1].x) / consts.STEP_SPLITTING
    elif type_of_coord == 'y':
        difference = (-0.5 * ip_point.path.dots[num - 1].y + 0.5 * ip_point.path.dots[
            num + 1].y) / consts.STEP_SPLITTING
    return difference


def backward_difference_1(ip_point, type_of_coord):
    difference = None
    if type_of_coord == 'x':
        difference = (0.5 * ip_point.path.dots[-3].x - 2 * ip_point.path.dots[-2].x
                      + 1.5 * ip_point.path.dots[-1].x) / consts.STEP_SPLITTING
    elif type_of_coord == 'y':
        difference = (0.5 * ip_point.path.dots[-3].y - 2 * ip_point.path.dots[-2].y
                      + 1.5 * ip_point.path.dots[-1].y) / consts.STEP_SPLITTING
    return difference


def diff1(point, base):
    ip_dot_list = interpolate(point, base)
    v_list = [Unit(forward_difference_1(ip_dot_list, 'x'), forward_difference_1(ip_dot_list, 'y'))]
    for i in range(1, len(ip_dot_list.path.dots) - 1):
        v_list.append(Unit(central_difference_1(ip_dot_list, i, 'x'),
                           central_difference_1(ip_dot_list, i, 'y')))
    v_list.append(Unit(backward_difference_1(ip_dot_list, 'x'), backward_difference_1(ip_dot_list, 'y')))
    return v_list


def forward_difference_2(ip_point, type_of_coord):
    difference = None
    if type_of_coord == 'x':
        difference = (2 * ip_point.path.dots[0].x - 5 * ip_point.path.dots[1].x + 4 * ip_point.path.dots[2].x
                      - ip_point.path.dots[3].x) / (consts.STEP_SPLITTING ** 2)
    elif type_of_coord == 'y':
        difference = (2 * ip_point.path.dots[0].y - 5 * ip_point.path.dots[1].y + 4 * ip_point.path.dots[2].y
                      - ip_point.path.dots[3].y) / (consts.STEP_SPLITTING ** 2)
    return difference


def central_difference_2(ip_point, num, type_of_coord):
    difference = None
    if type_of_coord == 'x':
        difference = (ip_point.path.dots[num - 1].x - 2 * ip_point.path.dots[num].x
                      + 1 * ip_point.path.dots[num + 1].x) / (consts.STEP_SPLITTING ** 2)
    elif type_of_coord == 'y':
        difference = (ip_point.path.dots[num - 1].y - 2 * ip_point.path.dots[num].y
                      + 1 * ip_point.path.dots[num + 1].y) / (consts.STEP_SPLITTING ** 2)
    return difference


def backward_difference_2(ip_point, type_of_coord):
    difference = None
    if type_of_coord == 'x':
        difference = (- ip_point.path.dots[-4].x + 4 * ip_point.path.dots[-3].x
                      - 5 * ip_point.path.dots[-2].x + 2 * ip_point.path.dots[-1].x) / (consts.STEP_SPLITTING ** 2)
    elif type_of_coord == 'y':
        difference = (- ip_point.path.dots[-4].y + 4 * ip_point.path.dots[-3].y
                      - 5 * ip_point.path.dots[-2].y + 2 * ip_point.path.dots[-1].y) / (consts.STEP_SPLITTING ** 2)
    return difference


def diff2(point, base):
    ip_dot_list = interpolate(point, base)
    a_list = [Unit(forward_difference_2(ip_dot_list, 'x'), forward_difference_2(ip_dot_list, 'y'))]
    for num in range(1, len(ip_dot_list.path.dots) - 1):
        a_list.append(Unit(central_difference_2(ip_dot_list, num, 'x'), central_difference_2(ip_dot_list, num, 'y')))
    a_list.append(Unit(backward_difference_2(ip_dot_list, 'x'), backward_difference_2(ip_dot_list, 'y')))
    return a_list


# Returns a polynomial function of dependence of y on x
def polinom(x, y):
    z = np.polyfit(x, y, consts.DEGREE_OF_POLYNOMIAL)
    p = np.poly1d(z)
    return p
