import math

import numpy as np

from .. import common
from ..common.Unit import Unit


def interpolate(point, base, step):
    ip_point = common.Point(point.name + '(ip)')
    dot_list = []
    for i in np.arange(0, 2 * math.pi + step, step):
        dot_list.append(common.Dot(np.interp(i, [dot.omega for dot in base.path.dots],
                                             [dot.x for dot in point.path.dots], period=2 * math.pi),
                                   np.interp(i, [dot.omega for dot in base.path.dots],
                                             [dot.y for dot in point.path.dots], period=2 * math.pi)))
    ip_point.path.dots = dot_list
    return ip_point


def diff1(point, base, step):
    ip_dot_list = interpolate(point, base, step)
    v_list = []
    v_q_x = (-1.5 * ip_dot_list.path.dots[0].x + 2 * ip_dot_list.path.dots[1].x -
             0.5 * ip_dot_list.path.dots[2].x) / step
    v_q_y = (-1.5 * ip_dot_list.path.dots[0].y + 2 * ip_dot_list.path.dots[1].y -
             0.5 * ip_dot_list.path.dots[2].y) / step
    v_list.append(Unit(v_q_x, v_q_y))
    for i in range(1, len(ip_dot_list.path.dots) - 1):
        v_q_x = (-0.5 * ip_dot_list.path.dots[i - 1].x + 0.5 * ip_dot_list.path.dots[i + 1].x) / step
        v_q_y = (-0.5 * ip_dot_list.path.dots[i - 1].y + 0.5 * ip_dot_list.path.dots[i + 1].y) / step
        v_list.append(Unit(v_q_x, v_q_y))
    v_q_x = (0.5 * ip_dot_list.path.dots[-3].x - 2 * ip_dot_list.path.dots[-2].x
             + 1.5 * ip_dot_list.path.dots[-1].x) / step
    v_q_y = (0.5 * ip_dot_list.path.dots[-3].y - 2 * ip_dot_list.path.dots[-2].y
             + 1.5 * ip_dot_list.path.dots[-1].y) / step
    v_list.append(Unit(v_q_x, v_q_y))
    return v_list


def diff2(point, base, step):
    ip_dot_list = interpolate(point, base, step)
    a_list = []
    a_q_x = (2 * ip_dot_list.path.dots[0].x - 5 * ip_dot_list.path.dots[1].x + 4 * ip_dot_list.path.dots[2].x
             - ip_dot_list.path.dots[3].x) / (step ** 2)
    a_q_y = (2 * ip_dot_list.path.dots[0].y - 5 * ip_dot_list.path.dots[1].y + 4 * ip_dot_list.path.dots[2].y
             - ip_dot_list.path.dots[3].y) / (step ** 2)
    a_list.append(Unit(a_q_x, a_q_y))
    for i in range(1, len(ip_dot_list.path.dots) - 1):
        a_q_x = (ip_dot_list.path.dots[i - 1].x - 2 * ip_dot_list.path.dots[i].x
                 + 1 * ip_dot_list.path.dots[i + 1].x) / (step ** 2)
        a_q_y = (ip_dot_list.path.dots[i - 1].y - 2 * ip_dot_list.path.dots[i].y
                 + 1 * ip_dot_list.path.dots[i + 1].y) / (step ** 2)
        a_list.append(Unit(a_q_x, a_q_y))
    a_q_x = (- ip_dot_list.path.dots[-4].x + 4 * ip_dot_list.path.dots[-3].x
             - 5 * ip_dot_list.path.dots[-2].x + 2 * ip_dot_list.path.dots[-1].x) / (step ** 2)
    a_q_y = (- ip_dot_list.path.dots[-4].y + 4 * ip_dot_list.path.dots[-3].y
             - 5 * ip_dot_list.path.dots[-2].y + 2 * ip_dot_list.path.dots[-1].y) / (step ** 2)
    a_list.append(Unit(a_q_x, a_q_y))
    return a_list

# Returns a polynomial function of dependence of y on x
def polinom(x, y):
    z = np.polyfit(x, y, 6)
    p = np.poly1d(z)
    return p
