from ctypes import *
from enum import Enum
from queue import Queue

import os

import numpy as np
import re

class lm_result(Structure):
    _fields_ = [("timestamp", c_uint64),
                ("triggerCount", c_uint32),
                ("range", (c_float * 16)),
                ("velocity", (c_float * 16)),
                ("upChirpPeakLocation", (c_float * 4) * 16),
                ("upChirpPeakHeight", (c_float * 4) * 16),
                ("downChirpPeakLocation", (c_float * 4) * 16),
                ("downChirpPeakHeight", (c_float * 4) * 16)]


class frameresult(Structure):
    _fields_ = [("data", lm_result * 1856) ]


class Connectionload(Structure):
    _fields_ = [("ethernetBufferSize", c_uint32),
                ("ipAddressString", (c_char * 40)),
                ("ethernetPort", (c_char * 6)),
                ("configurationFilePath", (c_char * 255))]

class lmpath(Structure):
    _fields_ = [
        ("ethernetBufferSize", c_int),
        ("Savepath", (c_char * 255))]

class MatLoad(Structure):
    _fields_ = [("ChirpManual", c_uint32),
                ("TrigManual", c_uint32),
                ("FFTTRig", c_uint32),
                ("CurrentPixCount", c_uint32),
                ("LastPixCount", c_uint32),
                ("ERDATrig", c_uint32),
                ("FFTEdge", c_uint32)]

class PeakSearchLoad(Structure):
    _fields_ = [("peakSearchWindowStart_m", c_float),
                ("peakSearchWindowEnd_m", c_float),
                ("peakHeightThreshold", c_float),
                ("peakSpacingMinimum_m", c_float)]

class lmreturn(Enum):
    LM_SUCCESS = 0
    LM_FAILURE = -1
    LM_CONNECTION_ERROR = -10
    LM_MODULE_UNAVAILABLE = -11
    LM_MODULE_ALREADY_CONFIGURED = -20
    LM_INPUT_PARAM_INVALID = -30
    LM_CONFIG_FILE_ERROR = -40

class lmtrig(Enum):
    LM_TRIGGER_MULT_SHOT = 0
    LM_TRIGGER_CONTINUOUS = 1

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


class CarlaBinReader(object):
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

        self.FrameData = (lm_result * 1856)()
        self.paysize = sizeof(self.FrameData)
        self.path = path
        with open(self.path, "rb") as f:
            self.payload_in = frameresult.from_buffer_copy(f.read())

    def bin_data_extraction_carlaFiles(self):
        # print("bin_data_extraction_bin")

        path = self.path
        data2D = None

        file_name_ = os.path.basename(path)
        file_name = os.path.splitext(file_name_)
        file_name_idx = re.findall("[0-9]+", file_name[0])[0]

        if path != '':
            rangeImage = np.zeros((116,256))
            velocity = np.zeros((116, 256))
            carlaReader = self
            ch_lut = np.arange(16)

            for j in range(1856):
                for k in range(16):
                    cindex = ch_lut[k]
                    velocity[int(j/16)][k * 16 + (j % 16)] = carlaReader.payload_in.data[j].velocity[cindex]
                    rangeImage[int(j/16)][k * 16 + (j % 16)] = carlaReader.payload_in.data[j].range[cindex]


            if (int(file_name_idx) % 2 == 0):
                data2D = (rangeImage[::-1], velocity[::-1])
            elif (int(file_name_idx) %2 != 0):
                data2D = (rangeImage, velocity)

        return data2D












