from __future__ import annotations

import os

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QFileDialog, QApplication, QMessageBox, QWidget, QVBoxLayout, QLabel, QHBoxLayout, \
    QPushButton, QComboBox, QCheckBox, QSpinBox

from src.common_entities import Point
from src.common_entities.mechanism.Link import Link
from src.cv_module import consts
from src.qt.QHline import QHLine
from src.qt.gen.ApplicationUI import Ui_MainWindow
from src.common_entities.mechanism.Mechanism import Mechanism
from src.cv_module.consts import BGR
from src.windows.DisplayImageWidget import DisplayImageWidget
from src.windows.PlotWindow import PlotWindow
import pyqtgraph as pg


def get_color_name(russian_name: str) -> tuple:
    return {
        'Красный': BGR.RED,
        'Синий': BGR.BLUE,
        'Зелёный': BGR.GREEN,
        'Желтый': BGR.YELLOW,
    }.get(russian_name)


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    form_links: list[QWidget]
    link_color_fields: list[QComboBox]
    link_name_fields: list[QComboBox]
    initial_link_checks: list[QCheckBox]
    link_point_counters: list[QSpinBox]
    plot_path_windows: list[QWidget]
    plot_speed_windows: list[QWidget]
    mechanism: Mechanism
    preview_window: DisplayImageWidget | None

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('The Great TMM')

        self.plot_path_windows = []
        self.plot_speed_windows = []

        self.researchPathsButton.clicked.connect(self.set_trajectories_page)
        self.researchAnalogs.clicked.connect(self.set_speeds_page)

        self.preview_window = None

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        if self.preview_window is not None:
            self.preview_window.destroy()
        for window in self.plot_path_windows + self.plot_speed_windows:
            window.destroy()

        a0.accept()

    def set_screen_geometry(self) -> None:
        screen_geometry = QApplication.desktop().screenGeometry()
        x = (screen_geometry.width() - self.width()) / 2
        y = (screen_geometry.height() - self.height()) / 2
        self.move(x, y)

    # noinspection DuplicatedCode
    def set_navigation(self) -> None:
        self.stackedWidget.setCurrentIndex(0)

        self.next_button_1.clicked.connect(self.next_page)
        self.next_button_2.clicked.connect(self.next_page)
        self.next_button_3.clicked.connect(self.proceed_if_links_ok)
        self.next_button_4.clicked.connect(self.next_page)
        self.next_button_5.clicked.connect(self.next_page)

        self.back_button_2.clicked.connect(self.prev_page)
        self.back_button_3.clicked.connect(self.prev_page)
        self.back_button_4.clicked.connect(self.prev_page)
        self.back_button_5.clicked.connect(self.prev_page)
        self.back_button_6.clicked.connect(self.prev_page)

        self.next_button_5.hide()
        self.next_button_6.hide()

    def set_upload_logic(self) -> None:
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

        self.link_color_fields = [
            self.link_1_color,
            self.link_2_color,
            self.link_3_color,
            self.link_4_color,
            self.link_5_color,
            self.link_6_color,
        ]

        self.link_point_counters = [
            self.link_1_points,
            self.link_2_points,
            self.link_3_points,
            self.link_4_points,
            self.link_5_points,
            self.link_6_points,
        ]

        self.link_name_fields = [
            self.link_1_letter,
            self.link_2_letter,
            self.link_3_letter,
            self.link_4_letter,
            self.link_5_letter,
            self.link_6_letter,
        ]

        self.initial_link_checks = [
            self.link_1_initial,
            self.link_2_initial,
            self.link_3_initial,
            self.link_4_initial,
            self.link_5_initial,
            self.link_6_initial,
        ]

        for link in self.form_links:
            link.hide()
        self.form_links[0].show()
        self.link_1_initial.setChecked(True)
        self.check_initial_boxes()

        for check_box in self.initial_link_checks:
            check_box.stateChanged.connect(self.check_initial_boxes)

        self.linksNumber.currentTextChanged.connect(self.update_link_forms)

    def set_research_screen(self) -> None:
        self.startResearchButton.clicked.connect(self.start_research)

        self.readyLabel.hide()
        self.next_button_4.hide()
        self.next_button_4.clicked.connect(self.show_preview_window)

        self.progressBar.valueChanged.connect(self.show_ready_label)

    def next_page(self) -> None:
        curr_page_index = self.stackedWidget.currentIndex()
        if curr_page_index < self.stackedWidget.count() - 1:
            self.stackedWidget.setCurrentIndex(curr_page_index + 1)

    def prev_page(self) -> None:
        curr_page_index = self.stackedWidget.currentIndex()
        if curr_page_index > 0:
            self.stackedWidget.setCurrentIndex(curr_page_index - 1)

    def browse_files(self) -> None:
        filename = QFileDialog.getOpenFileName(self, 'Open video', os.getcwd(), 'Video (*.mp4 *.avi)')
        if filename != '':
            self.videoFilePath.setText(filename[0])

    def check_provided_video(self) -> None:
        filename = self.videoFilePath.text()
        video_ok = Mechanism.video_fits(filename)

        if video_ok:
            self.next_button_2.show()
            self.fileErrorMessage.hide()
        else:
            self.fileErrorMessage.show()

    def update_link_forms(self) -> None:
        last_link_index = self.linksNumber.currentIndex() + 1

        for link in self.form_links:
            link.hide()

        for i in range(last_link_index):
            self.form_links[i].show()

    def collect_links_data(self) -> [Link]:
        links = []
        link_names = [field.currentText() for field in self.link_name_fields]
        link_colors = [get_color_name(field.currentText()) for field in self.link_color_fields]
        links_initial = [field.isChecked() for field in self.initial_link_checks]
        links_amount_points = [int(field.value()) for field in self.link_point_counters]
        last_link_number = self.linksNumber.currentIndex() + 1

        for i in range(last_link_number):
            name = link_names[i]
            point_names = ['%s%d' % (name, index) for index in range(links_amount_points[i])]
            points = [Point(point_name, links_initial[i]) for point_name in point_names]
            links.append(Link(link_colors[i], points, links_initial[i], link_id=i + 1))

        return links

    def start_research(self):
        self.back_button_4.hide()
        self.mechanism = Mechanism(self.videoFilePath.text())
        links = self.collect_links_data()
        for link in links:
            self.mechanism.set_new_link(link.color, link.points, link.is_initial, link.link_id)

        self.mechanism.research_input(self.progressBar)

    def show_preview_window(self):
        self.preview_window = DisplayImageWidget()
        self.preview_window.show_image(self.mechanism.preview_image)
        self.preview_window.show()
        self.preview_window.setFixedSize(self.preview_window.size())

    def show_ready_label(self):
        if self.progressBar.value() == consts.PROGRESS_BAR_MAX:
            self.readyLabel.show()
            self.next_button_4.show()

    def check_initial_boxes(self):
        checked_index = None

        for i, check_box in enumerate(self.initial_link_checks):
            if check_box.isChecked():
                checked_index = i
                break

        if checked_index is None:
            for check_box in self.initial_link_checks:
                check_box.setEnabled(True)

            return

        for i, check_box in enumerate(self.initial_link_checks):
            if i == checked_index:
                continue

            check_box.setEnabled(False)

    def check_link_colors(self) -> bool:
        used_colors = []
        for color_combo in self.link_color_fields:
            if color_combo.parentWidget().isHidden():
                continue

            if color_combo.currentIndex() in used_colors:
                return False

            used_colors.append(color_combo.currentIndex())

        return True

    def proceed_if_links_ok(self):
        colors_ok = self.check_link_colors()

        if colors_ok:
            self.next_page()
        else:
            QMessageBox.about(
                self,
                'Недопустимые цвета!',
                'Пожалуйста, выберете разные цвета для используемых звеньев'
            )

    def set_trajectories_page(self):
        self.researchPathsButton.hide()
        self.add_link_activities(self.mechanism.initial_link, self.show_point_path, self.verticalLayout_11)
        self.next_button_5.show()

        for link in self.mechanism.links:
            self.add_link_activities(link, self.show_point_path, self.verticalLayout_11)

    def set_speeds_page(self):
        self.mechanism.research_analogs()
        self.researchAnalogs.hide()
        self.next_button_6.show()

        self.add_link_activities(self.mechanism.initial_link, self.show_point_speeds, self.verticalLayout_12)
        for link in self.mechanism.links:
            self.add_link_activities(link, self.show_point_speeds, self.verticalLayout_12)

    def show_point_path(self, point: Point):
        def show_path():
            base_point = self.mechanism.initial_link.points[0]
            plot_win = PlotWindow()
            plot_win.setWindowTitle('Точка %s' % point.name)
            plot_widget = pg.GraphicsLayoutWidget(show=True)
            pg.setConfigOptions(antialias=True)

            p0 = plot_widget.addPlot(title='Point %s path' % point.name)
            X = point.get_coord_for_plot('x')
            Y = point.get_coord_for_plot('y')

            point_plot = p0.plot(x=X,
                                 y=Y,
                                 pen=pg.mkPen(consts.BGR.RED, width=1))

            point_plot_ip = p0.plot(x=[dot.x for dot in point.interpolated_path(base_point).dots],
                                    y=[dot.y for dot in point.interpolated_path(base_point).dots],
                                    pen=pg.mkPen('r', width=4), 
                                    symbol='o')
            p0.setAspectLocked()
            legend = pg.LegendItem((80, 60))
            legend.setParentItem(p0)
            legend.addItem(point_plot, 'Распознанная траектория')
            legend.addItem(point_plot_ip, 'Преобразованная траектория')

            p0.showGrid(x=True, y=True)
            plot_win.verticalLayout.addWidget(plot_widget)

            self.plot_path_windows.append(plot_win)

            plot_win.show()

        return show_path

    def show_point_speeds(self, point: Point):
        def show_speeds():
            speed = point.speed
            speed_x = [unit.x for unit in speed]
            speed_y = [unit.y for unit in speed]
            angle = point.analog_angle()

            acceleration = point.acceleration
            acc_x = [unit.x for unit in acceleration]
            acc_y = [unit.y for unit in acceleration]

            win = pg.GraphicsLayoutWidget(show=True)
            win.setWindowTitle('Аналоги скорости и ускорения точки %s' % point.name)

            p1 = win.addPlot(title='Аналоги скорости')
            Vx_plot = p1.plot(y=speed_x, x=angle, name='Vx', pen=pg.mkPen(consts.BGR.RED, width=2))
            Vy_plot = p1.plot(y=speed_y, x=angle, name='Vy', pen=pg.mkPen(consts.BGR.GREEN, width=2))

            p1.showGrid(x=True, y=True)

            legend = pg.LegendItem((80, 60), offset=(70, 20))
            legend.setParentItem(p1)
            legend.addItem(Vx_plot, 'Vx')
            legend.addItem(Vy_plot, 'Vy')

            p2 = win.addPlot(title='Аналоги ускорения')
            ax_plot = p2.plot(y=acc_x, x=angle, name='ax', pen=pg.mkPen(consts.BGR.RED, width=2))
            ay_plot = p2.plot(y=acc_y, x=angle, name='ay', pen=pg.mkPen(consts.BGR.GREEN, width=2))

            p2.showGrid(x=True, y=True)

            legend = pg.LegendItem((80, 60), offset=(70, 20))
            legend.setParentItem(p2)
            legend.addItem(ax_plot, 'ax')
            legend.addItem(ay_plot, 'ay')

            self.plot_speed_windows.append(win)

            win.show()

        return show_speeds

    def add_link_activities(self, link: Link, activity_func, containing_widget: QWidget):
        name_text = 'Звено %d' % link.link_id
        if link.is_initial:
            name_text += '(Начальное):'
        else:
            name_text += ':'

        link_widget = QWidget()
        link_widget_vbox = QVBoxLayout()
        link_widget.setLayout(link_widget_vbox)
        link_widget_vbox.addWidget(QHLine())
        link_widget_vbox.addWidget(QLabel(name_text))

        for point in link.points:
            hbox = QHBoxLayout()
            link_widget_vbox.addLayout(hbox)
            show_button = QPushButton('Показать')
            show_button.clicked.connect(activity_func(point))
            hbox.addWidget(QLabel('Точка %s' % point.name))
            hbox.addWidget(show_button)
        containing_widget.addWidget(link_widget)
        link_widget.adjustSize()


class WindowMaker(object):
    def __init__(self):
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')
        self.window = MainWindow()

    def make_main_window(self) -> MainWindow:
        self.window.set_screen_geometry()
        self.window.set_navigation()
        self.window.set_upload_logic()
        self.window.set_links_form_logic()
        self.window.set_research_screen()

        return self.window
