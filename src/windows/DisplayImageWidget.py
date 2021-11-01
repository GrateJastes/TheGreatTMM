from PyQt5 import QtGui, QtWidgets


class DisplayImageWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        self.image = None
        super(DisplayImageWidget, self).__init__(parent)
        self.setWindowTitle('Предпросмотр')

        self.image_frame = QtWidgets.QLabel()

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.image_frame)
        self.setLayout(self.layout)

    def show_image(self, cv_image):
        self.image = cv_image
        self.image = QtGui.QImage(self.image.data, self.image.shape[1], self.image.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()
        self.image_frame.setPixmap(QtGui.QPixmap.fromImage(self.image))
        self.image_frame.adjustSize()
