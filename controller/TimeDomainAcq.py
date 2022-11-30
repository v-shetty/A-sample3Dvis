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
class Connectionload(Structure):
    _fields_= [ ("ethernetBufferSize" , c_uint32),

                ("ipAddressString" , (c_char * 40)),
                ("ethernetPort" , (c_char * 6)),

                ("configurationFilePath" , (c_char * 255)),


 
    ]

class TimeLoad(Structure):
        _fields_= [ ("triggerCount" , c_uint16),

                ("triggerType" , c_uint8),
                ("triggerSource" , c_uint8),


                ("triggerTimestamp" , c_uint32),
                ("samples" , (c_int16 * 16400) ),
                ("sampleCount" , c_uint32),
                ("decimation" , c_uint32),


 
    ]   




class MatLoad(Structure):
    _fields_= [ ("ChirpManual" , c_uint32),

                ("TrigManual" , c_uint32),
                ("FFTTRig" , c_uint32),


                ("CurrentPixCount" , c_uint32),
                ("LastPixCount" , c_uint32),
                ("ERDATrig" , c_uint32),
                ("FFTEdge" , c_uint32),


 
    ]    

class PeakSearchLoad(Structure):
    _fields_= [ ("peakSearchWindowStart_m" , c_float),
                ("peakSearchWindowEnd_m" , c_float),
                ("peakHeightThreshold" , c_float),
                ("peakSpacingMinimum_m" , c_float),



    ]


class lmreturn(Enum):
        LM_SUCCESS 						= 0
        LM_FAILURE						= -1
        LM_CONNECTION_ERROR 			= -10
        LM_MODULE_UNAVAILABLE			= -11
        LM_MODULE_ALREADY_CONFIGURED 	= -20
        LM_INPUT_PARAM_INVALID			= -30
        LM_CONFIG_FILE_ERROR			= -40

class lmtrig(Enum):
        LM_TRIGGER_MULT_SHOT = 0
        LM_TRIGGER_CONTINUOUS = 1



class lmdata(Structure):
    _fields_= [ ("timestamp" , c_uint64),
                ("triggerCount" , c_uint32),
                ("range" , (c_float*16)),
                ("velocity" , (c_float*16)),

                ("upChirpPeakLocation" , (c_float*16)),
                ("upChirpPeakHeight" , (c_float*16)),
                ("downChirpPeakLocation" , (c_float*16)),
                ("downChirpPeakHeight" , (c_float*16)),

                ("status" , (c_uint32)),



    ]



class lmdataarray(Structure):
    _fields_= [ ("box" , lmdata * 16  ),
                

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

    BridDebuglid = cdll.LoadLibrary('./libBridgerPhotonics_LidarModule_DiagAPI.so')
    Bridlib = cdll.LoadLibrary('./libBridgerPhotonics_LidarModule_UserAPI.so')
    #os.getcwd() + '//Resources//ScantinelLogo.jpg'
    #Bridlib = cdll.LoadLibrary(os.getcwd() + '//libBridgerPhotonics_LidarModule_UserAPI.dll')
    print("Succesfully Loaded Library")
    conload = Connectionload()
    Peakload = PeakSearchLoad()

    conload.ethernetBufferSize =  1024*1024*128
    conload.ipAddressString = bytes("192.168.20.100", encoding='utf8')
    conload.ethernetPort = bytes("4194", encoding='utf8')



    conload.configurationFilePath = bytes("/home/scantinel/GUI/ConfigFiles", encoding='utf8')

    Peakload.peakSearchWindowStart_m = 1.0
    Peakload.peakSearchWindowEnd_m = 10.0
    Peakload.peakHeightThreshold = 1.79980
    Peakload.peakSpacingMinimum_m = 0.01

    Brid_init = Bridlib.lm_Init
    Brid_init.argtypes = [ctypes.POINTER(Connectionload), ctypes.POINTER(PeakSearchLoad)]
    Brid_init.restype = lmreturn
    resfloat = Brid_init( conload , Peakload)
    print("Succesfully Loaded Library")
    if(resfloat.name == "LM_SUCCESS"):
        print("Succesfully Loaded Library")

    #Flush the ethenet Bufer

    Brid_flushbuffer = Bridlib.lm_EthernetBufferFlush
    Brid_flushbuffer.argtypes = [ctypes.POINTER(Connectionload)]
    Brid_flushbuffer.restype = lmreturn

    resfloat = Brid_flushbuffer(conload)

    if(resfloat.name == "LM_SUCCESS"):
        print("Succesfully Flushed Buffer")  

    #Trigger enable

    Brid_pixdisable = Bridlib.lm_PixelTriggerDisable
    Brid_pixdisable.argtypes = [ctypes.POINTER(Connectionload)  ]
    Brid_pixdisable.restype = lmreturn

    resfloat = Brid_pixdisable(conload )



    if(resfloat.name == "LM_SUCCESS"):
        print("Succesfully enabled the Measurement") 

    #start the measurement




    Brid_start = BridDebuglid.lmdiag_DiagnosticsStart
    Brid_start.argtypes = [ctypes.POINTER(Connectionload) , c_uint32  , c_uint32 , c_uint32, c_uint32, c_uint32, c_uint32 , c_uint8, c_uint8, c_uint8 , c_uint8 ]
    Brid_start.restype = lmreturn

    NumCoulmn = 1

    resfloat = Brid_start(conload , 32 , 1, 19, 1, 0 ,  1 , 1, 0 ,  0 ,  0 )    #32*58=1856

# 1, 0 ,  0 ,  0    one
# 2, 0 ,  0 ,  0    two 
# 0, 1 ,  0 ,  0    five
# 0, 2 ,  0 ,  0    six
# 0,0,0,2       fourteen
#  0,0,0,8     sixteen
# 0,0,4,0     eleven
#
#
#
#


    if(resfloat.name == "LM_SUCCESS"):
        print("Succesfully Started the Debug Measurement")    


    loopconter = 0


    time.sleep(0.5)
 


    boxdata =(lmdata * 4000)() #58*16*2 here 2 is the padding, to be at safer side

    testboxdata =(lmdata * 4000)() #58*16*2 here 2 is the padding, to be at safer side


    framedata =(lmdata * 3712)() #58*16*2 here 2 is the padding, to be at safer side

    timedomaindata =(lmdata * 3712)() #58*16*2 here 2 is the padding, to be at safer side

    
    arrlm = (lmdata * 58*2)
    print("size of arra lam ", sizeof(arrlm))



    timedomain = (TimeLoad) ()

    Brid_getdata = BridDebuglid.lmdiag_DiagnosticsGet
    #array_type = ctypes. * num_numbers
    Brid_getdata.argtypes = [ctypes.POINTER(Connectionload) , ctypes.POINTER(TimeLoad) , c_uint16]
    Brid_getdata.restype = c_uint32

    ranger = np.zeros((116, 256))#58, 116



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
    homepath = str(os.getcwd() + '//resutlts//retro_140m')
    #homepath = r"/home/scantinel/GUI/resutlts/retro_56m"

    while 1:
        
        print('Client connection accepted Acquire Thread, Waiting for Trigger')
        resfloat = Brid_flushbuffer(conload)
        while 1:    

            #rawdata = (lmdata *16 )()  
            
            #print("-------------------------------- before sample count" , timedomain.sampleCount)
            numdata = Brid_getdata(conload ,timedomain  , 1)

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


                globalfile.timedomainavg  =  np.average(TimeDomainMatrix, axis=0).tolist()
                np.save('retro_56m.npy', globalfile.timedomainavg) 
                index = str(totalcount)
                savepath = join(homepath ,index)
                np.save(savepath ,testback)
                

                globalfile.timedomain = logsn[0:4096].tolist()###testback for timedomain
                globalfile.frebins = fbins[0:4096]

                lookuparray = globalfile.timedomainavg[globalfile.fremin:globalfile.fremax]
                globalfile.peakmax = np.max(lookuparray)

                if(globalfile.peakmax > globalfile.globalmaxpeak):
                    globalfile.globalmaxpeak = globalfile.peakmax 
                
                maxindex = np.argmax(lookuparray)

                globalfile.peakmaxdistance =  (fbins[maxindex] * co )/ (2* FTR)
                

                globalfile.adcmax = np.max(testback)
                globalfile.adcmin = np.min(testback)


                
                #print("Packets recived" ,numdata)

                print("----------------------------------Trigger count ", timedomain.triggerCount)
                print("--------------------------------Trigger Type" , timedomain.triggerType)
                print("--------------------------------Trigger source" , timedomain.triggerSource)

                #print("--------------------------------Decimation" , timedomain.decimation)
                print("--------------------------------sample count" , timedomain.sampleCount)

                print("Total count ", totalcount)

            else:
                print("waiting for data")
                if(restart):
                    print("Sent Trigger Aggain")
                    resfloat = Brid_start(conload , 32 , 1, 19, 1, 0 ,  0 , 2 , 0 ,  0 ,  0 )    #32*58=1856
                    restart = False


            time.sleep(0.2)


    print('Client connection closed for after Acquire Thread')
    #conn.close()





def print_Acquire( s):
    print(s)

def Acquire_thread_complete():
    print("THREAD COMPLETE for Sending Voltage")
    






 
 