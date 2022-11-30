import datetime
import os
import sys
import traceback
from ctypes import *
from enum import Enum
from os.path import join
from queue import Queue
import ctypes, ctypes.util
from copy import deepcopy
import numpy as np
from PyQt5.QtCore import pyqtSignal, QObject, QRunnable

import model.GlobalFile as globalfile


class lm_result(Structure):
    _fields_ = [("timestamp", c_uint64),
                ("FrameCounter", c_uint32),
                ("PacketCounter", c_uint32),
                ("DSPTemp", c_uint16),
                ("upChirpPeakHeight", (c_uint16 * 2) * 1856),
                ("upChirpPeakLocation", (c_uint16 * 2) * 1856),
                ("downChirpPeakHeight", (c_uint16 * 2) * 1856),
                ("downChirpPeakLocation", (c_uint16 * 2) * 1856),
                ]

class lmpath(Structure):
    _fields_ = [
        ("FrameCounter", c_int),
        ("Savepath", (c_char * 255)),
        ("saveflag", c_int),
        ("FFTsize", c_int),
        ("RangeMarker", c_int),
        ("IntensityMarker", c_int),

        ("FTR", c_float),

    ]


class frameresult(Structure):
    _fields_ = [("data", lm_result * 16)]

class lmreturn(Enum):
    LM_SUCCESS = 0
    LM_FAILURE = -1
    LM_CONNECTION_ERROR = -10
    LM_MODULE_UNAVAILABLE = -11
    LM_MODULE_ALREADY_CONFIGURED = -20
    LM_INPUT_PARAM_INVALID = -30
    LM_CONFIG_FILE_ERROR = -40


class lmdata(Structure):
    _fields_ = [("timestamp", c_uint64),
                ("triggerCount", c_uint32),
                ("range", (c_float * 16)),
                ("velocity", (c_float * 16)),
                ("upChirpPeakLocation", (c_float * 16)),
                ("upChirpPeakHeight", (c_float * 16)),
                ("downChirpPeakLocation", (c_float * 16)),
                ("downChirpPeakHeight", (c_float * 16)),
                ("status", c_uint32)]

scantinel = c_uint8 * 9
endframe = c_uint8 * 8

class Payload(Structure):
    # Defined Buffer structure
    _fields_ = [("StartFrame", scantinel),
                ("FutureUSe", c_uint8 * 23),
                ("FrameID", c_uint32),
                ("packetID", c_uint8),
                ("MetaINFO", c_uint8),
                ("TimeStamp", c_uint32),
                ("Range", ((c_float * 32) * 116)),
                ("Doppler", ((c_float * 32) * 116)),
                ("SNRData", (c_float * 32) * 116),
                ("CheckSum", c_uint32),
                ("EndFrame", endframe)]

class lmdataarray(Structure):
    _fields_ = [("box", lmdata * 16)]

class BinReader(object):
    def __init__(self, path):
        self.FTR = 1e14
        self.speed_of_light = 3e8
        self.FFT_size = 8192
        self.f_sample = 500e6
        self.wavelength = 1.55e-6
        self.num_cols = 116
        self.Vbc = -1.4373
        self.Vic = 0.00145849
        self.g_opt_deg_per_V = 4.8701
        self.num_lines = 256
        self.vfov_deg = 18.94
        self.server_on = True
        self.init_frame = -1
        self.init_packet_count = 0
        self.host = "192.168.20.165"
        self.port = 2889
        self.message = b'test'
        self.address = (self.host, self.port)
        self.queue_result = Queue()
        self.connect = False
        self.path = path


    def bin_data_extraction_binFiles(self):
        ConvertLib = cdll.LoadLibrary(os.path.dirname(__file__) + '../../../../DLL/ConvertStructure.dll')
        #os.path.dirname(__file__) + '../../../../DLL/ConvertStructure2Peaks.dll'
        #ConvertLib = cdll.LoadLibrary('./ConvertStructure.dll')

        imaged_POINTER = np.ctypeslib.ndpointer(dtype=np.float64,
                                                ndim=1,
                                                flags="C")

        Brid_convertstruct = ConvertLib.convertstruct
        Brid_convertstruct.argtypes = [ctypes.POINTER(lm_result), ctypes.POINTER(lmpath) , imaged_POINTER, imaged_POINTER, imaged_POINTER]
        Brid_convertstruct.restype = c_int

        # timeDomainPath = globalfile.savepath
        savepath = self.path

        pathinfo = lmpath()
        sep = "\\\\"
        # savepath = globalfile.savepath + sep
        pathinfo.Savepath = bytes(str(savepath),encoding="utf8")  #bytes("D:\PycharmProjects\LinuxToWindows\RawData\\", encoding="utf8")
        pathinfo.FrameCounter = c_int(123)
        pathinfo.saveflag = c_int(0)



        pathinfo.FFTsize = globalfile.FFTLength
        pathinfo.FTR = globalfile.FTR
        pathinfo.RangeMarker = globalfile.RangeMarker
        pathinfo.IntensityMarker = globalfile.IntensityMarker


        RangeDLL = np.zeros((29696), dtype=np.float64)
        DopplerDLL = np.zeros((29696), dtype=np.float64)
        IntensityDLL = np.zeros((29696), dtype=np.float64)
        RangeUpChirpDLL = np.zeros((29696), dtype=np.float64)
        RangeDownChirpDLL = np.zeros((29696), dtype=np.float64)
        IntensityUpChirpDLL = np.zeros((29696), dtype=np.float64)
        IntensityDownChirpDLL = np.zeros((29696), dtype=np.float64)

        FrameData = (lm_result * 16)()
        rangeimageupc1 = np.zeros((116, 256))
        rangeimageupc2 = np.zeros((116, 256))
        totalpacket = 0
        packetwatch = 0
        packetfiller = 0
        Skippedpackets = 0
        framecounter = 0

        f = open(savepath, 'rb')  # TODO

        data = f.read()
        payload_in = frameresult.from_buffer_copy(data)

        for i in range(16):
            FrameData[i] =payload_in.data[i]

        ###apply the DLL and have a image
        ret = Brid_convertstruct(FrameData, pathinfo, RangeDLL, DopplerDLL, IntensityDLL)
        framenumber = FrameData[0].FrameCounter


        temprange = deepcopy(RangeDLL.reshape((116, 256)))
        tempintensity = deepcopy(IntensityDLL.reshape((116, 256)))
        tempdoppler = deepcopy(DopplerDLL.reshape((116, 256)))

        if (framenumber % 2 == 0):
            globalfile.rangeimage = np.fliplr(temprange[::-1])
            globalfile.intensityimage = np.fliplr(tempintensity[::-1])
            globalfile.dopplerimage  = np.fliplr(tempdoppler[::-1])

            globalfile.intensityimage[globalfile.intensityimage > 30] = 30
            globalfile.intensityimage[0, 0] = 32

        else:
            globalfile.rangeimage = np.fliplr(temprange)
            globalfile.intensityimage = np.fliplr(tempintensity)
            globalfile.dopplerimage = np.fliplr(tempdoppler)

            globalfile.intensityimage[globalfile.intensityimage > 30] = 30
            globalfile.intensityimage[0, 0] = 32

        rangeimage3dinput = np.flip(temprange, 1)
        intensityimage3dinput = np.flip(tempintensity, 1)
        dopplerimage3dinput = np.flip(tempdoppler, 1)
        data2D = (rangeimage3dinput, dopplerimage3dinput, intensityimage3dinput, framenumber)

        return data2D







