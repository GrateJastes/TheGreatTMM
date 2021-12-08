import sys

import numpy as np
from PyQt5 import QtWidgets

from src.common_entities import Point
from src.common_entities.mechanism.Mechanism import Mechanism
from src.cv_module import consts
from src.windows.MainWindow import WindowMaker
import pyqtgraph as pg



def main():
    # cv2.aruco.detectMarkers()
    app = QtWidgets.QApplication(sys.argv)

    window_maker = WindowMaker()
    window = window_maker.make_main_window()
    window.show()

    app.exec_()
    sys.exit()


def test():
    mech = Mechanism('assets/video/multi_2.mp4')
    mech.set_new_link(consts.BGR.BLUE, [Point('A', False), Point('B', False)], False, 0)
    mech.set_new_link(consts.BGR.RED, [Point('C', False)], True, 1)

    mech.research_input()

    app = pg.mkQApp('Exp')
    win = pg.GraphicsLayoutWidget(show=True, title="title")
    win.resize(1000, 600)

    p1 = win.addPlot(title='paths')

    Ax = mech.links[0].points[0].get_coord_for_plot('x')
    Ay = mech.links[0].points[0].get_coord_for_plot('y')
    Bx = mech.links[0].points[1].get_coord_for_plot('x')
    By = mech.links[0].points[1].get_coord_for_plot('y')

    p1.plot(
        x=Ax,
        y=Ay,
        pen=pg.mkPen(consts.BGR.RED, width=1),
    )

    p1.plot(
        x=Bx,
        y=By,
        pen=pg.mkPen(consts.BGR.BLUE, width=1),
    )

    pg.exec()


if __name__ == '__main__':
    main()
    # test()
