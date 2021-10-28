# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/qt/ui/plot.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_plotWindow(object):
    def setupUi(self, plotWindow):
        plotWindow.setObjectName("plotWindow")
        plotWindow.resize(600, 600)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(plotWindow.sizePolicy().hasHeightForWidth())
        plotWindow.setSizePolicy(sizePolicy)
        self.verticalLayout = QtWidgets.QVBoxLayout(plotWindow)
        self.verticalLayout.setObjectName("verticalLayout")

        self.retranslateUi(plotWindow)
        QtCore.QMetaObject.connectSlotsByName(plotWindow)

    def retranslateUi(self, plotWindow):
        _translate = QtCore.QCoreApplication.translate
        plotWindow.setWindowTitle(_translate("plotWindow", "Form"))
