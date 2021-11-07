import math

import findiff
import numpy as np
from scipy import interpolate
from scipy.optimize import curve_fit

from src import common_entities
from src.common_entities.Unit import Unit
from src.diff import consts


def linear_interpolate(point, base):
    ip_point = common_entities.Point(point.name + '(ip)')
    dot_list = []
    for i in np.arange(0, 2 * math.pi + consts.STEP_SPLITTING, consts.STEP_SPLITTING):
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
    ip_dot_list = linear_interpolate(point, base)
    v_list = [Unit(forward_difference_1(ip_dot_list, 'x'), forward_difference_1(ip_dot_list, 'y'))]
    for i in range(1, len(ip_dot_list.path.dots) - 1):
        v_list.append(Unit(central_difference_1(ip_dot_list, i, 'x'),
                           central_difference_1(ip_dot_list, i, 'y')))
    v_list.append(Unit(backward_difference_1(ip_dot_list, 'x'), backward_difference_1(ip_dot_list, 'y')))
    # v_list_pol = data_fit(v_list)
    v_list_pol = data_interpolate(v_list)
    # v_list_pol = v_list
    return v_list_pol


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
    ip_dot_list = linear_interpolate(point, base)
    a_list = [Unit(forward_difference_2(ip_dot_list, 'x'), forward_difference_2(ip_dot_list, 'y'))]
    for num in range(1, len(ip_dot_list.path.dots) - 1):
        a_list.append(Unit(central_difference_2(ip_dot_list, num, 'x'), central_difference_2(ip_dot_list, num, 'y')))
    a_list.append(Unit(backward_difference_2(ip_dot_list, 'x'), backward_difference_2(ip_dot_list, 'y')))
    # a_list_pol = data_fit(a_list)
    a_list_pol = data_interpolate(a_list)
    # a_list_pol = a_list
    return a_list_pol


# Returns a polynomial function of dependence of y on x
def polinom(x, y):
    z = np.polyfit(x, y, consts.DEGREE_OF_POLYNOMIAL)
    p = np.poly1d(z)
    return p


def data_fit(data_list):
    fx = polinom([item * consts.STEP_SPLITTING for item in range(len(data_list))],
                 [unit.x for unit in data_list])
    fy = polinom([item * consts.STEP_SPLITTING for item in range(len(data_list))],
                 [unit.y for unit in data_list])
    data_list_pol = []
    for i in range(len(data_list)):
        data_list_pol.append(Unit(fx(i * consts.STEP_SPLITTING), fy(i * consts.STEP_SPLITTING)))
    return data_list_pol


def diff2_fd(point, base):
    ip_dot_list = linear_interpolate(point, base)
    a_list = []
    d_do = findiff.FinDiff(0, consts.STEP_SPLITTING, 2, acc=4)
    x_array = np.array([dot.x for dot in ip_dot_list.path.dots])
    y_array = np.array([dot.y for dot in ip_dot_list.path.dots])
    dx_do = d_do(x_array)
    dy_do = d_do(y_array)
    for i in range(len(dx_do)):
        a_list.append(Unit(dx_do[i], dy_do[i]))
    a_list_pol = data_fit(a_list)
    return a_list_pol


def data_interpolate(data_list):
    omega_list = [item * consts.STEP_SPLITTING for item in range(len(data_list))]
    omega_int = np.linspace(omega_list[0], omega_list[-1], 200)
    tck_x = interpolate.splrep(omega_list, [unit.x for unit in data_list], k=3, s=1120)
    int_x = interpolate.splev(omega_int, tck_x, der=0)
    tck_y = interpolate.splrep(omega_list, [unit.y for unit in data_list], k=3, s=1120)
    int_y = interpolate.splev(omega_int, tck_y, der=0)
    data_list_pol = []
    for i in range(len(data_list)):
        data_list_pol.append(Unit(int_x[i], int_y[i]))
    return data_list_pol


def optimize_curve(data_list):
    # fx = polinom([item * consts.STEP_SPLITTING for item in range(len(data_list))],
    #              [unit.x for unit in data_list])
    omega_list = [item * consts.STEP_SPLITTING for item in range(len(data_list))]
    # fx = func_x(omega_list, data_list)
    poptx, pcovx = curve_fit(func_x, omega_list,
                             [unit.x for unit in data_list], p0=data_list)
    # fy = polinom([item * consts.STEP_SPLITTING for item in range(len(data_list))],
    #              [unit.y for unit in data_list])
    # fy = func_y(omega_list, data_list)
    popty, pcovy = curve_fit(func_y, omega_list,
                             [unit.y for unit in data_list], p0=data_list)
    data_list_pol = []
    for i in range(len(data_list)):
        data_list_pol.append(Unit(poptx[i], popty[i]))
    return data_list_pol


def func_y(omega, other_list):
    i = omega // consts.STEP_SPLITTING
    return other_list[i].y


def func_x(omega, other_list):
    i = omega // consts.STEP_SPLITTING
    return other_list[i].x
