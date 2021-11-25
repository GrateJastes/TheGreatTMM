from PyQt5 import QtGui, QtWidgets
from PyQt5.QtGui import QImage


class DisplayImageWidget(QtWidgets.QWidget):
    image: QImage

    def __init__(self, parent=None):
        super(DisplayImageWidget, self).__init__(parent)
        self.setWindowTitle('Предпросмотр')
        # self.setMaximumSize(600, 340)
        # self.setMinimumSize(600, 340)

        self.image_frame = QtWidgets.QLabel()

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.image_frame)
        self.setLayout(self.layout)

    def show_image(self, cv_image):
        self.image = QtGui.QImage(
            cv_image.data,
            cv_image.shape[1],
            cv_image.shape[0],
            QtGui.QImage.Format_RGB888,
        ).rgbSwapped()

        self.image_frame.setPixmap(QtGui.QPixmap.fromImage(self.image))
        self.image_frame.adjustSize()
