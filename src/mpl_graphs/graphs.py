import math

import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import InterpolatedUnivariateSpline

from src.diff import diff_utils


def print_path(*points):
    plt.title('Траектории точек')
    for point in points:
        plt.plot([dot.x for dot in point.path.dots], [dot.y for dot in point.path.dots], label=point.name)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True)
    plt.legend(fontsize=10)
    plt.show()


def spline_analog(omegai, yi):
    omega = np.linspace(0, 2 * math.pi, 100)
    s = InterpolatedUnivariateSpline(omegai, yi, k=2)
    return s(omega)


def print_analog_v(step, *points):
    # omega = np.linspace(0, 2 * math.pi, 100)
    plt.subplot(211)
    plt.title('Цикловые графики аналогов скоростей')
    for point in points:
        f = diff_utils.polinom([item * step for item in range(len(point.speed))],
                               [unit.x for unit in point.speed])
        plt.plot([item * step for item in range(len(point.speed))],
                 [f(om) for om in [item * step for item in range(len(point.speed))]], label=point.name)
        # plt.plot(omega, spline_analog([item * step for item in range(len(point.speed))],
        #                               [unit.x for unit in point.speed]))
    plt.ylabel("v_x")
    plt.grid(True)
    plt.legend(fontsize=10)

    plt.subplot(212)
    for point in points:
        f = diff_utils.polinom([item * step for item in range(len(point.speed))],
                               [unit.y for unit in point.speed])
        plt.plot([item * step for item in range(len(point.speed))],
                 [f(om) for om in [item * step for item in range(len(point.speed))]], label=point.name)
        # plt.plot(omega, spline_analog([item * step for item in range(len(point.speed))],
        #                               [unit.y for unit in point.speed]))
    plt.xlabel("phi")
    plt.ylabel("v_y")
    plt.grid(True)
    plt.legend(fontsize=10)

    plt.show()


def print_analog_a(step, *points):
    # omega = np.linspace(0, 2 * math.pi, 100)
    plt.subplot(211)
    plt.title('Цикловые графики аналогов ускорений')
    for point in points:
        f = diff_utils.polinom([item * step for item in range(len(point.acceleration))],
                               [unit.x for unit in point.acceleration])
        plt.plot([item * step for item in range(len(point.acceleration))],
                 [f(om) for om in [item * step for item in range(len(point.acceleration))]], label=point.name)
        # plt.plot(omega, spline_analog([item * step for item in range(len(point.acceleration))],
        #                               [unit.x for unit in point.acceleration]))
    plt.ylabel("a_x")
    plt.grid(True)
    plt.legend(fontsize=10)

    plt.subplot(212)
    for point in points:
        f = diff_utils.polinom([item * step for item in range(len(point.acceleration))],
                               [unit.y for unit in point.acceleration])
        plt.plot([item * step for item in range(len(point.acceleration))],
                 [f(om) for om in [item * step for item in range(len(point.acceleration))]], label=point.name)
        # plt.plot(omega, spline_analog([item * step for item in range(len(point.acceleration))],
        #                               [unit.y for unit in point.acceleration]))
    plt.xlabel("phi")
    plt.ylabel("a_y")
    plt.grid(True)
    plt.legend(fontsize=10)

    plt.show()
