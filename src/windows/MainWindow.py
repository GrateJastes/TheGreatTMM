import os
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QApplication

from qt.gen.ApplicationUI import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # self.next_button_2.hide()

        # self.videoFilePath.textChanged.connect(self.check_provided_video)

        self.browse_button.clicked.connect(self.browse_files)

    def set_screen_geometry(self):
        screen_geometry = QApplication.desktop().screenGeometry()
        x = (screen_geometry.width() - self.width()) / 2
        y = (screen_geometry.height() - self.height()) / 2
        self.move(x, y)

    def set_navigation(self):
        self.stackedWidget.setCurrentIndex(0)

        self.next_button_1.clicked.connect(self.next_page)
        self.next_button_2.clicked.connect(self.next_page)
        self.next_button_3.clicked.connect(self.next_page)

        self.back_button_2.clicked.connect(self.prev_page)
        self.back_button_3.clicked.connect(self.prev_page)

    def show_upload_next_btn(self):
        self.next_button_2.show()

    def next_page(self):
        curr_page_index = self.stackedWidget.currentIndex()
        if curr_page_index < self.stackedWidget.count() - 1:
            self.stackedWidget.setCurrentIndex(curr_page_index + 1)

    def prev_page(self):
        curr_page_index = self.stackedWidget.currentIndex()
        if curr_page_index > 0:
            self.stackedWidget.setCurrentIndex(curr_page_index - 1)

    def browse_files(self):
        file_name = QFileDialog.getOpenFileName(self, 'Open video', os.getcwd(), 'Video (*.mp4 *.avi)')
        if file_name != '':
            self.videoFilePath.setText(file_name[0])


class WindowMaker(object):
    def __init__(self):
        self.window = MainWindow()

    def make_main_window(self) -> MainWindow:
        self.window.set_screen_geometry()
        self.window.set_navigation()

        return self.window

