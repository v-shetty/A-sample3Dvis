# Created by VikasVasanth at 03/05/2022
# *Copyright (C)  - All Rights Reserved at Scantinel Photonics GmbH*
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget
from matplotlib import cm
import pyqtgraph as pg
from view.colorbar import ColorBarItem
import model.GlobalFile as globalfile

from random import randint
from ctypes  import *
import time

import os
from os.path import join

import scipy.io
import numpy as np

import sys
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

class frameresult(Structure):
    _fields_= [ ("data" , lm_result*1856)


    ]


class VisWindowTimeDomain(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self):
        super().__init__()

        self.setWindowTitle("DSP")
        self.resize(650, 650)

        layout = QVBoxLayout()

        #################### DSP Visualization ###########################################################
        #colormap = cm.get_cmap("viridis")
        colormap = cm.get_cmap("jet")
        colormap._init()
        lut = (colormap._lut * 255).view(np.ndarray)  # Convert matplotlib colormap from 0-1 to 0 -255 for Qt


        self.canvas = pg.GraphicsLayoutWidget()
        layout.addWidget(self.canvas)
        self.canvas.setAspectLocked(True)




        ############# plot time domain --------------------
        

        self.timeplot = self.canvas.addPlot(title="Time domain Image")



        self.x = np.zeros((16384,), dtype=float).tolist()
        self.y = np.arange(start=1, stop=16385, step=1).tolist()

        #self.timedomain = pg.plot()
        #self.timedomain.plot(self.x ,self.y )

        self.dataline = self.timeplot.plot(self.x ,self.y)



        ############plot time domain average
        self.canvas.nextRow()

        self.timeplotavg = self.canvas.addPlot(title="FFT spectrum on Time Domain Data")


        self.xavg = np.arange(8192).tolist()
        self.yavg = np.arange(start=1, stop=8193, step=1).tolist()

        #self.timedomain = pg.plot()
        #self.timedomain.plot(self.x ,self.y )

        self.datalineavg = self.timeplotavg.plot(self.xavg ,self.yavg)
        #-----------------time domain

        #self.label = QLabel("Another Window2")
        #layout.addWidget(self.label)
        self.setLayout(layout)

        self.maxrange = 2
        self.minrange = 8

        self.maxInt = 2
        self.minInt = 8

        self.offlinedata = False
        self.filelist = []
        self.cIndexC = 0
        if (self.offlinedata):
            loadpath = r"D:\PycharmProjects\LinuxToWindows\Engine3_dopplerOnly"
            self.filelist = self.get_file_list(loadpath)


        ###timedomaindata -------------------------
        self.time_update()
        self.timeavg_update()



    def get_file_list(self,dataset_path):
        test_file_list = []

        for f in np.sort(os.listdir(dataset_path)):
            test_file_list.append([join(dataset_path, f)])

        test_file_list = np.concatenate(test_file_list, axis=0)
        return test_file_list

    
    def time_update(self):


        #data = np.full((116, 256), 100)
        #data = globalfile.DopplerImage

        value = randint(200, 300)
        beg = 100-value


        self.y = globalfile.timedomain
        self.x = globalfile.frebins


        #self.timeplot.plot(self.x ,self.y)

        self.dataline.setData(self.x ,self.y)
        
      
        QtCore.QTimer.singleShot(1, self.time_update)


    def timeavg_update(self):


        #data = np.full((116, 256), 100)
        #data = globalfile.DopplerImage

        #value = randint(200, 300)
        #beg = 100-value


        self.yavg = globalfile.timedomainavg
        self.xavg = globalfile.frequencybins

        #self.timeplot.plot(self.x ,self.y)

        self.datalineavg.setData(self.xavg ,self.yavg)
        
      
        QtCore.QTimer.singleShot(1, self.timeavg_update)    