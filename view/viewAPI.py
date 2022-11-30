from PyQt5.QtWidgets import QMainWindow, QFileDialog, QVBoxLayout
from os import path
#from view.main_view_ui import Ui_MainWindow
from PyQt5.uic import loadUi
import os
from matplotlib import cm
import pyqtgraph as pg
from Resources.VisGUI import Ui_MainWindow
import serial
from PyQt5.QtWidgets import (QApplication, QMainWindow, QDialog, QMessageBox, QLineEdit, QPushButton, QFileDialog, QSplashScreen, QCheckBox, QTableWidgetItem,QHeaderView,QProgressBar)
import json
from view.colorbar import ColorBarItem
import numpy as np
from controller.Setting import Setting
import time
from PyQt5 import QtCore
from os.path import join, dirname, abspath
import model.GlobalFile as globalfile
from PyQt5.QtCore import QThreadPool

from PyQt5.QtGui import *

from PyQt5 import QtCore, QtGui

from Resources.viswindow import Ui_viswindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout
from enum import IntEnum

from ctypes  import *
from enum import Enum
import ctypes, ctypes.util




class CtypesEnum(IntEnum):
    @classmethod
    def from_param(cls, obj):
        return int(obj)



class lm_fftSize(CtypesEnum):
    LM_FFT_8K= 0
    LM_FFT_16K= 1

class lm_triggerMode(CtypesEnum):
    LM_TRIGGER_MULT_SHOT = 0
    LM_TRIGGER_CONTINUOUS = 1




class lm_peakSearch(Structure):
    _fields_= [ ("peakSearchWindowStart_m" , c_float),
                ("peakSearchWindowEnd_m" , c_float),
                ("peakHeightThreshold" , c_float),
                ("peakSpacingMinimum_m" , c_float),
    ]


class lm_return(Enum):
        LM_SUCCESS 						= 0
        LM_FAILURE						= -1
        LM_CONNECTION_ERROR 			= -10
        LM_MODULE_UNAVAILABLE			= -11
        LM_MODULE_ALREADY_CONFIGURED 	= -20
        LM_INPUT_PARAM_INVALID			= -30
        LM_CONFIG_FILE_ERROR			= -40





class lm_result(Structure):
    _fields_= [ ("timestamp" , c_uint64),
                ("triggerCount" , c_uint32),
                ("range" , (c_float*16)),
                ("velocity" , (c_float*16)),
                ("upChirpPeakLocation" , (c_float*4)*16),
                ("upChirpPeakHeight" , (c_float*4)*16),
                ("downChirpPeakLocation" , (c_float*4)*16),
                ("downChirpPeakHeight" , (c_float*4)*16),

    ]



class lm(Structure):
    _fields_= [ ("ethernetBufferSize" , c_uint32),
                ("ipAddressString" , (c_char * 40)),
                ("ethernetPort" , (c_char * 6)),
                ("configurationFilePath" , (c_char * 255)),
                ("configFftSize", c_uint32)
                 
    ]






class MainView(QMainWindow):
    def __init__(self, model, main_controller):
        super().__init__()
        self._model = model
        self._main_controller = main_controller


        #self.ui = Ui_MainWindow()
        #self.ui.setupUi()
        #linux
        self.ui = loadUi(str(os.getcwd() + '//Resources//baseUI_tab.ui'), self)
        #windows
        #self.ui = loadUi(str(os.getcwd() + '//Resources//baseUI_tab.ui'), self)


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
        self.ui.la_logo.setPixmap(pixmap)

        app_icon = QtGui.QIcon()
        app_icon.addFile(os.getcwd() + '//Resources//ScanLogo.jpg', QtCore.QSize(500, 500))
        self.ui.setWindowIcon(app_icon)

        self.ui.setGeometry(500, 150, 650, 650)
        self.AcquireData()



        


    def AcquireData(self):

        #-----------Load the Library
    
        EngineLib = cdll.LoadLibrary('./libBridgerPhotonics_LidarModule_UserAPI.so')


        #------------Define the Functions

        Engine_Init = EngineLib.lm_Init
        Engine_Init.argtypes = [ctypes.POINTER(lm), ctypes.POINTER(lm_peakSearch)]
        Engine_Init.restype = lm_return

        Engine_FlushBuffer = EngineLib.lm_EthernetBufferFlush
        Engine_FlushBuffer.argtypes = [ctypes.POINTER(lm)]
        Engine_FlushBuffer.restype = lm_return

        Engine_TriggerDisable = EngineLib.lm_PixelTriggerEnable
        Engine_TriggerDisable.argtypes = [ctypes.POINTER(lm)  ]
        Engine_TriggerDisable.restype = lm_return

        Engine_MeasurementStart = EngineLib.lm_MeasurementsStart
        Engine_MeasurementStart.argtypes = [ctypes.POINTER(lm) , c_int  , c_uint32 ]
        Engine_MeasurementStart.restype = lm_return

        Engine_GetData = EngineLib.lm_MeasurementsGet
        Engine_GetData.argtypes = [ctypes.POINTER(lm) , ctypes.POINTER(lm_result) , c_uint16]
        Engine_GetData.restype = c_int32


        ######## ---------------Initialize the Library

        EngineCon = lm()
        PeakSearch = lm_peakSearch()

        EngineCon.ethernetBufferSize =  c_uint32(1024*1024*128)
        EngineCon.ipAddressString = bytes("192.168.20.100", encoding='utf8')
        EngineCon.ethernetPort = bytes("4194", encoding='utf8')
        EngineCon.configurationFilePath = bytes("/home/scantinel/EngineAPI/MultiPeak/ConfigFiles", encoding='utf8')
        EngineCon.configFftSize = c_uint32(1)
        

        PeakSearch.peakSearchWindowStart_m = c_float(4.0)
        PeakSearch.peakSearchWindowEnd_m = c_float(20.0)
        PeakSearch.peakHeightThreshold = c_float(1.7)
        PeakSearch.peakSpacingMinimum_m = c_float(0.01)
        
        FunReturn = Engine_Init( EngineCon , PeakSearch)

        if(FunReturn.name == "LM_SUCCESS"):
            print("Succesfully Loaded Library")
        else:
            print("ERROR --------------------Not possible to load Library", int(FunReturn.value), FunReturn.name)
            return 0

        ######## ---------------Flush the Buffer

        FunReturn = Engine_FlushBuffer( EngineCon )

        if(FunReturn.name == "LM_SUCCESS"):
            print("Succesfully Flushed Buffer")  
        else:
            print("ERROR --------------------Not possible to Flush the Buffer", FunReturn.value, FunReturn.name)   
            return 0 


        ######## ---------------Enable Pixel Trigger

        FunReturn = Engine_TriggerDisable(EngineCon )

        if(FunReturn.name == "LM_SUCCESS"):
            print("Succesfully Activated Pixel Trigger") 
        else:
            print("ERROR --------------------Not possible to activate the Pixel Trigger", FunReturn.value, FunReturn.name) 
            return 0



        ######## ---------------Start The Measurement

        FunReturn = Engine_MeasurementStart(EngineCon , 1 , 1856)    

        if(FunReturn.name == "LM_SUCCESS"):
            print("Succesfully Started the Measurement")    
        else:
            print("ERROR --------------------Not possible to start measurement", FunReturn.value, FunReturn.name) 
            return 0


        ######## --------- Variable Declaration

        FrameData =(lm_result * 1856)() 
        pixcount = 0



        while True:
            

            NumPacket = Engine_GetData(EngineCon ,FrameData  , 1856)
            print(" --------- Number of acquired packets ",NumPacket )



            if(NumPacket>0):
                    print(" --------- Number of acquired packets ",NumPacket )


                    for i in range(0, 1 ):
                        for j in range(0,16):
                            if( (FrameData[i].range[j]> (1)) and (j==5)):
                                print("---------Range and the ADC are ", FrameData[i].range[j], j)
                                pixcount = pixcount + 1


                    print("Pix count is for the Frame is  ", pixcount)
                    pixcount = 0
            else :
                print("Client connection  waiting for Trigger")

            time.sleep(0.2)
            





    