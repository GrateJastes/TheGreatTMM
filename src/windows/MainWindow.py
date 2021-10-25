import math
import os
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QApplication
from matplotlib import pyplot as plt

from src.common_entities import Point
from src.common_entities.mechanism.Link import Link
from src.qt.gen.ApplicationUI import Ui_MainWindow
from src.common_entities.mechanism.Mechanism import Mechanism
from src.cv_module.consts import BGR


def get_color_name(russian_name: str) -> tuple:
    return {
        'Красный': BGR.RED,
        'Синий': BGR.BLUE,
        'Зелёный': BGR.GREEN,
    }.get(russian_name)


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.form_links = []
        self.link_colors = []
        self.link_names = []
        self.link_points = []
        self.initial_links = []
        self.mechanism = Mechanism('')

        self.startResearchButton.clicked.connect(self.start_research)
        self.trajectoryButton.clicked.connect(self.show_trajectory)

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
        self.back_button_4.clicked.connect(self.prev_page)

    def set_upload_logic(self):
        self.next_button_2.hide()
        self.fileErrorMessage.hide()

        self.videoFilePath.textChanged.connect(self.check_provided_video)

        self.browse_button.clicked.connect(self.browse_files)

    def set_links_form_logic(self):
        self.form_links = [
            self.linkForm_1,
            self.linkForm_2,
            self.linkForm_3,
            self.linkForm_4,
            self.linkForm_5,
            self.linkForm_6,
        ]

        self.link_colors = [
            self.link_1_color,
            self.link_2_color,
            self.link_3_color,
            self.link_4_color,
            self.link_5_color,
            self.link_6_color,
        ]

        self.link_points = [
            self.link_1_points,
            self.link_2_points,
            self.link_3_points,
            self.link_4_points,
            self.link_5_points,
            self.link_6_points,
        ]

        self.link_names = [
            self.link_1_letter,
            self.link_2_letter,
            self.link_3_letter,
            self.link_4_letter,
            self.link_5_letter,
            self.link_6_letter,
        ]

        self.initial_links = [
            self.link_1_initial,
            self.link_2_initial,
            self.link_3_initial,
            self.link_4_initial,
            self.link_5_initial,
            self.link_6_initial,
        ]

        for link in self.form_links:
            link.hide()

        self.linksNumber.currentTextChanged.connect(self.update_link_forms)

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
        filename = QFileDialog.getOpenFileName(self, 'Open video', os.getcwd(), 'Video (*.mp4 *.avi)')
        if filename != '':
            self.videoFilePath.setText(filename[0])

    def check_provided_video(self):
        filename = self.videoFilePath.text()
        video_ok = Mechanism.video_fits(filename)

        if video_ok:
            self.next_button_2.show()
            self.fileErrorMessage.hide()
        else:
            self.fileErrorMessage.show()

    def update_link_forms(self):
        last_link_number = self.linksNumber.currentIndex() + 1

        for link in self.form_links:
            link.hide()

        for i in range(last_link_number):
            self.form_links[i].show()

    def collect_links_data(self) -> [Link]:
        links = []
        link_names = [field.currentText() for field in self.link_names]
        link_colors = [get_color_name(field.currentText()) for field in self.link_colors]
        links_initial = [field.isChecked() for field in self.initial_links]
        link_points = [int(field.value()) for field in self.link_points]
        last_link_number = self.linksNumber.currentIndex() + 1

        for i in range(last_link_number):
            name = link_names[i]
            point_names = ['%s%d' % (name, index) for index in range(link_points[i])]
            points = [Point(point_name, links_initial[i]) for point_name in point_names]
            links.append(Link(link_colors[i], points, links_initial[i]))

        return links

    def start_research(self):
        self.mechanism = Mechanism(self.videoFilePath.text())
        links = self.collect_links_data()
        for link in links:
            self.mechanism.set_new_link(link.color, link.points, link.is_initial)

        self.mechanism.research_input()

    def show_trajectory(self):
        pathA = self.mechanism.initial_link.points[0].path.dots
        for idx, dot in enumerate(pathA):
            if idx == 0:
                continue
            if math.sqrt((dot.x - pathA[idx - 1].x) ** 2 + (dot.y - pathA[idx - 1].y) ** 2) > 10:
                pathA.remove(dot)
        plt.plot([dot.x for dot in pathA], [dot.y for dot in pathA])
        plt.show()


class WindowMaker(object):
    def __init__(self):
        self.window = MainWindow()

    def make_main_window(self) -> MainWindow:
        self.window.set_screen_geometry()
        self.window.set_navigation()
        self.window.set_upload_logic()
        self.window.set_links_form_logic()

        return self.window

