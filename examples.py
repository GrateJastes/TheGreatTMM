import math
import sys

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

    mech = Mechanism('assets/video/camera/mech_1_1.mp4', consts.DebugMode.DEBUG_OFF)
    mech.set_new_link(consts.BGR.RED, [common_entities.Point('A', True)], True)
    mech.set_new_link(consts.BGR.BLUE, [common_entities.Point('B', False)], False)

    mech.research_input()
    pathA = mech.initial_link.points[0].path.dots
    remove_jumps(pathA)

    # win = PathWindow()
    # # win.setGeometry(500, 500, 600, 600)
    # plot_widget = pg.GraphicsLayoutWidget(show=True)
    # # plot_widget.resize(600, 600)
    # pg.setConfigOptions(antialias=True)
    #
    # plot_widget.addPlot(title='Point A path', x=[dot.x for dot in pathA], y=[dot.y for dot in pathA])
    # win.verticalLayout.addWidget(plot_widget)
    #
    # win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    # main()
    examples()
