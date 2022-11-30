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


class VisWindow(QWidget):
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

        #----------------------Range Visualization --------------------------------------#

        # RangePlot = self.canvas.addPlot(title="Range Image")
        # #RangePlot.hideAxis('left')
        # #RangePlot.hideAxis('bottom')
        # self.RangeImg = pg.ImageItem(border='w')
        # self.RangeImg.setLookupTable(lut)
        # RangePlot.addItem(self.RangeImg)   ###########################################globalfile.rangemax
        # Rangebar = ColorBarItem(interactive=False , cmap=colormap,values=(0, globalfile.rangemax) , label = "meters(m)") #0, globalfile.rangemax
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
        # Dopplerbar = ColorBarItem(interactive=False, cmap=colormap, values=(globalfile.dopplermin, globalfile.dopplermax), colorMap=cmap)
        # #Dopplerbar.hideAxis('right')
        # Dopplerbar.setImageItem(self.Dopplerimg, insert_in=DopplerPlot)
        # self.Dopplerimg.setLookupTable(lut)


        ############# plot time domain --------------------
        

        self.timeplot = self.canvas.addPlot(title="Time domain Image")



        self.x = np.zeros((16384,), dtype=float).tolist()
        self.y = np.arange(start=1, stop=16385, step=1).tolist()

        #self.timedomain = pg.plot()
        #self.timedomain.plot(self.x ,self.y )

        self.dataline = self.timeplot.plot(self.x ,self.y)



        ############plot time domain average
        self.canvas.nextRow()

        self.timeplotavg = self.canvas.addPlot(title="Time domain Image Averaged over 16")


        self.xavg = np.arange(8192).tolist()
        self.yavg = np.arange(start=1, stop=8193, step=1).tolist()

        #self.timedomain = pg.plot()
        #self.timedomain.plot(self.x ,self.y )

        self.datalineavg = self.timeplotavg.plot(self.xavg ,self.yavg)
        #-----------------time domain

        # # #----------------------Intensity Visualization --------------------------------------#
        # self.canvas.nextRow()
        # #
        # IntensityPlot = self.canvas.addPlot(title="Intensity Image")
        # # IntensityPlot.hideAxis('left')
        # # IntensityPlot.hideAxis('bottom')
        # #
        # self.Intensityimg = pg.ImageItem()
        # self.Intensityimg.setLookupTable(lut)
        # IntensityPlot.addItem(self.Intensityimg)
        # #
        # cmap = cm.get_cmap("viridis")
        # Intensitybar = ColorBarItem(interactive=False, cmap=colormap,values=(0, 200),label = "Linear Magnitude", colorMap=cmap, )
        # # #Intensitybar.hideAxis('right')
        # Intensitybar.setImageItem(self.Intensityimg, insert_in=IntensityPlot)
        # #
        # self.Intensityimg.setLookupTable(lut)

       




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


        #self.range_update()
        #self.doppler_update()
        #self.intensity_update()



        ###timedomaindata -------------------------
        self.time_update()
        self.timeavg_update()






    def range_update(self):





        #globalfile.rangeimage = np.full((116, 256), 10, dtype='f')

        #rstop = time.time()
        #data =  np.zeros((116, 256))  ###cartsial coordinate system
        #data[115][254] = float(16)#####right bottom corner
        #data[115][0] = 230#right corner
        #data1 = np.random.randint(16, size=(116, 256))
        #data1 = np.empty([256, 70])
        #data1.fill(220)
        #data1[0:10][0:10] = 10
        #data = np.random.randint(256, size=(70, 256))
        #print(globalfile.RangeImage[50][50])

        #for j in range(116):
            #for k in range(256):
                #pass#data[j][k] = 16


        #self.RangeImg.setImage(data)




        ####Activate later
        if( globalfile.RangeImageIndex == 0):
            self.RangeImg.setImage(globalfile.rangeimageup)
            #self.RangeImg.setImage(globalfile.rangeimageup * (255.0/globalfile.rangemax) )



        elif (globalfile.RangeImageIndex == 1):
            self.RangeImg.setImage(globalfile.rangeimageup * (255.0/globalfile.rangemax) )

        elif (globalfile.RangeImageIndex == 2):
            self.RangeImg.setImage(globalfile.rangeimagedown * (255.0/globalfile.rangemax))

        time.sleep(0.2)
        QtCore.QTimer.singleShot(1, self.range_update)
        #rstart = time.time()

        #print("Time from Range ", (rstart - rstop))



    def doppler_update(self):

        divisorfactor = 255/(globalfile.dopplermax - globalfile.dopplermin)

        addfactorarry = np.full((116, 256),128 , dtype='f')

        for i in range(1, 110):
            for j in range(1,210):
                if((globalfile.dopplerimage[i][j] * divisorfactor)+128 > 180):
                    print(" they are ",globalfile.dopplerimage[i][j] ,  (globalfile.dopplerimage[i][j] * divisorfactor)+128)






        #data = np.full((116, 256), 100)
        #data = globalfile.DopplerImage
        #self.Dopplerimg.setImage(data)

        self.Dopplerimg.setImage((globalfile.dopplerimage * divisorfactor) + addfactorarry )
        QtCore.QTimer.singleShot(1, self.doppler_update)

        #time.sleep(0.1)
        #print("Time from Doppler ", (dstop - dstart))


    def intensity_update(self):



        # #############read the bin file




        if (self.offlinedata):
            self.cIndexC = (self.cIndexC + 1) % 20

            #print("------index is ", self.cIndexC)


            FrameData = (lm_result * 1856)()
            paysize = sizeof(FrameData)
            file_path = self.filelist[globalfile.offlineIndex]
            f = open(file_path, 'rb')
            data = f.read()
            payload_in = frameresult.from_buffer_copy(data)
            ch_lut =  [0,2,4,6,8,10,12,14,1,3,5,7,9,11,13,15]

            cnt = -1
            for j in range(1856):
                for k in range(16):
                    cindex = ch_lut[k]

                    if (cnt >= 255):
                        cnt = 0
                    else:
                        cnt = cnt + 1

                    if (globalfile.offlineIndex % 2 == 0):



                        globalfile.intensityimage[int(j / 16)][k * 16 + (j % 16)] = payload_in.data[j].downChirpPeakHeight[cindex][0]
                        globalfile.rangeimageup[int(j / 16)][k * 16 + (j % 16)] = payload_in.data[j].range[cindex]


                        #globalfile.intensityimage[int(j / 16)][cnt ] = payload_in.data[j].downChirpPeakHeight[k][0]
                        #globalfile.rangeimageup[int(j / 16)][cnt ] = payload_in.data[j].range[k]


                    else:
                        globalfile.intensityimage[115 -int(j / 16)][k * 16 + (j % 16)] = payload_in.data[j].downChirpPeakHeight[cindex][0]
                        globalfile.rangeimageup[115 -int(j / 16)][k * 16 + (j % 16)] = payload_in.data[j].range[cindex]

                        #globalfile.intensityimage[int(j / 16)][cnt ] = payload_in.data[j].downChirpPeakHeight[k][0]
                        #globalfile.rangeimageup[int(j / 16)][cnt ] = payload_in.data[j].range[k]
                        #globalfile.rangeimageup[int(j / 16)][cnt ] = payload_in.data[j].range[k]



            ####Load Manually

            #mat1 = scipy.io.loadmat(r'D:\MATLAB\134\220504_Scantinel_Firmware_Version_134_ES\102228_Scantinel_Matlab_DAQ_For102220\trunk\ClientFiles\rangeImageshow.mat')
            # mat2 = scipy.io.loadmat(r'D:\MATLAB\134\220504_Scantinel_Firmware_Version_134_ES\102228_Scantinel_Matlab_DAQ_For102220\trunk\ClientFiles\intensityimageshow.mat')

            #data1 = mat1.get('rangeImage')
            #globalfile.rangeimageup = np.array(data1)

            #data2 = mat2.get('intensityimage')
            #globalfile.intensityimage = np.array(data2)



        #
        #globalfile.intensityimage[0, 0] = 50
        #print("-----", np.min(globalfile.intensityimage) ,np.max(globalfile.intensityimage) )
        if( globalfile.IntensityImageIndex == 0):
            self.Intensityimg.setImage(globalfile.intensityimage )

        elif (globalfile.IntensityImageIndex == 1):
            self.Intensityimg.setImage(globalfile.intensityimageup )

        elif (globalfile.IntensityImageIndex == 2):
            self.Intensityimg.setImage(globalfile.intensityimagedown )
        
      
        QtCore.QTimer.singleShot(1, self.intensity_update)



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