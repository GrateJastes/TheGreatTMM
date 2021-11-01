from PyQt5.QtWidgets import QWidget, QSlider, QLabel

from src.qt.gen.HSVSettingsUI import Ui_HSVSettings


class HSVSettingsWindow(Ui_HSVSettings, QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.setupUi(self)
        self.main_window = main_window
        self.updateButton.clicked.connect(main_window.update_hsv)
        # self.closeButton.clicked.connect()

        self.horizontalSlider_1.valueChanged.connect(self.get_tracker_updater(self.horizontalSlider_1, self.label_7))
        self.horizontalSlider_2.valueChanged.connect(self.get_tracker_updater(self.horizontalSlider_2, self.label_8))
        self.horizontalSlider_3.valueChanged.connect(self.get_tracker_updater(self.horizontalSlider_3, self.label_9))
        self.horizontalSlider_4.valueChanged.connect(self.get_tracker_updater(self.horizontalSlider_4, self.label_10))
        self.horizontalSlider_5.valueChanged.connect(self.get_tracker_updater(self.horizontalSlider_5, self.label_11))
        self.horizontalSlider_6.valueChanged.connect(self.get_tracker_updater(self.horizontalSlider_6, self.label_12))

    def get_trackers_info(self) -> dict:
        return {
            'h1': self.horizontalSlider_1.value(),
            's1': self.horizontalSlider_2.value(),
            'v1': self.horizontalSlider_3.value(),
            'h2': self.horizontalSlider_4.value(),
            's2': self.horizontalSlider_5.value(),
            'v2': self.horizontalSlider_6.value(),
        }

    def set_trackers_values(self, bounds: tuple):
        self.horizontalSlider_1.setValue(bounds[0][0])
        self.horizontalSlider_2.setValue(bounds[0][1])
        self.horizontalSlider_3.setValue(bounds[0][2])
        self.horizontalSlider_4.setValue(bounds[1][0])
        self.horizontalSlider_5.setValue(bounds[1][1])
        self.horizontalSlider_6.setValue(bounds[1][2])

    def get_tracker_updater(self, tracker: QSlider, label: QLabel):
        def tracker_updater():
            label.setText('%d' % tracker.value())

        return tracker_updater
