from ctypes import *
from enum import Enum
import ctypes, ctypes.util
from PyQt5.QtCore import *
import traceback, sys
import socket
import time
import pickle
import numpy as np
import model.GlobalFile as globalfile
from copy import deepcopy
import os
import time
from enum import IntEnum
import numpy.ctypeslib as npct
from Visualizer3D import model                              

from scipy.fftpack import fft, rfft, fftfreq
from os.path import join

scantinel = c_uint8 * 9
endframe = c_uint8 * 8

Rangedatatype = (c_float * 29) * 256
MaxPAcketSize = 48

np.seterr(divide = 'ignore')
class MatLoad(Structure):
    _fields_ = [("ChirpManual", c_uint32),
                ("TrigManual", c_uint32),
                ("FFTTRig", c_uint32),

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


class BRAMData(Structure):
    _fields_ = [
        ("BRAMMode", c_uint16),
        ("Index", c_uint16),
        ("Window", (c_uint16 * 512)),
    ]


class ModeSelector(Structure):
    _fields_ = [
        ("SetWindow", c_uint8),
        ("FFTMode", c_uint8),
        ("TimeDomainMode", c_uint8),
        ("FFTSize", c_uint8),

    ]


###############
## 0 is Write FFT config
## 1 is Write Window config
## 2 is Read FFT Data
## 3 is Read Time Domain Data

class Configuration(Structure):
    _fields_ = [
        ("Configuration", c_uint8),

    ]


class FFTConfig(Structure):
    _fields_ = [

        ("FFTSize", c_uint16),
        ("Detection", c_uint16),

    ]


class PacketConfig(Structure):
    _fields_ = [
        ("ModeSelector", c_uint16),
        ("WindowMin", c_uint16),
        ("WindowMax", c_uint16),
        ("PeakMinDist", c_uint16),
        ("CFARCoeff", c_uint16),
        ("CFAROffset", c_uint16),
        ("PrimaryADC", c_uint16),
        ("ConstThresh", c_uint16),
        ("ADCScale", c_uint16),
        ("ADCReset", c_uint16),
    ]


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


class lm_triggerMode(Enum):
    LM_TRIGGER_MULT_SHOT = 0
    LM_TRIGGER_CONTINUOUS = 1


class lm_peakSearch(Structure):
    _fields_ = [("peakSearchWindowStart_m", c_float),
                ("peakSearchWindowEnd_m", c_float),
                ("peakHeightThreshold", c_float),
                ("peakSpacingMinimum_m", c_float),
                ]


class lm_return(Enum):
    LM_SUCCESS = 0
    LM_FAILURE = -1
    LM_CONNECTION_ERROR = -10
    LM_MODULE_UNAVAILABLE = -11
    LM_MODULE_ALREADY_CONFIGURED = -20
    LM_INPUT_PARAM_INVALID = -30
    LM_CONFIG_FILE_ERROR = -40


class lm_result(Structure):
    _fields_ = [("timestamp", c_uint64),
                ("FrameCounter", c_uint32),
                ("PacketCounter", c_uint32),
                ("range", (c_float * 16)),
                ("velocity", (c_float * 16)),
                ("upChirpPeakLocation", (c_float * 4) * 16),
                ("upChirpPeakHeight", (c_float * 4) * 16),
                ("downChirpPeakLocation", (c_float * 4) * 16),
                ("downChirpPeakHeight", (c_float * 4) * 16),

                ]


class lm_resultUDP(Structure):
    _fields_ = [("timestamp", c_uint64),
                ("FrameCounter", c_uint32),
                ("PacketCounter", c_uint32),
                ("DSPTemp", c_uint16),

                ("upChirpPeakHeight", (c_uint16 * 2) * 1856),
                ("upChirpPeakLocation", (c_uint16 * 2) * 1856),

                ("downChirpPeakHeight", (c_uint16 * 2) * 1856),
                ("downChirpPeakLocation", (c_uint16 * 2) * 1856 ),

                ]

class BRAMProgress(Structure):
    _fields_ = [
        ("Flag", c_uint32),
        ("Index", c_uint32),

    ]


class lm_resultarray(Structure):
    _fields_ = [("data", (lm_result * MaxPAcketSize)),

                ]
# class lm_resultarrayUDP(Structure):
#     _fields_ = [("data", (lm_resultUDP )),]


class lm_matlabarray(Structure):
    _fields_ = [("data", (c_uint16 * 29696)),

                ]
class lm(Structure):
    _fields_ = [("ethernetBufferSize", c_uint32),
                ("ipAddressString", (c_char * 40)),
                ("ethernetPort", (c_char * 6)),
                ("configurationFilePath", (c_char * 255)),
                ("configFftSize", c_uint32)

                ]
class RawData(Structure):
    _pack_ = 1
    _fields_ = [("ADCNumber", c_uint16),
                ("DSPTemp", c_uint16),
                ("FrameNumber", c_uint32),
                ("ChannelData", (c_uint16 * 16384)),

                ]

class WorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(float)


class Acquire(QRunnable):

    def __init__(self, fn, *args, **kwargs):
        super(Acquire, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        # Add the callback to our kwargs
        self.kwargs['progress_callback'] = self.signals.progress

    def run(self):

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


def AcquireThread(progress_callback):
    #ConvertLib = cdll.LoadLibrary('./ConvertStructure.dll')
    ConvertLib = cdll.LoadLibrary(os.path.dirname(__file__) + '/../DLL/ConvertStructure.dll')

    imaged_POINTER = np.ctypeslib.ndpointer(dtype=np.float64,
                                            ndim=1,
                                            flags="C")

    Brid_convertstruct = ConvertLib.convertstruct
    Brid_convertstruct.argtypes = [ctypes.POINTER(lm_resultUDP), ctypes.POINTER(lmpath) , imaged_POINTER, imaged_POINTER, imaged_POINTER]
    Brid_convertstruct.restype = c_int

    timeDomainPath = globalfile.savepath

    pathinfo = lmpath()
    sep = "\\\\"
    savepath = globalfile.savepath + sep
    pathinfo.Savepath = bytes(str(savepath),encoding="utf8")  #bytes("D:\PycharmProjects\LinuxToWindows\RawData\\", encoding="utf8")
    pathinfo.FrameCounter = c_int(123)
    pathinfo.saveflag = c_int(1)
    pathinfo.FFTsize = c_int(16384)
    pathinfo.RangeMarker = c_int(0)
    pathinfo.IntensityMarker = c_int(0)
    pathinfo.FTR = c_float(1)





    RangeDLL = np.zeros((29696), dtype=np.float64)
    DopplerDLL = np.zeros((29696), dtype=np.float64)
    IntensityDLL = np.zeros((29696), dtype=np.float64)
    RangeUpChirpDLL = np.zeros((29696), dtype=np.float64)
    RangeDownChirpDLL = np.zeros((29696), dtype=np.float64)
    IntensityUpChirpDLL = np.zeros((29696), dtype=np.float64)
    IntensityDownChirpDLL = np.zeros((29696), dtype=np.float64)



    print('Create a socket on the host PC client.')
    lwIP_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print('Connecting to the socket of the DSP server.')
    lwIP_server_address = ('192.168.20.10', 7)
    lwIP_socket.connect(lwIP_server_address)
    print("connection success")
    print("------- Waiting for Trigger--------")



    FrameData = (lm_resultUDP * 16)()
    totalpacket = 0
    packetwatch = 0
    packetfiller = 0
    Skippedpackets = 0
    framecounter = 0

    #### Send FFT configuration

    ffttemplate = FFTConfig()
    ffttemplate.FFTSize = globalfile.FFTLength
    ffttemplate.Detection = globalfile.detectionmode

    lwIP_socket.sendall(ffttemplate)
    time.sleep(0.5)
    #####################

    ######## send point cloud mode

    PacketSetting = PacketConfig()
    PacketSetting.WindowMin = globalfile.RangeMinBin
    PacketSetting.WindowMax = globalfile.RangeMaxBin
    PacketSetting.PeakMinDist = globalfile.PeakSpaceBin
    PacketSetting.CFARCoeff = globalfile.CFARCoeff
    PacketSetting.CFAROffset = globalfile.CFAROffset
    PacketSetting.PrimaryADC = globalfile.ADCCH1
    PacketSetting.ConstThresh = globalfile.ConstThresh
    PacketSetting.ADCScale = globalfile.ADCscale
    PacketSetting.ADCReset = globalfile.ADCreset
    #########################################

    ########## ------------- Write to FFT Window BRAM ----------------- ##########################

    BRAMContent = BRAMData()
    BRAMFFTWindowFlag = False
    BRAMProgressSize = sizeof(BRAMProgress)
    BramIndex = 0;
    BRAMDataFile = np.load('BRAMData.npz')  ###### Store your npy here

    FFTwindow = BRAMDataFile['BRAMFFTWindowArray']
    PeakMask = BRAMDataFile['BRAMPeakMaskArray']

    bramcounter = -1
    while (BRAMFFTWindowFlag):

        bramcounter = bramcounter + 1
        BRAMContent.BRAMMode = 0  # select FFT Window write
        BRAMContent.Index = BramIndex

        setdata = np.array(FFTwindow[BramIndex: (BramIndex + 512)], dtype='ushort')
        BRAMContent.Window = npct.as_ctypes(setdata)
        lwIP_socket.sendall(BRAMContent)

        BRAmProgressdata = lwIP_socket.recv(BRAMProgressSize)
        BRAmProgressdata_in = BRAMProgress.from_buffer_copy(BRAmProgressdata)

        if (BRAmProgressdata_in.Index == (BramIndex + 1)):
            BramIndex = BramIndex + 512

        if (BramIndex == 8192):
            BRAMFFTWindowFlag = False
            BramIndex = 0;



    ############# ------------ write Noise floor balance for Peak Masking -------#######################

    BRAMPeakMaskFlag = False
    paydata = np.load("FFTwindow.npy")  ###### Store your npy here
    while (BRAMPeakMaskFlag):
        BRAMContent.BRAMMode = 1  # select FFT Window write
        BRAMContent.Index = BramIndex

        setdata = np.array(PeakMask[BramIndex: (BramIndex + 512)], dtype='ushort')
        BRAMContent.Window = npct.as_ctypes(setdata)
        lwIP_socket.sendall(BRAMContent)

        BRAmProgressdata = lwIP_socket.recv(BRAMProgressSize)
        BRAmProgressdata_in = BRAMProgress.from_buffer_copy(BRAmProgressdata)

        if (BRAmProgressdata_in.Index == (BramIndex + 1)):
            BramIndex = BramIndex + 512

        if (BramIndex == 8192):
            BRAMPeakMaskFlag = False
            BramIndex = 0;

    #################################------------ ############################

    ###select the mode of the DSP

    PacketSetting.ModeSelector = globalfile.DSPMode

    ########## time domain setting

    channelA = np.zeros((16384,), dtype=float)#np.random.random(1, size=8192)

    Fs = 500e6
    N = 16384
    frebins = np.arange(0, N)*Fs/N
    timeaxis = np.arange(0, N)


    starttime = time.time()
    while True:


        PacketSetting.WindowMin = globalfile.RangeMinBin
        PacketSetting.WindowMax = globalfile.RangeMaxBin

        PacketSetting.PeakMinDist = globalfile.PeakSpaceBin
        PacketSetting.CFARCoeff = globalfile.CFARCoeff
        PacketSetting.CFAROffset = globalfile.CFAROffset

        PacketSetting.PrimaryADC = globalfile.ADCCH1

        PacketSetting.ConstThresh = globalfile.ConstThresh
        PacketSetting.ADCScale = globalfile.ADCscale
        PacketSetting.ADCReset = globalfile.ADCreset

        ####  --- save path ------
        savepath = globalfile.savepath + sep
        pathinfo.Savepath = bytes(str(savepath), encoding="utf8")
        pathinfo.FFTsize = globalfile.FFTLength
        pathinfo.FTR = globalfile.FTR
        pathinfo.RangeMarker = globalfile.RangeMarker
        pathinfo.IntensityMarker = globalfile.IntensityMarker
        pathinfo.saveflag = globalfile.LogFlag




        if (PacketSetting.ModeSelector == 0): ##### point cloud mode
            if (totalpacket < 16):

                lwIP_socket.sendall(PacketSetting)
                paysize = sizeof(lm_resultUDP)

                data = lwIP_socket.recv(paysize)
                #print(sys.getsizeof(data))

                if (sys.getsizeof(data) == 29753): ## 29753 for 2 peaks  and  59449 for 4 peaks
                    totalpacket = totalpacket + 1
                    payload_in = lm_resultUDP.from_buffer_copy(data)

                    packetnumber = payload_in.PacketCounter
                    if (packetnumber == packetwatch):

                        FrameData[packetwatch] = deepcopy(payload_in)
                        packetwatch = packetwatch + 1

                        #print(" packet watch is ",packetwatch )

                    else:
                        print("Frame skipped for packet mismatch")

                        packetfiller = 0
                        packetwatch = 0
                        totalpacket = 0

                else:
                    Skippedpackets = Skippedpackets + 1
                    #print(" Frame Skipped for ")

            else:

                framecounter = framecounter + 1
                totalpacket = 0
                packetwatch = 0

                globalfile.FrameIndex = FrameData[0].FrameCounter
                globalfile.DSPTemp = FrameData[0].DSPTemp
                FrameData[0].timestamp = globalfile.TimeStampBase
                FrameData[0].PacketCounter = globalfile.TimeStampMicro

                pathinfo.FrameCounter = c_int(FrameData[1].FrameCounter)

                #ret = Brid_convertstruct(FrameData, pathinfo, RangeDLL, DopplerDLL, IntensityDLL, RangeUpChirpDLL,RangeDownChirpDLL, IntensityUpChirpDLL, IntensityDownChirpDLL)

                #
                ret = Brid_convertstruct(FrameData, pathinfo, RangeDLL, DopplerDLL, IntensityDLL)
                #
                #
                temprange = deepcopy(RangeDLL.reshape((116, 256)))
                tempintensity = deepcopy(IntensityDLL.reshape((116, 256)))
                tempdoppler = deepcopy(DopplerDLL.reshape((116, 256)))
                #
                if (globalfile.FrameIndex % 2 == 0):



                    globalfile.rangeimage = np.fliplr(temprange[::-1])  ## flip it for left right scan
                    globalfile.intensityimage = np.fliplr(tempintensity[::-1])

                    globalfile.intensityimage[globalfile.intensityimage > 30] = 30
                    globalfile.intensityimage[0,0] = 32



                else:


                    globalfile.rangeimage =  np.fliplr(temprange)
                    globalfile.intensityimage = np.fliplr(tempintensity)
                    globalfile.dopplerimage = np.fliplr(tempdoppler)

                    globalfile.intensityimage[globalfile.intensityimage > 30] = 30
                    globalfile.intensityimage[0,0] = 32


                
                
                rangeimage3dinput = np.flip(temprange , 1)
                intensityimage3dinput = np.flip(tempintensity, 1)
                dopplerimage3dinput = np.flip(tempdoppler, 1)
                
                
                globalfile.data2D = (rangeimage3dinput, dopplerimage3dinput, intensityimage3dinput, globalfile.FrameIndex)
                progress_callback.emit(0.0)
                #print("progress_callback >> 3D Visualizer")


                endtime = time.time()
                print( "------------------------------------------Completed, Frame Time  %1.3f  with frame number %d  " % (endtime - starttime ,FrameData[1].FrameCounter ))
                #print(" frame counter ",FrameData[1].FrameCounter )
                starttime = time.time()

        else:

            lwIP_socket.sendall(PacketSetting)
            paysize = sizeof(RawData)
            data = lwIP_socket.recv(paysize)

            #print(sys.getsizeof(data))
            if (sys.getsizeof(data) == 32809):
                #print(sys.getsizeof(data))
                payload_in = RawData.from_buffer_copy(data)
                globalfile.DSPTemp = payload_in.DSPTemp
                framenumber = payload_in.FrameNumber

                for i in range(16384):
                    # pass
                    #### convert raw data to voltage
                    rawdata = payload_in.ChannelData[i]
                    channelA[i] = ConvertedVoltage(rawdata)

                window = np.hamming(16384)
                windowdata = np.multiply(channelA[0:16384], window)
                f_signal = fft(windowdata)
                logsn = 20 * np.log10(2 * np.abs(f_signal) / N)

                # globalfile.timedomain = logsn[0:4096].tolist()  ###testback for timedomain
                # globalfile.frebins = fbins[0:4096]
                #print(channelA[0:20])
                globalfile.timedomain = channelA[0:16384].tolist()  ###testback for timedomain
                globalfile.frebins = timeaxis[0:16384].tolist()

                globalfile.timedomainavg = logsn[0:8192].tolist()  ###testback for timedomain
                globalfile.frequencybins = frebins[0:8192].tolist()

                ### Log the time domain data

                if (PacketSetting.ModeSelector == 1):
                    adcfolder = "TimeDomain_ADC_" + str("%02d" % (PacketSetting.PrimaryADC))

                else:
                    adcfolder = "Spectrum_ADC_" + str("%02d" % (PacketSetting.PrimaryADC))

                adcpath = join(timeDomainPath, adcfolder)
                index = str("%06d" % (framenumber))
                timesavepath = join(adcpath, index)
                if not os.path.exists(adcpath):
                    os.makedirs(adcpath)

                np.save(timesavepath, channelA)

            else:
                pass
                ##-------print(" Waiting for trigger ")


def print_Acquire(s):
    print(s)


def Acquire_thread_complete():
    print("THREAD COMPLETE for Sending Voltage")



def ConvertedVoltage(rawData):

    volt = 0.0
    if (rawData >= 32768) :

        volt = ((rawData % 32768) * 0.5 / 32768) - 0.5;

    else:
        volt = rawData * 0.5 / 32768;


    return volt





