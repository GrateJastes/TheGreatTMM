import sys

from PyQt5 import QtWidgets

from src.cv_module import consts
from src.windows.MainWindow import WindowMaker


def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == 'debug':
            consts.DEBUG = True
    app = QtWidgets.QApplication(sys.argv)

    window_maker = WindowMaker()
    window = window_maker.make_main_window()
    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
