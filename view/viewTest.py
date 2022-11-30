from PyQt5.QtCore import pyqtSlot
from os import path
#from view.main_view_ui import Ui_MainWindow
from PyQt5.uic import loadUi
import os

from PyQt5.QtWidgets import (QMainWindow, QFileDialog, QTableWidgetItem)

import numpy as np
from controller.Setting import Setting
import time
from os.path import join
import model.GlobalFile as globalfile

# self.ui = loadUi(str(os.getcwd() + '\\Resources\\VisGUI.ui'), self)
from controller.RecvTemp import RecvTemp, RecvTempThread, print_temp, temp_thread_complete
from controller.GalvoControl import GalvoControl , Run_Galvo, Print_Galvo, Exit_Glavo
from controller.LaserControl import LaserControl , Run_Laser , Print_Laser , Exit_Laser
from controller.PowerControl import RecvPowerBoardThread, PowerControl, Print_PowerBoard, Exit_PowerBoard
from controller.APIControl import Acquire , AcquireThread , print_Acquire, Acquire_thread_complete


from PyQt5.QtGui import *

from PyQt5 import QtCore, QtGui

class MainView(QMainWindow):
    def __init__(self, model, main_controller):
        super().__init__()
        self._model = model
        self._main_controller = main_controller


        #self.ui = Ui_MainWindow()
        #self.ui.setupUi()
        self.ui = loadUi(str(os.getcwd() + '//Resources//TestGUI.ui'), self)

        self.setting = Setting(self.ui)

        ####################################################################
        #   connect widgets to controllers
        ####################################################################
        # open file buttons
        #self._ui.pushButton.clicked.connect(self.open_file_name_dialog)

        ####################################################################
        #   listen for model event signals
        ####################################################################
        # file name is updated
        #self._model.file_name_changed.connect(self.on_file_name_changed)

        ###############Logo Update###################
        pixmap = QPixmap(os.getcwd() + '//Resources//ScantinelLogo.jpg'  )
        #self.ui.la_logo.setPixmap(pixmap)

        app_icon = QtGui.QIcon()
        app_icon.addFile(os.getcwd() + '//Resources//ScanLogo.jpg', QtCore.QSize(500, 500))
        self.ui.setWindowIcon(app_icon)

        self.ui.setGeometry(500, 150, 650, 650)





    def startacquire(self):
        self.AcquireThread()



    def Acquire_Progress(self):
        print("Acquire thread prgress")

    def AcquireThread(self):
        print(" API Client Started")

        worker = Acquire(AcquireThread) # Any other args, kwargs are passed to the run function
        worker.signals.result.connect(print_Acquire)
        worker.signals.finished.connect(Acquire_thread_complete)
        #worker.signals.progress.connect(Acquire_Progress)
        # Execute
        self.threadpool.start(worker)

    def PowerBoardUpdate(self):
        globalfile.PowerBoard.bit_EN5V = 2
        globalfile.PowerBoard.bit_ENPC = 2
        globalfile.PowerBoard.bit_ENPC = self.ui.pb_cb_1.checkState()
        globalfile.PowerBoard.bit_EN12V = self.ui.pb_cb_2.checkState()
        globalfile.PowerBoard.bit_EN24V = self.ui.pb_cb_3.checkState()
        globalfile.PowerBoard.bit_ENGALVO = self.ui.pb_cb_4.checkState()
        globalfile.PowerBoard.bit_EN34V = self.ui.pb_cb_5.checkState()
        globalfile.PowerBoard.bit_RD6 = self.ui.pb_cb_6.checkState()
        globalfile.PowerBoard.bit_RD7 = self.ui.pb_cb_7.checkState()
        globalfile.PowerBoard.voltage_enable = [globalfile.PowerBoard.bit_EN5V, globalfile.PowerBoard.bit_ENPC,
                                                globalfile.PowerBoard.bit_EN12V,
                                                globalfile.PowerBoard.bit_EN24V, globalfile.PowerBoard.bit_ENGALVO,
                                                globalfile.PowerBoard.bit_EN34V,
                                                globalfile.PowerBoard.bit_RD6, globalfile.PowerBoard.bit_RD7]
        globalfile.PowerBoard.PowerBoardFlag = True
        print("-----PowerBoard is setting the voltage")

    def Powerboardthread(self):
        print("ENTERED INTO THE POWERBOARD THREAD")
        worker = PowerControl(RecvPowerBoardThread)  # Any other args, kwargs are passed to the run function
        worker.signals.result.connect(Print_PowerBoard)
        worker.signals.finished.connect(Exit_PowerBoard)
        # worker.signals.progress.connect(self.Temp_Progress)
        self.threadpool.start(worker)


    def Temp_Progress(self, n):
        print("Temp Progress Running")


    def recvtemp(self):

        # Pass the function to execute
        worker = RecvTemp(RecvTempThread ) # Any other args, kwargs are passed to the run function
        worker.signals.result.connect(print_temp)
        worker.signals.finished.connect(temp_thread_complete)
        worker.signals.progress.connect(self.Temp_Progress)

        # Execute
        self.threadpool.start(worker)


    def LaserProgress(self,n):
        #print("Debug Purpose Laser Progress")
        TempOut = str(n)
        self.ui.le_temp.setText(TempOut)
        self.ui.le_pixcount.setText(str(globalfile.NTCData[11]))
        #print(globalfile.NTCData)


        if (globalfile.NTCData[9] > 0):
            self.ui.pb_interlock.setStyleSheet(
                "QWidget { color: %s ; background-color:dark;border-style:outset;border-color:green;border-radius:18px;border: 5px solid green; }" % QColor(
                    69, 220, 53, 230).name())


        else:
            self.ui.pb_interlock.setStyleSheet(
                "QWidget { color: %s ; background-color:dark;border-style:outset;border-color:red;border-radius:18px;border: 5px solid red; }" % QColor(
                    220, 53, 69, 255).name())

        # --------------------------------------------------
        if (globalfile.NTCData[10] > 0):
            self.ui.pb_lsren.setStyleSheet(
                "QWidget { color: %s ; background-color:dark;border-style:outset;border-color:green;border-radius:18px;border: 5px solid green; }" % QColor(
                    69, 220, 53, 230).name())


        else:
            self.ui.pb_lsren.setStyleSheet(
                "QWidget { color: %s ; background-color:dark;border-style:outset;border-color:red;border-radius:18px;border: 5px solid red; }" % QColor(
                    220, 53, 69, 255).name())
        # ----------------------------------------------------

        # update matrix
        for row in range(9):
            item = QTableWidgetItem(str(round(globalfile.NTCData[row], 4)))
            self.ui.temp_matrix.setItem(0, row, item)


    def LaserControl(self):

            LaserController = LaserControl(Run_Laser)
            LaserController.signals.result.connect(Print_Laser)
            LaserController.signals.finished.connect(Exit_Laser)
            LaserController.signals.progress.connect(self.LaserProgress)
            self.threadpool.start(LaserController)


    def UpdateRawData(self):

        PacketName = "Frame" + "_" + "%06d" % self.framecounter

        PacketPath = join(os.getcwd() , "RawData" , PacketName)
        #print(PacketPath)

        file_exists = os.path.exists(PacketPath)

        if(file_exists):
            print("select the required image here")


        globalfile.RangeImage = np.full((256, 7), globalfile.RangeImageIndex*60)
        globalfile.DopplerImage = np.full((256, 7), globalfile.RangeImageIndex*60)
        globalfile.IntentsityImage = np.full((256, 7), globalfile.RangeImageIndex*60)

    def GalvoUpdate(self):


        if (self.ui.ed_vic.text()):
            globalfile.Galvo.VIC = float(self.ui.ed_vic.text())
        else:
            globalfile.Galvo.VIC = 0.0012507690927035656

        if (self.ui.ed_vbc.text()):
            globalfile.Galvo.VBC = float(self.ui.ed_vbc.text())
        else:
            globalfile.Galvo.VBC = -0.6160037781565061

        if (self.ui.ed_pixelFrame.text()):
            globalfile.Galvo.Pix_Per_Frame = int(self.ui.ed_pixelFrame.text())
        else:
            globalfile.Galvo.Pix_Per_Frame = 986


        globalfile.Galvo.Trigger_Angle_Deg = 0#float(self.ui.ed_TrigAngle.text())
        globalfile.Galvo.Pause_After_Trigger_ms = 0#int(self.ui.ed_pauseTrig.text())
        globalfile.Galvo.Galvo_Mech_Deg_Per_V = 4.8701#float(self.ui.ed_GalvoDeg.text())
        globalfile.GalvoFlag = True
        print("Galvo Updated")

    def GalvoProgress(self):
        print("Debug Purpose Galvo Progress")

    def GalvoControl(self):

        GalvoController = GalvoControl(Run_Galvo)
        GalvoController.signals.result.connect(Print_Galvo)
        GalvoController.signals.finished.connect(Exit_Glavo)
        GalvoController.signals.progress.connect(self.GalvoProgress)
        self.threadpool.start(GalvoController)


    def range_update(self):

        rstop = time.time()
        data = np.random.randint(256, size=(70, 256))
        #data = globalfile.RangeImage

        self.RangeImg.setImage(data)
        QtCore.QTimer.singleShot(1, self.range_update)
        rstart = time.time()
        #time.sleep(0.1)
        #print("Time from Range ", (rstart - rstop))



    def doppler_update(self):

        dstop = time.time()
        data = np.random.randint(256, size=(70, 256))
        #data = globalfile.DopplerImage
        self.Dopplerimg.setImage(data)
        QtCore.QTimer.singleShot(1, self.doppler_update)
        dstart = time.time()
        #time.sleep(0.1)
        #print("Time from Doppler ", (dstop - dstart))


    def intensity_update(self):

        istop = time.time()
        data = np.random.randint(256, size=(70, 256))
        #data = globalfile.IntentsityImage
        self.Intensityimg.setImage(data)
        QtCore.QTimer.singleShot(1, self.intensity_update)
        istart = time.time()
        #print("Time from Intensity ", (istart - istop))


    def on_file_name_changed(self, name):
        # label color based on file_name
        # if the file name is empty them it means file is reseted
        name = path.basename(name)
        file_label_color = "green"
        self.on_task_bar_message(file_label_color, "Successfully loaded {} file".format(name))

    @pyqtSlot(str, str)
    def on_task_bar_message(self, color, message):
        self._ui.statusbar.show()
        self._ui.statusbar.showMessage(message)
        self._ui.statusbar.setStyleSheet('color: {}'.format(color))

    # Set one file
    def open_file_name_dialog(self):
        # open window to select file
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        file_name, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                       "All Files (*)", options=options)

        if file_name:
            self._main_controller.file_name_changed(file_name)
