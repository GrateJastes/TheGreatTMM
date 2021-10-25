import sys

from PyQt5 import QtWidgets

from src.windows.MainWindow import WindowMaker


# def main():
#     mech = Mechanism('assets/video/camera/mech_4_2.mp4', consts.DebugMode.DEBUG_OFF)
#     mech.set_new_link(consts.BGR.RED, [common.Point('A', True)], True)
#     mech.set_new_link(consts.BGR.BLUE, [common.Point('B', False)], False)
#
#     mech.research_input()
#
#     pathA = mech.initial_link.points[0].path.dots
#     for idx, dot in enumerate(pathA):
#         if idx == 0:
#             continue
#         if math.sqrt((dot.x - pathA[idx - 1].x) ** 2 + (dot.y - pathA[idx - 1].y) ** 2) > 10:
#             pathA.remove(dot)
#     plt.plot([dot.x for dot in pathA], [dot.y for dot in pathA])
#     plt.show()
#     cv2.waitKey(0)


def main():
    app = QtWidgets.QApplication(sys.argv)

    window_maker = WindowMaker()
    window = window_maker.make_main_window()
    window.show()

    app.exec_()


if __name__ == '__main__':
    main()
