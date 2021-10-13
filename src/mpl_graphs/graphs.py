import math

import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import InterpolatedUnivariateSpline


def print_path(*points):
    plt.title('Траектории точек')
    for point in points:
        plt.plot([dot.x for dot in point.path.dots], [dot.y for dot in point.path.dots])
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True)
    plt.show()


def spline_analog(omegai, yi):
    omega = np.linspace(0, 2 * math.pi, 100)
    s = InterpolatedUnivariateSpline(omegai, yi, k=2)
    return s(omega)


def print_analog(analog_type, step, *vectors):
    omega = np.linspace(0, 2 * math.pi, 100)
    plt.subplot(211)
    if analog_type == 'v':
        plt.title('Цикловые графики аналогов скоростей')
    elif analog_type == 'a':
        plt.title('Цикловые графики аналогов ускорений')
    else:
        plt.title('Не введен тип аналога')
    for vector in vectors:
        plt.plot(omega, spline_analog([item * step for item in range(len(vector))], [dot[0] for dot in vector]))
    plt.ylabel("v_x")
    plt.grid(True)

    plt.subplot(212)
    for vector in vectors:
        plt.plot(omega, spline_analog([item * step for item in range(len(vector))], [dot[1] for dot in vector]))
    plt.xlabel("phi")
    plt.ylabel("v_y")
    plt.grid(True)

    plt.show()
