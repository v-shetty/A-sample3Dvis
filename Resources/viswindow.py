# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'viswindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_viswindow(object):
    def setupUi(self, viswindow):
        viswindow.setObjectName("viswindow")
        viswindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(viswindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(510, 140, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.datavis = QtWidgets.QWidget(self.centralwidget)
        self.datavis.setGeometry(QtCore.QRect(79, 89, 391, 341))
        self.datavis.setObjectName("datavis")
        viswindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(viswindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        viswindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(viswindow)
        self.statusbar.setObjectName("statusbar")
        viswindow.setStatusBar(self.statusbar)

        self.retranslateUi(viswindow)
        QtCore.QMetaObject.connectSlotsByName(viswindow)

    def retranslateUi(self, viswindow):
        _translate = QtCore.QCoreApplication.translate
        viswindow.setWindowTitle(_translate("viswindow", "MainWindow"))
        self.pushButton.setText(_translate("viswindow", "vis"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    viswindow = QtWidgets.QMainWindow()
    ui = Ui_viswindow()
    ui.setupUi(viswindow)
    viswindow.show()
    sys.exit(app.exec_())
