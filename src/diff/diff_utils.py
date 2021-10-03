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