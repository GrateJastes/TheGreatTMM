import sys

from PyQt5 import QtWidgets

from src.windows.MainWindow import WindowMaker


def main():
    app = QtWidgets.QApplication(sys.argv)

    window_maker = WindowMaker()
    window = window_maker.make_main_window()
    window.show()

    app.quit()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
