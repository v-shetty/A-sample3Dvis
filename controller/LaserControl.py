import socket
from ctypes import *
import json
import numpy as np
from PyQt5.QtCore import *

import time
import traceback, sys
import model.GlobalFile as globalfile
import array as arr

import os


# pragma pack(1)
class tempLoad(Structure):
    _pack_ = 1
    _fields_ = [
        ("INTLCK", c_uint32),
        ("LSREN", c_uint32),
        ("pixcount", c_uint32),
        ("SMID", c_uint32),
        ("TimeStampBase", c_uint32),
        ("TimeStampMicro", c_uint32),
        ("LA_TEMP", c_float),
        ("LA_CUR", c_float),
        ("NTC_NW", c_float),
        ("NTC_NE", c_float),
        ("NTC_SW", c_float),
        ("NTC_SE", c_float),
        ("NTC_HotPlate", c_float),
        ("NTC_ColdPlate", c_float),
        ("NTC_Main", c_float),
        ("NTC_NDriver", c_float),
        ("NTC_SDriver", c_float),
        ("amplifier_power", c_char * 15),
    ]


class LaserLoad(Structure):
    _fields_ = [
        ("PreChirpDelay", c_uint32),
        ("CurrentPixCount", c_uint32),
        ("LastPixCount", c_uint32),
        ("DoTrig", c_uint32),
        ("Tdd", c_uint32),
        ("Tdu", c_uint32),
        ("Flag", c_uint32),
        ("Laser", c_uint32),
        ("Start", c_uint32),
        ("LaserManual", c_uint32),
        ("ChirpSimEn", c_uint32),
        ("ENFFT", c_uint32),
        ("DEB_A", c_uint32),
        ("DEB_B", c_uint32),
        ("FFT_Edge", c_uint32),
        ("PauseAftRDATrig", c_uint16),
        ("SelectChipSource", c_uint16),
        ("Raw_Acq", c_uint8),
        ("SelectDIO", c_uint8),
        ("DelayRDATrig", c_uint8),
        ("ChirpManual", c_uint8),
        ("VOA_control", c_uint8),
        ("amplifier_power", c_char * 15)

    ]


class WorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(float)


class LaserControl(QRunnable):
    '''
    Worker thread
    '''

    def __init__(self, fn, *args, **kwargs):
        super(LaserControl, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        # Add the callback to our kwargs
        self.kwargs['progress_callback'] = self.signals.progress

    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''

        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done


def Run_Laser(progress_callback):
    HOST = '192.168.20.190'  # Standard loopback interface address (localhost)
    PORT = 2032  # Port to listen on (non-privileged ports are > 1023)
    print("Starting the server for Laser Thread ")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_addr = (HOST, PORT)
    s.connect(server_addr)
    print('Client connection accepted for Laser thread ')

    while 1:

        if (1):

            # payload_out = LaserLoad(c_uint32(1), c_uint32(globalFile.LaserON), c_uint32(globalFile.Start), c_uint32(globalFile.LSRMan),c_uint32(globalFile.ChirpSim), c_uint32(globalFile.ENFFT), c_uint32(globalFile.DEB_A), c_uint32(globalFile.DEB_B), c_uint32(globalFile.Raw_Acq), c_uint8(globalFile.selectDB) ,c_uint32(globalFile.PreChirpDelay),c_uint32(globalFile.CurrentPixCount),c_uint32(globalFile.LastPixCount) , c_uint32(globalFile.DoTrig) , c_uint8(globalFile.DelayRDATrig)  , c_uint16(globalFile.PauseAftRDATrig), c_uint32(globalFile.Tdd) , c_uint32(globalFile.Tdu), c_uint16(globalFile.SelectChipSource), c_uint8(globalFile.ChirpManual))
            payload_out = LaserLoad()
            payload_out.Laser = c_uint32(globalfile.LaserON)
            payload_out.Start = c_uint32(globalfile.Start)
            payload_out.LaserManual = c_uint32(globalfile.LSRMan)
            payload_out.ChirpSimEn = c_uint32(globalfile.ChirpSim)
            payload_out.ENFFT = c_uint32(globalfile.ENFFT)
            payload_out.DEB_A = c_uint32(globalfile.DEB_A)
            payload_out.DEB_B = c_uint32(globalfile.DEB_B)
            # print("----------ChirpManual is ", globalfile.FFTEdge)

            payload_out.FFT_Edge = c_uint32(globalfile.FFTEdge)
            # print("from file ", globalfile.ENFFT)

            payload_out.Raw_Acq = c_uint8(globalfile.Raw_Acq)
            payload_out.SelectDIO = c_uint8(globalfile.SelectDIO)

            payload_out.PreChirpDelay = c_uint32(globalfile.PreChirpDelay)
            payload_out.CurrentPixCount = c_uint32(globalfile.CurrentPixCount)
            payload_out.LastPixCount = c_uint32(globalfile.LastPixCount)

            payload_out.DoTrig = c_uint32(globalfile.DoTrig)
            payload_out.DelayRDATrig = c_uint8(globalfile.DelayRDATrig)
            payload_out.PauseAftRDATrig = c_uint16(globalfile.PauseAftRDATrig)
            payload_out.Tdd = c_uint32(globalfile.Tdd)
            payload_out.Tdu = c_uint32(globalfile.Tdu)
            payload_out.SelectChipSource = c_uint16(globalfile.SelectChipSource)
            payload_out.ChirpManual = c_uint8(globalfile.ChirpManual)

            payload_out.VOA_control = c_uint8(globalfile.voa_control)

            if globalfile.amp_pwr_.flag == 1:
                payload_out.Flag = c_uint32(globalfile.amp_pwr_.flag)
                payload_out.amplifier_power = bytes(globalfile.amp_pwr_.amplifier_power + "\r\n", encoding='utf-8')
                print(" LASER amplifier command send")
            s.sendall(payload_out)
            globalfile.LaserFlag = True
            # print("send all")
            paysize = sizeof(tempLoad)
            data = s.recv(paysize)
            # print("recived all")
            payload_in = tempLoad.from_buffer_copy(data)
            # print(" Received amplifier buffer value is", payload_in.amplifier_power)
            TempArray = [payload_in.NTC_NW, payload_in.NTC_NE, payload_in.NTC_SW, payload_in.NTC_SE,
                         0, payload_in.NTC_Main, payload_in.NTC_ColdPlate, payload_in.NTC_NDriver,
                         payload_in.NTC_SDriver, payload_in.INTLCK, payload_in.LSREN, payload_in.pixcount,
                         payload_in.SMID]
            # print("NTC main ",  payload_in.NTC_Main)
            globalfile.NTCData = TempArray
            globalfile.amp_pwr_.amp_receive = payload_in.amplifier_power
            globalfile.TimeStampBase = payload_in.TimeStampBase
            globalfile.TimeStampMicro = payload_in.TimeStampMicro
            globalfile.laser_temp = payload_in.LA_TEMP
            globalfile.laser_current = payload_in.LA_CUR

            # print("Time Stamp Base  ",payload_in.TimeStampBase )
            # print("Time Stamp Micro  ",payload_in.TimeStampMicro )

            with open('TempStorage.txt', 'a') as f:
                f.write(str(round(TempArray[5], 3)) + " " + str(round(TempArray[0], 3)) + " " + str(
                    round(TempArray[1], 3)) + " " + str(round(TempArray[2], 3)) + " " + str(
                    round(TempArray[3], 3)) + " " + str(round(TempArray[4], 3)) + " " + str(
                    round(TempArray[7], 3)) + " " + str(
                    round(TempArray[8], 3)) + " " + str(round(globalfile.laser_temp, 3)) + " " +
                        str(round(globalfile.laser_current, 3)) + " " + str(round(globalfile.PowerBoard.PB_TEMP1, 3))
                        + " " + str(round(globalfile.PowerBoard.PB_TEMP2, 3)) +
                        " " + "\n")  # the line I needed to have printed via a loop
            # print("written temp")
            # progress_callback.emit(round(TempArray[globalfile.TempSource], 4))
            progress_callback.emit(payload_in.SMID)
            # print("call back temp")
            time.sleep(0.1)
        else:

            print("Waiting for the Laser Command")
            time.sleep(1)


def Print_Laser(s):
    print(s)


def Exit_Laser():
    print("THREAD COMPLETE! for Laser")
