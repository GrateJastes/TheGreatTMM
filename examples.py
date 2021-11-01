import math
import sys

from cv2 import cv2

import pyqtgraph as pg
import pyqtgraph.examples
# pyqtgraph.examples.run()
from PyQt5 import QtWidgets

from src import common_entities
from src.common_entities import Dot
from src.common_entities.mechanism.Mechanism import Mechanism
from src.cv_module import consts
from src.cv_module.cv_utils import remove_jumps


def examples():
    pg.examples.run()


def main():
    app = QtWidgets.QApplication(sys.argv)

    mech = Mechanism('assets/video/camera/mech_4_1.mp4')
    mech.set_new_link(consts.BGR.RED, [common_entities.Point('A', True)], True)
    mech.set_new_link(consts.BGR.BLUE, [common_entities.Point('B', False)], False)

    mech.research_input()
    pathA = mech.initial_link.points[0].path.dots
    remove_jumps(pathA)

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
    # examples()
