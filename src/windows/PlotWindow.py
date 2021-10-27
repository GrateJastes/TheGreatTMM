from PyQt5.QtWidgets import QWidget, QVBoxLayout

from src.qt.gen.PlotWidget import Ui_plotWindow


class PlotWindow(Ui_plotWindow, QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def heightForWidth(self, a0: int) -> int:
        return a0
