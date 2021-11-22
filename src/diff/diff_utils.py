import math

import numpy as np
from scipy import interpolate
from scipy.interpolate import splprep, splev

from src import common_entities
from src.common_entities.Unit import Unit
from src.diff import consts

from sympy import lambdify
from sympy.abc import u

import numpy as np
from matplotlib import pyplot as plt
from scipy import interpolate
from sympy import interpolating_spline
from scipy.misc import derivative


def crop_path(point, base):
    x = [dot.x for dot in point.path.dots]
    y = [dot.y for dot in point.path.dots]
    base_x = [dot.x for dot in base.path.dots]
    base_y = [dot.y for dot in base.path.dots]
    base_omega = [dot.omega for dot in base.path.dots]
    i = consts.NUM_OF_STEPS_FROM_START
    while ((i != len(base_x))
           and ((base_x[i] <= base_x[0] - consts.SHOOTING_ERROR)
                or (base_x[i] >= base_x[0] + consts.SHOOTING_ERROR)
                or (base_y[i] <= base_y[0] - consts.SHOOTING_ERROR)
                or (base_y[i] >= base_y[0] + consts.SHOOTING_ERROR))):
        i += 1
    x = x[:(i + 1)]
    y = y[:(i + 1)]
    base_x = base_x[:(i + 1)]
    base_y = base_y[:(i + 1)]
    base_omega = base_omega[:(i + 1)]
    return x, y, base_omega


def path_smoothing(point, base):
    if point.name == base.name:
        smoothing_order = consts.BASE_SMOOTH_ORDER
    else:
        smoothing_order = consts.POINT_SMOOTH_ORDER
    ip_point = common_entities.Point(point.name + '(ip)')
    dot_list = []
    point.remove_dot_repeat()
    base.remove_dot_repeat()
    x, y, base_omega = crop_path(point, base)
    omega, subject = sort_addiction(base_omega, x)
    coords_poly(omega,subject)
    x.append(x[0])
    y.append(y[0])
    xy = [x, y]
    tck_x, ux = splprep(xy, s=smoothing_order, per=True)
    new_points = splev(ux, tck_x)
    i = 0
    while i < len(new_points[0]):
        dot_list.append(common_entities.Dot(new_points[0][i], new_points[1][i]))
        i += 1
    ip_point.path.dots = dot_list
    return ip_point


def linear_interpolate(point, base):
    temp_base = path_smoothing(base, base)
    temp_point = path_smoothing(point, base)
    temp_omega = [math.atan2(temp_base.path.dots[i].y,
                             temp_base.path.dots[i].x) for i in range(len(temp_base.path.dots))]
    new_dots = []
    for i in np.arange(0, 2 * np.pi + consts.STEP_SPLITTING, consts.STEP_SPLITTING):
        new_dots.append(common_entities.Dot(np.interp(i,
                                                      temp_omega,
                                                      [dot.x for dot in temp_point.path.dots],
                                                      period=2 * np.pi),
                                            np.interp(i,
                                                      temp_omega,
                                                      [dot.y for dot in temp_point.path.dots],
                                                      period=2 * np.pi)))
    ip_point = common_entities.Point(point.name + '(ip.)')
    ip_point.path.dots = new_dots
    return ip_point


def central_difference_1(ip_point, num, type_of_coord):
    difference = None
    if type_of_coord == 'x':
        difference = (-0.5 * ip_point.path.dots[num - 1].x + 0.5 * ip_point.path.dots[
            num + 1].x) / consts.STEP_SPLITTING
    elif type_of_coord == 'y':
        difference = (-0.5 * ip_point.path.dots[num - 1].y + 0.5 * ip_point.path.dots[
            num + 1].y) / consts.STEP_SPLITTING
    return difference


def extreme_difference_1(ip_point, type_of_coord):
    difference = None
    if type_of_coord == 'x':
        difference = (-0.5 * ip_point.path.dots[-2].x + 0.5 * ip_point.path.dots[1].x) / consts.STEP_SPLITTING
    elif type_of_coord == 'y':
        difference = (-0.5 * ip_point.path.dots[-2].y + 0.5 * ip_point.path.dots[1].y) / consts.STEP_SPLITTING
    return difference


# First-order differentiation (enables smoothing of results)
def diff1(point, base):
    ip_dot_list = linear_interpolate(point, base)
    v_list = [Unit(extreme_difference_1(ip_dot_list, 'x'), extreme_difference_1(ip_dot_list, 'y'))]
    for i in range(1, len(ip_dot_list.path.dots) - 1):
        v_list.append(Unit(central_difference_1(ip_dot_list, i, 'x'),
                           central_difference_1(ip_dot_list, i, 'y')))
    v_list.append(Unit(extreme_difference_1(ip_dot_list, 'x'), extreme_difference_1(ip_dot_list, 'y')))
    v_list_pol = data_fit(v_list)
    # v_list_pol = v_list
    return v_list_pol


def diff1_without_fit(point, base):
    ip_dot_list = linear_interpolate(point, base)
    v_list = [Unit(extreme_difference_1(ip_dot_list, 'x'), extreme_difference_1(ip_dot_list, 'y'))]
    for i in range(1, len(ip_dot_list.path.dots) - 1):
        v_list.append(Unit(central_difference_1(ip_dot_list, i, 'x'),
                           central_difference_1(ip_dot_list, i, 'y')))
    v_list.append(Unit(extreme_difference_1(ip_dot_list, 'x'), extreme_difference_1(ip_dot_list, 'y')))
    return v_list


def central_difference_2(ip_point, num, type_of_coord):
    difference = None
    if type_of_coord == 'x':
        difference = (ip_point.path.dots[num - 1].x - 2 * ip_point.path.dots[num].x
                      + 1 * ip_point.path.dots[num + 1].x) / (consts.STEP_SPLITTING ** 2)
    elif type_of_coord == 'y':
        difference = (ip_point.path.dots[num - 1].y - 2 * ip_point.path.dots[num].y
                      + 1 * ip_point.path.dots[num + 1].y) / (consts.STEP_SPLITTING ** 2)
    return difference


# Returns the value of the derivative for the first and last parameters, provided they are equal
def extreme_difference_2(ip_point, type_of_coord):
    difference = None
    if type_of_coord == 'x':
        difference = (ip_point.path.dots[-2].x - 2 * ip_point.path.dots[-1].x
                      + 1 * ip_point.path.dots[1].x) / (consts.STEP_SPLITTING ** 2)
    elif type_of_coord == 'y':
        difference = (ip_point.path.dots[-2].y - 2 * ip_point.path.dots[-1].y
                      + 1 * ip_point.path.dots[1].y) / (consts.STEP_SPLITTING ** 2)
    return difference


# Second-order differentiation (enables smoothing of results)
def diff2(point, base):
    ip_dot_list = linear_interpolate(point, base)
    a_list = [Unit(extreme_difference_2(ip_dot_list, 'x'), extreme_difference_2(ip_dot_list, 'y'))]
    for num in range(1, len(ip_dot_list.path.dots) - 1):
        a_list.append(Unit(central_difference_2(ip_dot_list, num, 'x'), central_difference_2(ip_dot_list, num, 'y')))
    a_list.append(Unit(extreme_difference_2(ip_dot_list, 'x'), extreme_difference_2(ip_dot_list, 'y')))
    a_list_pol = data_fit(a_list)
    # a_list_pol = a_list
    return a_list_pol


def diff2_without_fit(point, base):
    ip_dot_list = linear_interpolate(point, base)
    a_list = [Unit(extreme_difference_2(ip_dot_list, 'x'), extreme_difference_2(ip_dot_list, 'y'))]
    for num in range(1, len(ip_dot_list.path.dots) - 1):
        a_list.append(Unit(central_difference_2(ip_dot_list, num, 'x'), central_difference_2(ip_dot_list, num, 'y')))
    a_list.append(Unit(extreme_difference_2(ip_dot_list, 'x'), extreme_difference_2(ip_dot_list, 'y')))
    return a_list


# Returns a polynomial function of dependence of y on x
def polinom(x, y):
    z = np.polyfit(x, y, consts.DEGREE_OF_POLYNOMIAL)
    p = np.poly1d(z)
    return p


# Calculates the values of x and y projections from a polynomial functions fx, fy
def data_fit(data_list):
    fx = polinom([item * consts.STEP_SPLITTING for item in range(len(data_list))],
                 [unit.x for unit in data_list])
    fy = polinom([item * consts.STEP_SPLITTING for item in range(len(data_list))],
                 [unit.y for unit in data_list])
    data_list_pol = []
    for i in range(len(data_list)):
        data_list_pol.append(Unit(fx(i * consts.STEP_SPLITTING), fy(i * consts.STEP_SPLITTING)))
    return data_list_pol


def set_angle_addiction(point, base):
    point.remove_dot_repeat()
    base.remove_dot_repeat()
    x, y, base_omega = crop_path(point, base)
    x.append(x[0])
    y.append(y[0])
    print(len(x), x)
    print(len(y), y)
    print(len(base_omega), base_omega)
    base_omega.append(base_omega[0])
    # Формат вывода уточнить
    return [base_omega, x], [base_omega, y]


def sort_addiction(omega, subject):
    points = zip(omega, subject)
    points = sorted(points, key=lambda point: point[0])
    return zip(*points) # (base_omega, subject)

def coords_poly(omega, subject):
    plt.plot(omega, subject)
    print(omega[0], omega[-1])
    plt.show()
    f = polinom(omega, subject)
    us = np.linspace(- np.pi, np.pi, 100)
    temp = []
    for i in us:
        temp.append(derivative(f, i, dx=1e-6))
    print('5')
    plt.plot(us, temp)
    plt.show()
    temp2 = []
    for i in us:
        temp2.append(derivative(f, i, dx=1e-6, n=2))
    print('5')
    plt.plot(us, temp2)
    plt.show()
    return temp


def coords_smoothing(subject, omega):
    x = np.r_[omega, omega[0]]
    y = np.r_[subject, subject[0]]
    tck, u_ticks = interpolate.splprep([x, y], s=4000, per=True)
    xi, yi = interpolate.splev(np.linspace(0, 1, 1000), tck)
    us = [u_ticks[-3] - 1, u_ticks[-2] - 1, *u_ticks, u_ticks[1] + 1, u_ticks[2] + 1]
    xs = [*x[-3:-1], *x, *x[1:3]]
    ys = [*y[-3:-1], *y, *y[1:3]]
    interpx = interpolating_spline(tck[2], u, us, xs)
    interpy = interpolating_spline(tck[2], u, us, ys)
    fx = lambdify(u, interpx, modules=['numpy'])
    fy = lambdify(u, interpy, modules=['numpy'])
    us = np.linspace(0, 1, 100)
    plt.scatter(fx(us), fy(us), c=us, s=40, marker='o', cmap='tab10')  # label='sympy´s interpolating_spline'
    temp = []
    for i in us:
        temp.append(derivative(fx, i, dx=1e-6))
    plt.show()
    print('5')
    plt.plot(us, temp)
    plt.show()
