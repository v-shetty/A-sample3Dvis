import datetime
import random
import numpy as np
from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


import Visualizer3D.main_app
import model.GlobalFile as globalfile

class MockUp(QMainWindow):

    sigNewDataArrived = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.pushbutton = QPushButton("Open Window")
        self.pushbutton.setObjectName("pb1")

        self.setCentralWidget(self.pushbutton)
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._timer_cb)
        self._timer.start(100)
        self.sigNewDataArrived.connect(self.on_sigNewDataArrived)
        self.visapp = None
        QMetaObject.connectSlotsByName(self)

    @pyqtSlot()
    def on_pb1_clicked(self):
        if self.visapp is None:
            self.visapp = Visualizer3D.main_app.App()
            self.visapp.main_view.show()
            self.sigNewDataArrived.connect(self.visapp.main_view.newDataArrive)
        else:
            self.visapp.main_view.show()


    @pyqtSlot()
    def on_sigNewDataArrived(self):

        print(f"{datetime.datetime.now().isoformat()} {id(globalfile.data2D)}")


    def _timer_cb(self):
        globalfile.data2D = (200*np.random.rand(116,256),np.random.rand(116,256),np.random.rand(116,256))
        print(f"{datetime.datetime.now().isoformat()} {id(globalfile.data2D)}")
        self.sigNewDataArrived.emit()

if __name__ == '__main__':
    app = QApplication([])

    mock = MockUp()
    mock.show()

    app.exec_()