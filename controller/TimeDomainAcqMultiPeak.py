from ctypes  import *
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
from os.path import join
from scipy.fftpack import fft, rfft, fftfreq
LMDIAG_TIMEDOMAIN_SAMPLE_COUNT_MAX = (16 * 1024) + 16



class lmdiag_timeDomain(Structure):
        _fields_= [ ("triggerCount" , c_uint16),
                ("triggerType" , c_uint8),
                ("triggerSource" , c_uint8),
                ("triggerTimestamp" , c_uint32),
                ("samples" , (c_int16 * 16400)),
                ("sampleCount" , c_uint32),
                ("decimation" , c_uint32),
    ]   









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
                ("triggerCount", c_uint32),
                ("range", (c_float * 16)),
                ("velocity", (c_float * 16)),
                ("upChirpPeakLocation", (c_float * 4) * 16),
                ("upChirpPeakHeight", (c_float * 4) * 16),
                ("downChirpPeakLocation", (c_float * 4) * 16),
                ("downChirpPeakHeight", (c_float * 4) * 16),

                ]


class lm(Structure):
    _fields_ = [("ethernetBufferSize", c_uint32),
                ("ipAddressString", (c_char * 40)),
                ("ethernetPort", (c_char * 6)),
                ("configurationFilePath", (c_char * 255)),
                ("configFftSize", c_uint32)

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
    cwd = os.getcwd()


    configpath = os.path.join(cwd , "ConfigFiles")
    print(configpath)

    BridDebuglid = cdll.LoadLibrary('./libBridgerPhotonics_LidarModule_DiagAPI.dll')
    EngineLib = cdll.LoadLibrary('./libBridgerPhotonics_LidarModule_UserAPI.dll')
    #os.getcwd() + '//Resources//ScantinelLogo.jpg'
    #Bridlib = cdll.LoadLibrary(os.getcwd() + '//libBridgerPhotonics_LidarModule_UserAPI.dll')
    print("Succesfully Loaded Library")
    EngineCon = lm()
    PeakSearch = lm_peakSearch()

    EngineCon.ethernetBufferSize =  1024*1024*128
    EngineCon.ipAddressString = bytes("192.168.20.100", encoding='utf8')
    EngineCon.ethernetPort = bytes("4194", encoding='utf8')
    EngineCon.configurationFilePath = bytes("D:\PycharmProjects\MutlipPeak\MultiPeak\ConfigFiles", encoding='utf8')
    EngineCon.configFftSize = c_uint32(1)

    PeakSearch.peakSearchWindowStart_m = c_float(4.0)
    PeakSearch.peakSearchWindowEnd_m = c_float(80.0)
    PeakSearch.peakHeightThreshold = c_float(1.7)
    PeakSearch.peakSpacingMinimum_m = c_float(0.01)

    ##Engine Init
    Engine_Init = EngineLib.lm_Init
    Engine_Init.argtypes = [ctypes.POINTER(lm), ctypes.POINTER(lm_peakSearch)]
    Engine_Init.restype = lm_return

    FunReturn = Engine_Init( EngineCon , PeakSearch)

    if(FunReturn.name == "LM_SUCCESS"):
        print("Succesfully Loaded Library")
    else:
        print("ERROR --------------------Not possible to load Library", int(FunReturn.value), FunReturn.name)
        return 0

    #Flush the ethenet Bufer

    Engine_FlushBuffer = EngineLib.lm_EthernetBufferFlush
    Engine_FlushBuffer.argtypes = [ctypes.POINTER(lm)]
    Engine_FlushBuffer.restype = lm_return

    FunReturn = Engine_FlushBuffer( EngineCon )

    if(FunReturn.name == "LM_SUCCESS"):
        print("Succesfully Flushed Buffer")
    else:
        print("ERROR --------------------Not possible to Flush the Buffer", FunReturn.value, FunReturn.name)
        return 0



    #Trigger enable

    Engine_TriggerDisable = EngineLib.lm_PixelTriggerEnable
    Engine_TriggerDisable.argtypes = [ctypes.POINTER(lm)]
    Engine_TriggerDisable.restype = lm_return

    FunReturn = Engine_TriggerDisable(EngineCon )

    if(FunReturn.name == "LM_SUCCESS"):
        print("Succesfully Activated Pixel Trigger")
    else:
        print("ERROR --------------------Not possible to activate the Pixel Trigger", FunReturn.value, FunReturn.name)
        return 0




    #start the measurement


    Brid_start = BridDebuglid.lmdiag_DiagnosticsStart
    Brid_start.argtypes = [ctypes.POINTER(lm) , c_uint32  , c_uint32 , c_uint32, c_uint32, c_uint32, c_uint32 , c_uint8, c_uint8, c_uint8 , c_uint8 ]
    Brid_start.restype = lm_return

    NumCoulmn = 1

    resfloat = Brid_start(EngineCon , 32 , 1, 19, 1, 0 ,  0 , 15, 15,  15 ,  15 )    #32*58=1856

# 1, 0 ,  0 ,  0    one
# 2, 0 ,  0 ,  0    one and two              #############
# 0, 1 ,  0 ,  0    five
# 0, 2 ,  0 ,  0    six
# 0,0,0,2       fourteen
#  0,0,0,8     sixteen
# 0,0,5,0     nine and twelve
# 0, 0 , 0 , 8  sixteenm
# 1 ,2,4,8
#
#
#


    if(resfloat.name == "LM_SUCCESS"):
        print("Succesfully Started the Debug Measurement")    




    time.sleep(0.5)




    timedomain = (lmdiag_timeDomain) ()

    Brid_getdata = BridDebuglid.lmdiag_DiagnosticsGet
    #array_type = ctypes. * num_numbers
    Brid_getdata.argtypes = [ctypes.POINTER(lm) , ctypes.POINTER(lmdiag_timeDomain) , c_uint16]
    Brid_getdata.restype = c_uint32





    totalcount = 0

    testback = np.random.randint(20, size=8192)

    Fs = 500e6
    N = 8192

    fbins = np.arange(0, N)*Fs/N

    #W = fftfreq(y.size, d=x[1]-x[0])
    restart = False

    TimeDomainMatrix = np.full((16, 4096), 0)
    id = 0

    co = 3e8
    FTR = 1e14
    homepath = str(os.getcwd() + '//resutlts//Calibration//Images')
    #homepath = r"/home/scantinel/GUI/resutlts/retro_56m"

    while 1:
        
        print('Client connection accepted Acquire Thread, Waiting for Trigger')

        while 1:    

            #rawdata = (lmdata *16 )()  
            
            #print("-------------------------------- before sample count" , timedomain.sampleCount)
            numdata = Brid_getdata(EngineCon ,timedomain  , 1)
            #time.sleep(0.2)

            if(numdata>0):
                restart = True
                totalcount = totalcount + numdata


                for i in range(8192):
                    #pass
                    testback[i]= timedomain.samples[i]

                #apply FFT


                # DFT
                #X = np.fft.fft(x)
                #X_db = 20*np.log10(2*np.abs(X)/N)
                #f = np.fft.fftfreq(N, 1/Fs)
                #f = np.arange(0, N)*Fs/N
                window = np.hamming(8192)
                windowdata = np.multiply(testback, window)
                f_signal = fft(windowdata)
                logsn = 20*np.log10(2*np.abs(f_signal)/N)
                #logsn = 10*np.log10(abs(f_signal))

                if(totalcount % 15 == 0):
                    id = 0
                else :
                    id = id + 1

                TimeDomainMatrix[id][:] = logsn[0:4096]


                #print("----------------------------------Trigger count ", timedomain.triggerCount)
                #print("--------------------------------Trigger Type" , timedomain.triggerType)
                #print("--------------------------------Trigger source" , timedomain.triggerSource)

                #print("--------------------------------Decimation" , timedomain.decimation)
                #print("--------------------------------sample count" , timedomain.sampleCount)


                globalfile.timedomainavg  =  np.average(TimeDomainMatrix, axis=0).tolist()
                #np.save('retro_56m.npy', globalfile.timedomainavg)
                index = str("%06d" %(totalcount))
                adcfolder = "ADC_"+str("%02d"%(timedomain.triggerSource + 1))
                adcpath = join(homepath , adcfolder)
                print("store path --------------------------------------------------------", adcpath , timedomain.triggerCount , adcfolder)
                savepath = join(adcpath ,index)

                if not os.path.exists(adcpath):
                    os.makedirs(adcpath)
                np.save(savepath ,testback)
                

                globalfile.timedomain = logsn[0:4096].tolist()###testback for timedomain
                globalfile.frebins = fbins[0:4096]

                lookuparray = globalfile.timedomainavg[globalfile.fremin:globalfile.fremax]
                globalfile.peakmax = np.max(lookuparray)

                if(globalfile.peakmax > globalfile.globalmaxpeak):
                    globalfile.globalmaxpeak = globalfile.peakmax 


                maxindex = np.argmax(lookuparray) + globalfile.fremin
                #np.argmax(lookuparray)
                print("----max index is at--- ",maxindex )

                globalfile.peakmaxdistance =  (fbins[maxindex] * co )/ (2* FTR)
                

                globalfile.adcmax = np.max(testback)
                globalfile.adcmin = np.min(testback)


                
                #print("Packets recived" ,numdata)



                print("Total count ", totalcount)

            else:
                #print("waiting for data")
                if(restart):
                    print("Sent Trigger Aggain")
                    resfloat = Brid_start(EngineCon , 32 , 1, 19, 1, 0 ,  0 , 15, 15,  15 ,  15 )    #32*58=1856
                    restart = False


            #time.sleep(0.3)


    print('Client connection closed for after Acquire Thread')
    #conn.close()





def print_Acquire( s):
    print(s)

def Acquire_thread_complete():
    print("THREAD COMPLETE for Sending Voltage")
    






 
 