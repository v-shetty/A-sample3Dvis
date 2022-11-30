# Created by VikasVasanth at 20/04/2022
# *Copyright (C)  - All Rights Reserved at Scantinel Photonics GmbH*

import numpy as np
from ctypes import *


class __Galvo__():
    def __init__(self):
        self.VIC = 0.0
        self.VBC = 0.0
        self.Pix_Per_Frame = 0
        self.Trigger_Angle_Deg = 0.0
        self.Pause_After_Trigger_ms = 0
        self.Galvo_Mech_Deg_Per_V = 0.0


Galvo = __Galvo__()


class NTCParameter():
    def __init__(self):
        self.NW = 0.0
        self.NE = 0.0
        self.SW = 0.0
        self.SE = 0.0
        self.Chip = 0.0
        self.Hotplate = 0.0


NTC = NTCParameter()
NTCData = [0, 0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, ]


class com_variable(Structure):
    _fields_ = [
        ("crc", c_ubyte, 8)
    ]


comvariable = com_variable()


class __PowerControl__():
    def __init__(self):
        self.PowerBoardFlag = False
        self.PowerBoardONFlag = False
        self.PowerBoardOFFFlag = False
        self.SDL_priority = False
        self.with_load = True
        self.temp_mon_result = 0
        self.COM_PORT_STATUS = 'NO CONNECTION'
        comvariable.sync = 0xaa
        comvariable.len = 0x15
        comvariable.crc = 0x00
        self.time_pause = 0  # pause to ramp up the voltages from 0 t0 respective voltages(-15v, 24V)
        self.test_SDL = False  # variable for enabling the sdl, can be removed when SDL is well tested
        self.state = 0
        self.EN_P3V = 0
        self.EN_N3V = 0
        self.EN_P5V = 0
        self.EN_P24V = 0
        self.EN_P15V = 0
        self.EN_N15V = 0
        self.EN_5V = 0
        self.EN_FANS = 0
        self.EN_DSP = 0
        self.EN_LASER = 0
        self.EN_SCAN_SYS = 0
        self.EN_34V = 0
        self.READ_EN_P3V = 0
        self.READ_EN_N3V = 0
        self.READ_EN_P5V = 0
        self.READ_EN_P24V = 0
        self.READ_EN_P15V = 0
        self.READ_EN_N15V = 0
        self.READ_EN_5V = 0
        self.READ_EN_FANS = 0
        self.READ_EN_DSP = 0
        self.READ_EN_LASER = 0
        self.READ_EN_SCAN_SYS = 0
        self.READ_EN_34V = 0
        self.FAULT_N3V = 0
        self.FAULT_24V = 0
        self.P3V_PGOOD = 0
        self.P5V_PGOOD = 0
        self.PFET_STATUS = 0
        self.port_C = [self.EN_P3V, self.EN_N3V, self.EN_P5V,
                       self.EN_P24V, self.EN_P15V,
                       self.EN_N15V, 0, 0]
        self.port_D = [self.EN_5V, self.EN_FANS, self.EN_DSP,
                       self.EN_LASER, self.EN_SCAN_SYS,
                       self.EN_34V, 0, 0]
        self.read_port_c = [self.READ_EN_P3V, self.READ_EN_N3V, self.READ_EN_P5V, self.READ_EN_P24V,
                            self.READ_EN_P15V, self.READ_EN_N15V]
        self.read_port_d = [self.READ_EN_5V, self.READ_EN_FANS,
                            self.READ_EN_DSP,
                            self.READ_EN_LASER, self.READ_EN_SCAN_SYS, self.READ_EN_34V]
        self.read_portab = [self.FAULT_N3V, self.FAULT_24V, 0, 0, 0, self.P3V_PGOOD, self.P5V_PGOOD, self.PFET_STATUS]
        self.vol_monitoring = [2, 2, self.port_D[5], self.port_C[0],
                               self.port_C[1],
                               self.port_C[4], self.port_C[5], self.port_C[2],
                               self.port_C[3], 2, 2, 2]
        self.Sending_data = [0xaa, 0x1D, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                             0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                             0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xc9]
        self.Receiving_data = [0xaa, 0x1D, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                               0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                               0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        self.Read_status = []
        # self.power_up_sequence = [9, 10, 8, 0, 3, 13, 4, 11, 2, 12]
        self.power_up_sequence = [0, 1, 9, 10, 8, 3, 13, 4, 11, 2, 12]
        # need to change according to the requirement at 7, 9
        self.voltage_monitoring = {"0": [10.8, 13.2], "1": [10.8, 13.2], "2": [0, 37.4],
                                   "3": [-3.3, -2.7], "4": [2.7, 3.3],
                                   "5": [-16.5, -13.5],
                                   "6": [13.5, 16.5],
                                   "7": [4.5, 5.5], "8": [21.6, 26.4],
                                   "9": [0, 3], "10": [0, 60], "11": [0, 60]}
        self.Temp_meta_info = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.temp_threshold = 80
        self.auto_shut_down = False
        self.PB_TEMP1 = 0
        self.PB_TEMP2 = 0


PowerBoard = __PowerControl__()


class __lsr_amp_pwr__():
    def __init__(self):
        self.flag = 0
        self.amplifier_power = ""
        self.amp_receive = b""
        # self.amp_linux_enable = "COM7"


amp_pwr_ = __lsr_amp_pwr__()


def initialize():
    global RangeImageIndex
    global DopplerImageIndex
    global IntensityImageIndex

    global RangeImage
    global DopplerImage
    global IntentsityImage

    global LaserFlag
    global LaserON
    global Start
    global LSRMan
    global ChirpSim
    global ENFFT
    global DEB_A
    global DEB_B
    global Raw_Acq
    global SelectDIO
    global PreChirpDelay
    global CurrentPixCount
    global LastPixCount
    global DoTrig
    global DelayRDATrig
    global PauseAftRDATrig
    global Tdd
    global Tdu
    global SelectChipSource
    global ChirpManual
    global FFTEdge

    global AcquireThread

    global TempSource
    global amplifier_power
    global flag
    global amp_receive
    global voa_control
    voa_control = 10
    TempSource = 0

    RangeImageIndex = 0
    DopplerImageIndex = 0
    IntensityImageIndex = 0
    RangeImage = np.random.randint(256, size=(256, 116))
    DopplerImage = np.random.randint(256, size=(256, 70))
    IntentsityImage = np.random.randint(256, size=(256, 70))

    LaserFlag = False
    LaserON = 0
    Start = 0
    LSRMan = 0
    ChirpSim = 0
    ENFFT = 0
    DEB_A = 0
    DEB_B = 0
    Raw_Acq = 0
    SelectDIO = 0
    PreChirpDelay = 40
    CurrentPixCount = 0
    LastPixCount = 0
    DoTrig = 0
    DelayRDATrig = 20
    PauseAftRDATrig = 2000
    Tdd = 10
    Tdu = 10
    SelectChipSource = 0
    ChirpManual = 0
    FFTEdge = 0
    amplifier_power = ""
    amp_receive = ""
    flag = 0

    global rangeimage
    global rangeimageup
    global rangeimagedown

    global dopplerimage

    global intensityimage
    global intensityimageup
    global intensityimagedown

    global rangeimagepixel
    global intensityimagepixel

    rangeimagepixel = np.zeros((256, 256))
    intensityimagepixel = np.zeros((256, 256))

    rangeimage = np.zeros((116, 256))
    rangeimageup = np.zeros((116, 256))
    rangeimagedown = np.zeros((116, 256))

    dopplerimage = np.zeros((116, 256))

    intensityimage = np.zeros((116, 256))
    intensityimageup = np.zeros((116, 256))
    intensityimagedown = np.zeros((116, 256))

    global FrameIndex
    FrameIndex = 0

    global TimeStampBase
    TimeStampBase = 0

    global laser_temp
    laser_temp = 0

    global laser_current
    laser_current = 0

    global TimeStampMicro
    TimeStampMicro = 0

    AcquireThread = False

    global startlog
    startlog = False

    global sbriostart
    sbriostart = False

    global timedomain

    timedomain = np.zeros((16384,), dtype=float).tolist()

    global timedomainavg

    timedomainavg = np.zeros((8192,), dtype=float).tolist()

    global frebins

    frebins = np.arange(16384).tolist()

    global frequencybins

    frequencybins = np.arange(8192).tolist()

    global peakmax
    peakmax = 0

    global peakmaxdistance
    peakmaxdistance = 0

    global adcmax
    adcmax = 0

    global adcmin
    adcmin = 0

    global fremin
    fremin = int(114)

    global fremax
    fremax = int(4000)

    global globalmaxpeak
    globalmaxpeak = 0

    global udpsend
    udpsend = False

    global socket_udp

    # host = "192.168.20.165"
    # port = 2889

    # socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # socket_udp.bind((host, port))

    global savepath
    savepath = ""

    global BRAMfilePath
    BRAMfilePath = ""

    global offlineIndex
    offlineIndex = 0

    ###### ---------------------------------------------      DSP Configuration
    global DSPMode
    global FFTMode
    global PeakSpace
    global CFARCoeff
    global CFAROffset
    global ADCCH1
    global ADCCH2

    global ADCreset
    global ADCscale
    global ConstThresh

    global rangemin
    global rangemax

    global dopplermin
    global dopplermax

    global intensitymin
    global intensitymax

    rangemin = 4
    rangemax = 18

    dopplermin = -20
    dopplermax = 20

    intensitymin = 0
    intensitymax = 200

    DSPMode = 0
    FFTMode = 0
    PeakSpace = 5
    CFARCoeff = 52000
    CFAROffset = 30
    ADCCH1 = 0  # Time domain data for this channel. Indexing starting from 0 till 15
    ADCCH2 = 1

    global FS
    global FFTLength
    global FTR
    global FreqRes
    global c0

    global detectionmode

    ### peack detection algorithm
    ### 0 --- constant threshold
    ### 1 --- CFAR algo
    detectionmode = 0 ##default constant threshold

    c0 = 3e8
    FS = 500e6
    FFTLength = 16384
    FreqRes = FS / FFTLength
    FTR = 1

    global RangeMinBin
    global RangeMaxBin
    global PeakSpaceBin

    RangeMinBin = int(rangemin * (2 * FTR * 1e14) / (FreqRes * c0))
    RangeMaxBin = int(rangemax * (2 * FTR * 1e14) / (FreqRes * c0))
    PeakSpaceBin = int(PeakSpace * (2 * FTR * 1e14) / (FreqRes * c0))

    global packetIni
    global data2D
    data2D = tuple()
    packetIni = False


    global DSPTemp
    DSPTemp = 0;

    global RangeMarker
    global IntensityMarker
    global LogFlag
    RangeMarker = 0
    IntensityMarker = 0
    LogFlag = 0
