from PyQt5.QtWidgets import QMainWindow, QFileDialog, QVBoxLayout
from PyQt5.QtCore import pyqtSlot
from os import path
# from view.main_view_ui import Ui_MainWindow
from PyQt5.uic import loadUi
import os
from matplotlib import cm
import pyqtgraph as pg
from Resources.VisGUI import Ui_MainWindow
import serial
from PyQt5.QtWidgets import (QApplication, QMainWindow, QDialog, QMessageBox, QLineEdit, QPushButton, QFileDialog,
                             QSplashScreen, QCheckBox, QTableWidgetItem, QHeaderView, QProgressBar)
import paramiko
import json
from view.colorbar import ColorBarItem
import numpy as np
from controller.Setting import Setting
import time
from PyQt5 import QtCore
from os.path import join, dirname, abspath
import model.GlobalFile as globalfile
from PyQt5.QtCore import QThreadPool

# self.ui = loadUi(str(os.getcwd() + '\\Resources\\VisGUI.ui'), self)
# from controller.UDPThread import RecvTemp, RecvTempThread, print_temp, temp_thread_complete
# from controller.GalvoControl import GalvoControl , Run_Galvo, Print_Galvo, Exit_Glavo
from controller.LaserControl import LaserControl, Run_Laser, Print_Laser, Exit_Laser
# # Activate
from controller.PowerControl import RecvPowerBoardThread, PowerControl, Print_PowerBoard, Exit_PowerBoard
# from controller.APIControlTestBench17Packets import Acquire , AcquireThread , print_Acquire, Acquire_thread_complete
############from controller.APIControlTestPixelOrder import Acquire , AcquireThread , print_Acquire, Acquire_thread_complete
###########from controller.APIControlTestPixelOrderDSPTestBench import Acquire , AcquireThread , print_Acquire, Acquire_thread_complete
######from controller.APIControlTestPixelOrderDSPTestBenchTimeDomain import Acquire , AcquireThread , print_Acquire, Acquire_thread_complete
from controller.APIControlTestPixelOrderDSPUDPTest2peaksmultiply import Acquire, AcquireThread, print_Acquire, Acquire_thread_complete
from Visualizer3D.main_app import App
##from controller.TimeDomainAcq import Acquire , AcquireThread , print_Acquire, Acquire_thread_complete
# from controller.APIStatus import Acquire , AcquireThread , print_Acquire, Acquire_thread_complete
# from controller.APIControlUDP import Acquire , AcquireThread , print_Acquire, Acquire_thread_complete


# from controller.APIControl import Acquire , AcquireThread , print_Acquire, Acquire_thread_complete

##############from controller.TimeDomainAcqMultiPeak import Acquire , AcquireThread , print_Acquire, Acquire_thread_complete


# from controller.MatlabClient import MatThread , MatThreadRun , print_mat , mat_thread_complete
# from controller.VisWindow2Frame import VisWindow
from controller.VisWindow import VisWindow

#######from controller.VisWindowEqualPixel import VisWindow

from controller.VisWindowTimeDomain import VisWindowTimeDomain
from controller.VisWindowPointCloud import VisWindowPointCloud
from controller.VisWindowLinearSpectrum import VisWindowLinearSpectrum

from PyQt5.QtGui import *

from PyQt5 import QtCore, QtGui

from Resources.viswindow import Ui_viswindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget


class MainView(QMainWindow):
    newDataArrived = QtCore.pyqtSignal()
    def __init__(self, model, main_controller):
        super().__init__()
        self._model = model
        self._main_controller = main_controller

        # self.ui = Ui_MainWindow()
        # self.ui.setupUi()
        # linux
        self.ui = loadUi(str(os.path.dirname(__file__) + '/..//Resources//baseUI_tab.ui'), self)
        # windows
        # self.ui = loadUi(str(os.getcwd() + '//Resources//baseUI_tab.ui'), self)

        self.setting = Setting(self.ui)
        self.vis3d = None
        ####################################################################
        #   connect widgets to controllers
        ####################################################################
        # open file buttons
        # self._ui.pushButton.clicked.connect(self.open_file_name_dialog)

        ####################################################################
        #   listen for model event signals
        ####################################################################
        # file name is updated
        # self._model.file_name_changed.connect(self.on_file_name_changed)

        ###############Logo Update###################
        pixmap = QPixmap(os.path.dirname(__file__) + '/..//Resources//ScantinelLogo.jpg')
        self.ui.la_logo.setPixmap(pixmap.scaledToWidth(300))

        app_icon = QtGui.QIcon()
        app_icon.addFile(os.path.dirname(__file__) + '/..//Resources//ScanLogo.jpg', QtCore.QSize(500, 500))
        self.ui.setWindowIcon(app_icon)

        self.ui.setGeometry(500, 150, 650, 650)

        # #################### DSP Visualization ###########################################################
        # colormap = cm.get_cmap("viridis")
        # colormap._init()
        # lut = (colormap._lut * 255).view(np.ndarray)  # Convert matplotlib colormap from 0-1 to 0 -255 for Qt
        # self.ui.VisWidget.setLayout(QVBoxLayout())
        # self.canvas = pg.GraphicsLayoutWidget()
        # self.ui.VisWidget.layout().addWidget(self.canvas)
        # self.canvas.setAspectLocked(True)
        #
        # #----------------------Range Visualization --------------------------------------#
        #
        # RangePlot = self.canvas.addPlot(title="Range Image")
        # #RangePlot.hideAxis('left')
        # #RangePlot.hideAxis('bottom')
        # self.RangeImg = pg.ImageItem(border='w')
        # self.RangeImg.setLookupTable(lut)
        # RangePlot.addItem(self.RangeImg)
        # Rangebar = ColorBarItem(interactive=False , cmap=colormap,values=(0, 50) , label = "meters(m)")
        # Rangebar.setImageItem( self.RangeImg, insert_in=RangePlot )
        # self.RangeImg.setLookupTable(lut)

        # # #----------------------Doppler Visualization --------------------------------------#
        # self.canvas.nextRow()
        #
        # DopplerPlot = self.canvas.addPlot(title="Doppler Image")
        # #DopplerPlot.hideAxis('left')
        # #DopplerPlot.hideAxis('bottom')
        #
        # self.Dopplerimg = pg.ImageItem()
        # self.Dopplerimg.setLookupTable(lut)
        # DopplerPlot.addItem(self.Dopplerimg)
        #
        # cmap = cm.get_cmap("viridis")
        # Dopplerbar = ColorBarItem(interactive=False, cmap=colormap, values=(0, 150), colorMap=cmap)
        # #Dopplerbar.hideAxis('right')
        # Dopplerbar.setImageItem(self.Dopplerimg, insert_in=DopplerPlot)
        # self.Dopplerimg.setLookupTable(lut)
        #
        # #----------------------Intensity Visualization --------------------------------------#
        # self.canvas.nextRow()
        #
        # IntensityPlot = self.canvas.addPlot(title="Intensity Image")
        # IntensityPlot.hideAxis('left')
        # IntensityPlot.hideAxis('bottom')
        #
        # self.Intensityimg = pg.ImageItem()
        # self.Intensityimg.setLookupTable(lut)
        # IntensityPlot.addItem(self.Intensityimg)
        #
        # cmap = cm.get_cmap("viridis")
        # Intensitybar = ColorBarItem(interactive=False, cmap=colormap,values=(0, 1), colorMap=cmap, )
        # #Intensitybar.hideAxis('right')
        # Intensitybar.setImageItem(self.Intensityimg, insert_in=IntensityPlot)
        #
        # self.Intensityimg.setLookupTable(lut)
        # #----------------------------------------
        # self.range_update()
        # self.doppler_update()
        # self.intensity_update()

        ######### update Image###################

        #self.ui.pb_imageupdate.clicked.connect(self.setting.updatePlot)
        self.ui.pb_start.clicked.connect(self.setting.LaserUpdate)
        self.ui.cb_ENFFT.stateChanged.connect(self.setting.LaserUpdate)
        self.ui.cb_start.stateChanged.connect(self.setting.LaserUpdate)
        self.ui.cb_laser.stateChanged.connect(self.setting.LaserUpdate)
        self.ui.cb_ChirpSim.stateChanged.connect(self.setting.LaserUpdate)
        self.ui.cb_LSRMan.stateChanged.connect(self.setting.LaserUpdate)
        self.ui.cb_ChirpMan.stateChanged.connect(self.setting.LaserUpdate)

        self.ui.EN_P3V.stateChanged.connect(self.PowerBoardUpdate)
        self.ui.EN_N3V.stateChanged.connect(self.PowerBoardUpdate)
        self.ui.EN_P5V.stateChanged.connect(self.PowerBoardUpdate)
        self.ui.EN_P24V.stateChanged.connect(self.PowerBoardUpdate)
        self.ui.EN_P15V.stateChanged.connect(self.PowerBoardUpdate)
        self.ui.EN_5V.stateChanged.connect(self.PowerBoardUpdate)
        self.ui.EN_FANS.stateChanged.connect(self.PowerBoardUpdate)
        self.ui.EN_DSP.stateChanged.connect(self.PowerBoardUpdate)
        self.ui.EN_LASER.stateChanged.connect(self.PowerBoardUpdate)
        self.ui.EN_SCAN_SYS.stateChanged.connect(self.PowerBoardUpdate)
        self.ui.EN_34V.stateChanged.connect(self.PowerBoardUpdate)
        self.ui.visualizaton_3D.clicked.connect(self.visualization_3D)

        # self.ui.sendvoltage.clicked.connect(self.PowerBoardUpdate)
        # self.ui.pb_AcquireData.clicked.connect(self.startacquire)
        self.ui.pb_logdata.clicked.connect(self.startacquire)

        self.ui.pb_connect.clicked.connect(self.setting.connectscanner)
        self.ui.pb_power.clicked.connect(self.power_up_sequence)

        self.ui.pb_init.clicked.connect(self.initialize)

        #self.ui.pb_laser.clicked.connect(self.setting.EngineON)

        self.ui.pb_stop.clicked.connect(self.setting.PowerDown)

        self.ui.gb_status.setEnabled(False)

        self.ui.pb_viswindow.clicked.connect(self.viswindow)
        # self.ui.ls_pb_amp.clicked.connect(self.laser_power_update)

        self.ui.pb_savefolder.clicked.connect(self.selectfolder)

        self.ui.pb_BRAMupdate.clicked.connect(self.selectBRAMfile)

        # timer = QtCore.QTimer(self)
        # timer.timeout.connect(self.UpdateRawData)
        # timer.start(10)
        self.framecounter = 80

        ################## Thread Management #######################

        # Save Temperature into txt file

        TempHeader = "MainSM  , NW  , NE  , SW , SE , Heat-Sink , ND-Driver , SD-Driver , LA_TEMP , LA_CUR , " \
                     "PB_TEMP1 , PB_TEMP2 "

        tempfile = "TempStorage.txt"

        if os.path.exists(tempfile):
            os.remove(tempfile)
        else:
            print("Can not delete the temp file as it doesn't exists")

        with open('TempStorage.txt', 'a') as f:
            f.write(TempHeader + "\n")
            f.close

        self.threadpool = QThreadPool()

        # self.recvtemp()   ##-----------udp
        # self.LaserControl()

        ##Activatetion needed
        # self.Powerboardthread()

        # self.ui.temp_matrix.verticalHeader().setDefaultSectionSize(50);
        # self.ui.temp_matrix.horizontalHeader().setDefaultSectionSize(200);

        self.ui.statusBar().showMessage("Waiting for Connection")
        self.ui.statusBar().setStyleSheet(
            "background-color:red;\ncolor:white;\nborder-style:outset;\nborder-width:2px;\nborder-radius:1px;border: 5px  red")

        self.w = None  # VisWindow()

        ###Debug Purpose only
        self.ui.pb_power.setEnabled(True)
        self.ui.pb_init.setEnabled(True)

        ##debug purpose only

        self.ui.pb_config.clicked.connect(self.ConfigDSP)

        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.UpdateADC)
        timer.start(1000)

        ############### inistal DSP diables


        #self.ui.pb_logdata.setEnabled(False)

        # PB update
        self.read_port_c = [self.ui.READ_P3V, self.ui.READ_N3V, self.ui.READ_P5V, self.ui.READ_P24V,
                            self.ui.READ_P15V, self.ui.READ_P15V, self.ui.bit_RC6, self.ui.bit_RC77]
        self.read_port_d = [self.ui.READ_5V, self.ui.READ_FANS,
                            self.ui.READ_DSP,
                            self.ui.READ_LASER, self.ui.READ_SCAN, self.ui.READ_34V, self.ui.bit_LED1,
                            self.ui.bit_LED2]
        self.read_portab = [self.ui.FAULT_N3V, self.ui.FAULT_24V, self.ui.bit_RB2, self.ui.bit_RB3, self.ui.bit_RB4,
                            self.ui.P3V_PGOOD, self.ui.P5V_PGOOD,
                            self.ui.PFET_STATUS]
        self.port_c = [self.ui.EN_P3V, self.ui.EN_N3V, self.ui.EN_P5V, self.ui.EN_P24V,
                       self.ui.EN_P15V, self.ui.EN_P15V, self.ui.bit_RC6, self.ui.bit_RC77]
        self.port_d = [self.ui.EN_5V, self.ui.EN_FANS,
                       self.ui.EN_DSP,
                       self.ui.EN_LASER, self.ui.EN_SCAN_SYS, self.ui.EN_34V, self.ui.bit_LED1,
                       self.ui.bit_LED2]

        self.vis3d = None

        self.ui.cb_log.setCurrentIndex(1)
        self.ui.cb_detection.setCurrentIndex(1)
        self.ui.cb_range.setCurrentIndex(0)




    def startacquire(self):
        # pass
        isExist = os.path.exists(globalfile.savepath)

        if not isExist:

            ret = QMessageBox.question(self.ui, 'Information', "Please Select the Directory to Log the Data",
                                       QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Cancel)

        else:

            self.ui.pb_logdata.setEnabled(False)
            self.AcquireThread()

        # self.AcquireThread()
        # self.MatlabThread()

        ##Disbale acquire button and Enabler Vis window

    def selectBRAMfile(self):

        filepath = QFileDialog.getOpenFileName(self.ui, 'Select BRAM file', '', "BRAM files (*.npzpb_logdata)")
        self.ui.le_BRAMcontent.setText(str(filepath[0]))
        globalfile.BRAMfilePath = str(filepath[0])

        print(type(filepath))
        print("BRAM file Path  -------", globalfile.BRAMfilePath)

    def selectfolder(self):

        folderpath = QFileDialog.getExistingDirectory(self.ui, 'Select Folder')
        self.ui.le_savepath.setText(str(folderpath))
        globalfile.savepath = str(folderpath)
        print("path is -------", globalfile.savepath)

    def initialize(self):
        if (globalfile.LaserFlag == False):
            print("Laser Thread starting")

            self.LaserControl()

            ##debugpurpose
            # self.MatlabThread()
        self.setting.Init()

    def power_up_sequence(self):
        print("State", globalfile.PowerBoard.PowerBoardFlag)
        if not globalfile.PowerBoard.PowerBoardFlag:
            self.Powerboardthread()
        for i in globalfile.PowerBoard.power_up_sequence:
            if i < 8:
                if i == 4:
                    # if i == 0 or i == 4:
                    globalfile.PowerBoard.port_C[i] = 2
                    globalfile.PowerBoard.port_C[i + 1] = 2
                    globalfile.PowerBoard.PowerBoardFlag = True
                    self.port_c[i].setChecked(True)
                    self.port_c[i + 1].setChecked(True)
                else:
                    globalfile.PowerBoard.port_C[i] = 2
                    globalfile.PowerBoard.PowerBoardFlag = True
                    self.port_c[i].setChecked(True)
            elif i >= 8:
                if i == 10:
                    globalfile.PowerBoard.PowerBoardFlag = True
                globalfile.PowerBoard.port_D[i - 8] = 2
                globalfile.PowerBoard.PowerBoardFlag = True
                self.port_d[i - 8].setChecked(True)
            time.sleep(0.5)
        self.ui.pb_power.setEnabled(False)
        self.ui.pb_init.setEnabled(True)
        self.ui.statusBar().showMessage("Powered ON")

    def UpdateADC(self):

        a = 0

        self.ui.le_DSPtemp.setText(str(globalfile.DSPTemp))
        if globalfile.PowerBoard.auto_shut_down:
            self.port_d[5].setChecked(False)
            ret = QMessageBox.question(self.ui, 'Warning', "Please power off system",
                                       QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Cancel)

            # self.ui.le_max.setText(str(globalfile.peakmax))
            # self.ui.le_adcmax.setText(str(globalfile.adcmax))
            # self.ui.le_adcmin.setText(str(globalfile.adcmin))

            # self.ui.le_distance.setText(str(globalfile.peakmaxdistance))

    def ConfigDSP(self):

        # self.ui.gb_DSPenable.setEnabled(True)
        #self.ui.pb_logdata.setEnabled(True)

        self.ui.cb_DSPmode.setEnabled(False)
        self.ui.cb_fftmode.setEnabled(False)
        #self.ui.cb_detection.setEnabled(False)


        globalfile.RangeMarker = self.ui.cb_range.currentIndex()
        globalfile.IntensityMarker = self.ui.cb_intensity.currentIndex()
        globalfile.LogFlag = self.ui.cb_log.currentIndex()


        print(" Range Marker and Intensity Markers are",globalfile.RangeMarker , globalfile.IntensityMarker )

        if (self.ui.cb_fftmode.currentIndex() == 0):
            globalfile.FFTLength = 16384
        elif(self.ui.cb_fftmode.currentIndex() == 1):
            globalfile.FFTLength = 8192

        detectionalgo = self.ui.cb_detection.currentIndex()
        if(detectionalgo == 0):
            globalfile.detectionmode = 0
            print(" constant threshold selected")
        else:
            globalfile.detectionmode = 1
            print(" CFAR is selected")


        if (self.ui.le_rangemin.text()):
            globalfile.rangemin = int(self.ui.le_rangemin.text())

        if (self.ui.le_rangemax.text()):
            globalfile.rangemax = int(self.ui.le_rangemax.text())

        if (self.ui.le_peakspace.text()):
            globalfile.PeakSpace = int(self.ui.le_peakspace.text())


        #################################################
        if (self.ui.le_CFARcoeff.text()):
            globalfile.CFARCoeff = int(self.ui.le_CFARcoeff.text())

        if (self.ui.le_CFARoffset.text()):
            globalfile.CFAROffset = int(self.ui.le_CFARoffset.text())

        if (self.ui.le_ADCchannel.text()):
            globalfile.ADCCH1 = int(self.ui.le_ADCchannel.text())

        if (self.ui.le_ConstThresh.text()):
            globalfile.ConstThresh = int(self.le_ConstThresh.text())
        ################################################# ADC config #################

        if (self.ui.le_ADCscale.text()):
            globalfile.ADCscale = int(self.le_ADCscale.text())
        if (self.ui.le_ADCreset.text()):
            globalfile.ADCreset = int(self.le_ADCreset.text())
        if (self.ui.le_FTR.text()):
            globalfile.FTR = float(self.le_FTR.text())



        globalfile.FreqRes = globalfile.FS / globalfile.FFTLength

        globalfile.RangeMinBin = int(
            (globalfile.rangemin * 2 * globalfile.FTR * 1e14) / (globalfile.FreqRes * globalfile.c0))
        globalfile.RangeMaxBin = int(
            (globalfile.rangemax * 2 * globalfile.FTR * 1e14) / (globalfile.FreqRes * globalfile.c0))
        globalfile.PeakSpaceBin = int(
            (globalfile.PeakSpace * 2 * globalfile.FTR * 1e14) / (globalfile.FreqRes * globalfile.c0))


        # if(globalfile.FFTLength == 8192):
        #     globalfile.RangeMinBin = 2 * globalfile.RangeMinBin
        #     globalfile.RangeMaxBin = 2 * globalfile.RangeMaxBin
        #     globalfile.PeakSpace = 2 * globalfile.PeakSpace


        print(" configured window is ", globalfile.RangeMinBin, globalfile.RangeMaxBin)

        print(" FFT size and Fre resolution ", globalfile.FFTLength, globalfile.FreqRes ,globalfile.FTR  )

        ret = QMessageBox.question(self.ui, 'Information', "DSP will be Initialized with these Configuration",
                                   QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Cancel)

        # print(globalfile.ADCCH1 , globalfile.CFARCoeff  ,globalfile.FFTLength )

        if (self.ui.cb_DSPmode.currentIndex() == 1):
            globalfile.DSPMode = 1
            if self.w is None:
                self.w = VisWindowTimeDomain()

        if (self.ui.cb_DSPmode.currentIndex() == 2):
            globalfile.DSPMode = 2
            if self.w is None:
                self.w = VisWindowLinearSpectrum()

        if (self.ui.cb_DSPmode.currentIndex() == 0):
            globalfile.DSPMode = 0
            if self.w is None:
                self.w = VisWindowPointCloud()

    def viswindow(self):

        self.w.show()

    def Acquire_Progress(self):
        print("Acquire thread prgress")

    def AcquireThread(self):
        print(" API Client Started")

        worker = Acquire(AcquireThread)  # Any other args, kwargs are passed to the run function
        worker.signals.result.connect(print_Acquire)
        worker.signals.finished.connect(Acquire_thread_complete)
        worker.signals.progress.connect(lambda *args: self.newDataArrived.emit())
        # Execute
        self.threadpool.start(worker)

    def PowerBoardUpdate(self):
        print("---checked after")
        if not globalfile.PowerBoard.PowerBoardFlag:
            self.Powerboardthread()
        globalfile.PowerBoard.port_C = [self.ui.EN_P3V.checkState(), self.ui.EN_N3V.checkState(),
                                        self.ui.EN_P5V.checkState(),
                                        self.ui.EN_P24V.checkState(), self.ui.EN_P15V.checkState(),
                                        self.ui.EN_P15V.checkState(), 0, 0]
        # print(" port c ::: ", globalfile.PowerBoard.port_C)
        globalfile.PowerBoard.port_D = [self.ui.EN_5V.checkState(), self.ui.EN_FANS.checkState(),
                                        self.ui.EN_DSP.checkState(),
                                        self.ui.EN_LASER.checkState(), self.ui.EN_SCAN_SYS.checkState(),
                                        self.ui.EN_34V.checkState(), 0, 0]
        globalfile.PowerBoard.PowerBoardFlag = True
        # print("-----PowerBoard is setting the voltage")

    def PB_progress(self, n):
        vol_monitoring = [2, 2, globalfile.PowerBoard.port_D[5], globalfile.PowerBoard.port_C[0],
                          globalfile.PowerBoard.port_C[1],
                          globalfile.PowerBoard.port_C[4], globalfile.PowerBoard.port_C[5],
                          globalfile.PowerBoard.port_C[2],
                          globalfile.PowerBoard.port_C[3], 2, 2, 2]
        for i in range(8):
            if globalfile.PowerBoard.Receiving_data[5] & (1 << i):
                self.read_port_c[i].setChecked(True)
            else:
                self.read_port_c[i].setChecked(False)
            if globalfile.PowerBoard.Receiving_data[6] & (1 << i):
                self.read_port_d[i].setChecked(True)
            else:
                self.read_port_d[i].setChecked(False)
            if globalfile.PowerBoard.Receiving_data[7] & (1 << i):
                self.read_portab[i].setChecked(True)
            else:
                self.read_portab[i].setChecked(False)

        for col in range(12):
            a = (int(globalfile.PowerBoard.Read_status[col], 16))
            # print("Normal a value is ....", a)
            if a & (1 << (16 - 1)):
                a -= 1 << 16
            a_con = round(a * 0.01, 2)
            # print("After a value is-----", a_con)
            item = QTableWidgetItem(str(a_con))
            self.ui.PB_matrix.setItem(col, 0, item)
            # need to remove test SDL when voltage monitoring is well tested
            if globalfile.PowerBoard.time_pause == 3 and vol_monitoring[col] == 2 and globalfile.PowerBoard.test_SDL:
                if (globalfile.PowerBoard.voltage_monitoring[str(col)][0]) <= a_con <= \
                        (globalfile.PowerBoard.voltage_monitoring[str(col)][1]):
                    pass
                    print("with in the range ", col)
                else:
                    print(a_con)
                    globalfile.PowerBoard.Temp_meta_info[col] = 1
                    globalfile.PowerBoard.SDL_priority = True
                    print('Problem With Power Supply', col)
        globalfile.PowerBoard.PB_TEMP1 = round((int(globalfile.PowerBoard.Read_status[-1], 16) * 0.01), 2)
        globalfile.PowerBoard.PB_TEMP2 = round((int(globalfile.PowerBoard.Read_status[-2], 16) * 0.01), 2)
        self.ui.T1_PCB_TEMP.setText(str(globalfile.PowerBoard.PB_TEMP1))
        self.ui.T2_PCB_TEMP.setText(str(globalfile.PowerBoard.PB_TEMP2))
        # need to remove test SDL when voltage monitoring is well tested
        if globalfile.PowerBoard.SDL_priority and globalfile.PowerBoard.test_SDL:
            print('in SDL priority')
            # not used for loop because of time consumption
            globalfile.PowerBoard.temp_mon_result = 0
            if globalfile.PowerBoard.Temp_meta_info[0] or globalfile.PowerBoard.Temp_meta_info[1]:
                globalfile.PowerBoard.temp_mon_result += 1 << 0
            if globalfile.PowerBoard.Temp_meta_info[2]:
                globalfile.PowerBoard.temp_mon_result += 1 << 1
            if globalfile.PowerBoard.Temp_meta_info[3] or globalfile.PowerBoard.Temp_meta_info[4]:
                globalfile.PowerBoard.temp_mon_result += 1 << 2
            if globalfile.PowerBoard.Temp_meta_info[5] or globalfile.PowerBoard.Temp_meta_info[6]:
                globalfile.PowerBoard.temp_mon_result += 1 << 3
            if globalfile.PowerBoard.Temp_meta_info[7]:
                globalfile.PowerBoard.temp_mon_result += 1 << 4
            if globalfile.PowerBoard.Temp_meta_info[8]:
                globalfile.PowerBoard.temp_mon_result += 1 << 5
            if globalfile.PowerBoard.Temp_meta_info[9]:
                globalfile.PowerBoard.temp_mon_result += 1 << 6
            globalfile.PowerBoard.time_pause = 0
            np.save("Temp_Monitoring.npy", globalfile.PowerBoard.temp_mon_result)
            # print("Temperature status saved in a file")

    def Powerboardthread(self):
        print("ENTERED INTO THE POWER BOARD THREAD")
        worker = PowerControl(RecvPowerBoardThread)  # Any other args, kwargs are passed to the run function
        worker.signals.result.connect(Print_PowerBoard)
        worker.signals.finished.connect(Exit_PowerBoard)
        worker.signals.progress.connect(self.PB_progress)
        self.threadpool.start(worker)

    def show_visualization(self):
        pass
        # vis_3d = visualization(Run_visualization)
        # self.vis_3d = main_app()
        # vis_3d.show()

    def visualization_3D(self):
        print("Entered into the 3D visualization window")
        if self.vis3d is None:
            self.vis3d = App()
            self.vis3d.main_view.show()
            self.newDataArrived.connect(self.vis3d.main_view.newDataArrive)
        else:
            self.vis3d.main_view.show()




    def Temp_Progress(self, n):
        print("Temp Progress Running")

    # def recvtemp(self):
    #
    #     # Pass the function to execute
    #     worker = RecvTemp(RecvTempThread)  # Any other args, kwargs are passed to the run function
    #     worker.signals.result.connect(print_temp)
    #     worker.signals.finished.connect(temp_thread_complete)
    #     worker.signals.progress.connect(self.Temp_Progress)
    #
    #     # Execute
    #     self.threadpool.start(worker)

    def LaserProgress(self, n):
        # print("Debug Purpose Laser Progress")
        TempOut = str(int(n))
        # print(globalfile.amp_pwr_.flag)
        if globalfile.amp_pwr_.flag == 1:
            self.ui.le_laser_power.clear()
            globalfile.amp_pwr_.flag = 0
            print(" CLEARED ")
        self.ui.la_readback.setText((globalfile.amp_pwr_.amp_receive).decode("utf-8"))
        self.ui.pb_SMID.setText(TempOut)
        self.ui.le_pixcount.setText(str(globalfile.NTCData[11]))
        self.ui.le_SMTemp.setText(str(round(globalfile.NTCData[3], 2)))
        # print(globalfile.NTCData)
        self.ui.la_temp.setText(str(round(globalfile.laser_temp, 2)))
        self.ui.la_current.setText(str(round(globalfile.laser_current, 2)))

        # if (globalfile.NTCData[9] > 0):
        #     self.ui.pb_interlock.setStyleSheet(
        #         "QWidget { color: %s ; background-color:dark;border-style:outset;border-color:green;border-radius:18px;border: 5px solid green; }" % QColor(
        #             69, 220, 53, 230).name())
        #
        #
        # else:
        #     self.ui.pb_interlock.setStyleSheet(
        #         "QWidget { color: %s ; background-color:dark;border-style:outset;border-color:red;border-radius:18px;border: 5px solid red; }" % QColor(
        #             220, 53, 69, 255).name())

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

        for row in range(9):
            if (globalfile.NTCData[row] > 90):
                # pass

                self.ui.temp_matrix.item(0, row).setBackground(QtGui.QColor(69, 180, 53, 230))  ##RGB
            else:
                pass
                self.ui.temp_matrix.item(0, row).setBackground(QtGui.QColor(180, 53, 69, 255))

        # self.ui.temp_matrix.setItem(row, 0, item)

    def ResistanceProgress(self):
        pass

    # def MatlabThread(self):
    #     print("Starting Matlab Measurement Thread")
    #     MatAgent = MatThread(MatThreadRun)
    #     MatAgent.signals.result.connect(print_mat)
    #     MatAgent.signals.finished.connect(mat_thread_complete)
    #     MatAgent.signals.progress.connect(self.ResistanceProgress)
    #     self.threadpool.start(MatAgent)

    def LaserControl(self):

        LaserController = LaserControl(Run_Laser)
        LaserController.signals.result.connect(Print_Laser)
        LaserController.signals.finished.connect(Exit_Laser)
        LaserController.signals.progress.connect(self.LaserProgress)
        self.threadpool.start(LaserController)

    def UpdateRawData(self):

        PacketName = "Frame" + "_" + "%06d" % self.framecounter

        PacketPath = join(os.getcwd(), "RawData", PacketName)
        # print(PacketPath)

        file_exists = os.path.exists(PacketPath)

        if (file_exists):
            print("select the required image here")

        self.framecounter = self.framecounter + 1
        if (self.framecounter > 230):
            self.framecounter = 80
        globalfile.RangeImage = np.full((256, 70), self.framecounter)
        globalfile.DopplerImage = np.full((256, 70), self.framecounter)
        globalfile.IntentsityImage = np.full((256, 70), self.framecounter)

    def range_update(self):

        # rstop = time.time()
        data = np.zeros((116, 256))  ###cartsial coordinate system
        data[115][0] = 230  # right corner

        # data1 = np.empty([256, 70])
        # data1.fill(220)
        # data1[0:10][0:10] = 100
        # globalfile.rangeimageup = np.random.randint(256, size=(70, 256))
        # print(globalfile.RangeImage[50][50])
        # data1 = globalfile.RangeImage
        if (globalfile.RangeImageIndex == 0):
            self.RangeImg.setImage(globalfile.rangeimage)

        elif (globalfile.RangeImageIndex == 1):
            self.RangeImg.setImage(globalfile.rangeimageup)

        elif (globalfile.RangeImageIndex == 2):
            self.RangeImg.setImage(globalfile.rangeimagedown)

        QtCore.QTimer.singleShot(1, self.range_update)
        # rstart = time.time()
        # time.sleep(0.1)
        # print("Time from Range ", (rstart - rstop))

    def doppler_update(self):

        dstop = time.time()
        data = np.full((116, 256), 100)
        # data = globalfile.DopplerImage
        self.Dopplerimg.setImage(data)

        # self.Dopplerimg.setImage(globalfile.dopplerimage)
        QtCore.QTimer.singleShot(1, self.doppler_update)
        dstart = time.time()
        # time.sleep(0.1)
        # print("Time from Doppler ", (dstop - dstart))

    def intensity_update(self):

        istop = time.time()
        data = np.random.randint(256, size=(70, 256))
        # data = globalfile.IntentsityImage

        if (globalfile.IntensityImageIndex == 0):
            self.Intensityimg.setImage(globalfile.intensityimage)

        elif (globalfile.IntensityImageIndex == 1):
            self.Intensityimg.setImage(globalfile.intensityimageup)

        elif (globalfile.IntensityImageIndex == 2):
            self.Intensityimg.setImage(globalfile.intensityimagedown)

        QtCore.QTimer.singleShot(1, self.intensity_update)
        istart = time.time()
        # print("Time from Intensity ", (istart - istop))

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

    def laser_power_update(self):
        pass
        # print("entered into the amplider *****")
        # with open("/home/scantinel/GUI/controller/Power_Board_Configuration.json", "r",
        #           encoding='utf-8') as configuration:
        #     data = json.load(configuration)
        #     host_info_ = data["host_info"]
        #     for key in host_info_:
        #         host = key["HOST"]
        #         port = int(key["PORT"])
        #         username = key["USERNAME"]
        #         password = key["PASSWORD"]
        #         print(port, host)
        #     ssh = paramiko.SSHClient()
        #     ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        #     ssh.connect(host, port, username, password)
        #     print('SSH connection is established for laser amplifier power ')
        #     if self.ui.ls_line_amp.text():
        #         globalfile.amp_pwr_.amp_pwr = int(self.ui.ls_line_amp.text())
        #         stdin, stdout, stderr = ssh.exec_command(f'./laser_amp_pwr -i {globalfile.amp_pwr_.amp_pwr}')
        #         # amp_pwr_read = laser_serial_comm.readline()
        #     else:
        #         print("NO input")
