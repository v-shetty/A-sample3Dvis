# Created by VikasVasanth at 20/04/2022
# *Copyright (C)  - All Rights Reserved at Scantinel Photonics GmbH*

import model.GlobalFile as globalfile
import paramiko
import time
import os, signal
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, \
    QPushButton


class Setting:
    def __init__(self, mainWindow):
        self.ui = mainWindow


        self.ssh = paramiko.SSHClient()

    def updatePlot(self):
        globalfile.RangeImageIndex = self.ui.cb_range.currentIndex()
        globalfile.DopplerImageIndex = self.ui.cb_doppler.currentIndex()
        globalfile.IntensityImageIndex = self.ui.cb_intensity.currentIndex()
        print("Image selected is -------------------", globalfile.RangeImageIndex)
        globalfile.startlog = True

    def connectscanner(self):

        print("Starting connection")
        host = "192.168.20.190"
        port = 22
        username = "admin"
        password = "$cantin3l"

        if (globalfile.sbriostart):

            print("already running")

        else:

            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(host, port, username, password)
            globalfile.sbriostart = True

            stdin, stdout, stderr = self.ssh.exec_command('pgrep Controller')
            lines = stdout.readlines()

            if lines:
                print("already running killing it ")
                print(int(lines[0]))
                pidt = int(lines[0])
                cmd = "kill -9 " + str(pidt)
                self.ssh.exec_command(cmd)
                print("already running killing it ")
                # time.sleep(1)
                print("restarting it")
                self.ssh.exec_command('cd Controller; ls ; ./Controller')
                time.sleep(1)

            else:
                # self.ssh.exec_command('kill -9 1845')
                # print(" process killed")

                print("Need to start test")

                self.ssh.exec_command('cd Controller; ls ; ./Controller')
                # self.ssh.close()
                time.sleep(1)
        print("Finished Connection")
        self.ui.statusBar().showMessage("Connected")
        self.ui.statusBar().setStyleSheet(
            "background-color:green;\ncolor:white;\nborder-style:outset;\nborder-width:2px;\nborder-radius:1px;border: 5px solid green")
        self.ui.pb_connect.setEnabled(False)
        self.ui.pb_power.setEnabled(True)

        # stdin, stdout, stderr = ssh.exec_command('pgrep test')
        # lines = stdout.readlines()
        # print("Apllication already running in sbrio with ID ", lines)
        # if lines:
        # print("already running")
        # else:
        # print("Need to start test")
        # stdin, stdout, stderr = ssh.exec_command('ls')

    def LaserUpdate(self):

        globalfile.LaserON = self.ui.cb_laser.checkState()
        globalfile.Start = self.ui.cb_start.checkState()

        globalfile.LSRMan = self.ui.cb_LSRMan.checkState()
        globalfile.ChirpSim = self.ui.cb_ChirpSim.checkState()

        globalfile.ENFFT = self.ui.cb_ENFFT.checkState()
        # print(globalfile.ENFFT)

        globalfile.DEB_A = self.ui.cb_DEBA.checkState()
        globalfile.DEB_B = self.ui.cb_DEBB.checkState()
        globalfile.Raw_Acq = self.ui.cb_ENFFTEdge.checkState()
        globalfile.FFTEdge = self.ui.cb_ENFFTEdge.checkState()

        globalfile.DoTrig = self.ui.cb_DoTrig.checkState()

        globalfile.ChirpManual = self.ui.cb_ChirpMan.checkState()

        if self.ui.voa_control.text():
            globalfile.voa_control = int(float(self.ui.voa_control.text()) * 10)

        else:
            globalfile.voa_control = 10

        if self.ui.le_chirpsource.text():
            globalfile.SelectChipSource = int(self.ui.le_chirpsource.text())
        else:
            globalfile.SelectChipSource = 0

        if self.ui.le_laser_power.text():
            globalfile.amp_pwr_.amplifier_power = (self.ui.le_laser_power.text())
            globalfile.amp_pwr_.flag = 1
            print(' Some thing is written ')
        else:
            globalfile.amp_pwr_.amplifier_power = " "
        globalfile.LaserFlag = True
        # print("Laser Clicked")

    def PowerUP(self):
        globalfile.PowerBoard.port_C = [self.ui.EN_P3V.checkState(), self.ui.EN_P3V.checkState(),
                                        self.ui.EN_P5V.checkState(),
                                        self.ui.EN_P24V.checkState(), self.ui.EN_P15V.checkState(),
                                        self.ui.EN_P15V.checkState(), 0, 0]
        # print(" port c ::: ", globalfile.PowerBoard.port_C)
        globalfile.PowerBoard.port_D = [self.ui.EN_5V.checkState(), self.ui.EN_FANS.checkState(),
                                        self.ui.EN_DSP.checkState(),
                                        self.ui.EN_LASER.checkState(), self.ui.EN_SCAN_SYS.checkState(),
                                        self.ui.EN_34V.checkState(), 0, 0]

        self.ui.pb_cb_1.setChecked(True)
        self.ui.pb_cb_2.setChecked(True)
        self.ui.pb_cb_3.setChecked(True)
        self.ui.pb_cb_4.setChecked(True)
        self.ui.pb_cb_5.setChecked(True)

        globalfile.PowerBoard.voltage_enable = [globalfile.PowerBoard.bit_EN5V, globalfile.PowerBoard.bit_ENPC,
                                                globalfile.PowerBoard.bit_EN12V,
                                                globalfile.PowerBoard.bit_EN24V, globalfile.PowerBoard.bit_ENGALVO,
                                                globalfile.PowerBoard.bit_EN34V,
                                                globalfile.PowerBoard.bit_RD6, globalfile.PowerBoard.bit_RD7]

        globalfile.PowerBoard.PowerBoardFlag = True

        self.ui.pb_power.setEnabled(False)
        self.ui.pb_init.setEnabled(True)
        self.ui.statusBar().showMessage("Powered ON")
        # self.ui.pb_status.setStyleSheet("QWidget { color: %s ; background-color:dark;border-style:outset;border-color:green;border-radius:18px;border: 5px solid green; }" % QColor(69, 220, 53, 230).name())

    def Init(self):

        ret = QMessageBox.question(self.ui, 'Information', "Please wait till the Pixel Count is incremented",
                                   QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel)

        self.ui.pb_stop.setEnabled(True)
        if ret == QMessageBox.Yes:
            globalfile.Start = 2

            self.ui.cb_start.setChecked(True)
            self.ui.statusBar().showMessage("Galvo Ramping")

            time.sleep(2)

            self.ui.statusBar().showMessage("Galvo Running")

            globalfile.LaserON = 2

            self.ui.cb_laser.setChecked(True)

            self.ui.pb_init.setEnabled(False)
            #self.ui.pb_laser.setEnabled(True)


    def EngineON(self):

        ret = QMessageBox.question(self.ui, 'Information', "Turn ON the Engine Amplifier",
                                   QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel)

        if ret == QMessageBox.Yes:
            print('Laser is out')
            self.ui.statusBar().showMessage("LASER is OUT")
            #self.ui.pb_laser.setEnabled(False)
            self.ui.pb_stop.setEnabled(True)

            # self.ui.pb_logdata.setEnabled(True)
            # self.ui.pb_savefolder.setEnabled(True)



        else:
            print('Laser is not out')

    def PowerDown(self):

        #### Turn Off the Trigger
        # globalfile.ENFFT = 0

        # Galvo Down

        globalfile.LaserON = 0
        self.ui.cb_start.setChecked(False)
        self.ui.statusBar().showMessage("Galvo Ramping Down")

        time.sleep(2)

        globalfile.Start = 0

        self.ui.cb_laser.setChecked(False)

        # Power Down

        # globalfile.PowerBoard.bit_EN24V = 0
        # globalfile.PowerBoard.bit_ENGALVO = 0
        # globalfile.PowerBoard.bit_EN34V = 0
        #
        # self.ui.pb_cb_3.setChecked(False)
        # self.ui.pb_cb_4.setChecked(False)
        # self.ui.pb_cb_5.setChecked(False)
        #
        # globalfile.PowerBoard.voltage_enable = [globalfile.PowerBoard.bit_EN5V, globalfile.PowerBoard.bit_ENPC,
        #                                         globalfile.PowerBoard.bit_EN12V,
        #                                         globalfile.PowerBoard.bit_EN24V, globalfile.PowerBoard.bit_ENGALVO,
        #                                         globalfile.PowerBoard.bit_EN34V,
        #                                         globalfile.PowerBoard.bit_RD6, globalfile.PowerBoard.bit_RD7]
        globalfile.PowerBoard.Sending_data[5] = 0
        globalfile.PowerBoard.Sending_data[6] = 0
        self.ui.EN_P3V.setChecked(False)
        self.ui.EN_N3V.setChecked(False)
        self.ui.EN_P5V.setChecked(False)
        self.ui.EN_P24V.setChecked(False)
        self.ui.EN_P15V.setChecked(False)
        self.ui.EN_5V.setChecked(False)
        self.ui.EN_FANS.setChecked(False)
        self.ui.EN_DSP.setChecked(False)
        self.ui.EN_LASER.setChecked(False)
        self.ui.EN_SCAN_SYS.setChecked(False)
        self.ui.EN_34V.setChecked(False)


        globalfile.PowerBoard.PowerBoardFlag = True

        self.ui.pb_stop.setEnabled(False)
        #self.ui.pb_power.setEnabled(True)
        self.ui.gb_status.setEnabled(False)

        self.ui.statusBar().showMessage("System Turned OFF")
