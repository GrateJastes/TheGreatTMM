import math
import matplotlib.pyplot as plt
import numpy
from .. import common


def interpolate(path, base_path, step):
    ip_dot_list = []
    for i in numpy.arange(0, 2 * math.pi + step, step):
        ip_dot_list.append([numpy.interp(i, [dot.omega for dot in base_path.dots],
                                         [dot.x for dot in path.dots], period=2*math.pi),
                            numpy.interp(i, [dot.omega for dot in base_path.dots],
                                         [dot.y for dot in path.dots], period=2*math.pi)])
    return ip_dot_list


def diff1(path, base_path, step):
    ip_dot_list = interpolate(path, base_path, step)
    v_list = []
    v_q_x = (-1.5 * ip_dot_list[0][0] + 2 * ip_dot_list[1][0] - 0.5 * ip_dot_list[2][0]) / step
    v_q_y = (-1.5 * ip_dot_list[0][1] + 2 * ip_dot_list[1][1] - 0.5 * ip_dot_list[2][1]) / step
    v_list.append([v_q_x, v_q_y])
    for i in range(1, len(ip_dot_list) - 1):
        v_q_x = (-0.5 * ip_dot_list[i - 1][0] + 0.5 * ip_dot_list[i + 1][0]) / step
        v_q_y = (-0.5 * ip_dot_list[i - 1][1] + 0.5 * ip_dot_list[i + 1][1]) / step
        v_list.append([v_q_x, v_q_y])
    v_q_x = (0.5 * ip_dot_list[-3][0] - 2 * ip_dot_list[-2][0] + 1.5 * ip_dot_list[-1][0]) / step
    v_q_y = (0.5 * ip_dot_list[-3][1] - 2 * ip_dot_list[-2][1] + 1.5 * ip_dot_list[-1][1]) / step
    v_list.append([v_q_x, v_q_y])
    return v_list


def diff2(path, base_path, step):
    ip_dot_list = interpolate(path, base_path, step)
    a_list = []
    a_q_x = (2 * ip_dot_list[0][0] - 5 * ip_dot_list[1][0] + 4 * ip_dot_list[2][0] - ip_dot_list[3][0]) / (step ** 2)
    a_q_y = (2 * ip_dot_list[0][1] - 5 * ip_dot_list[1][1] + 4 * ip_dot_list[2][1] - ip_dot_list[3][1]) / (step ** 2)
    a_list.append([a_q_x, a_q_y])
    for i in range(1, len(ip_dot_list) - 1):
        a_q_x = (ip_dot_list[i - 1][0] - 2 * ip_dot_list[i][0] + 1 * ip_dot_list[i + 1][0]) / (step ** 2)
        a_q_y = (ip_dot_list[i - 1][1] - 2 * ip_dot_list[i][1] + 1 * ip_dot_list[i + 1][1]) / (step ** 2)
        a_list.append([a_q_x, a_q_y])
    a_q_x = (- ip_dot_list[-4][0] + 4 * ip_dot_list[-3][0] - 5 * ip_dot_list[-2][0] + 2 * ip_dot_list[-1][0]) / (step ** 2)
    a_q_x = (- ip_dot_list[-4][1] + 4 * ip_dot_list[-3][1] - 5 * ip_dot_list[-2][1] + 2 * ip_dot_list[-1][1]) / (step ** 2)
    a_list.append([a_q_x, a_q_y])
    return a_list
