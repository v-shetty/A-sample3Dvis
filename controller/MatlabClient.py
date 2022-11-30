import socket
from ctypes import *
from PyQt5.QtCore import *
import time
import traceback, sys
import model.GlobalFile as globalfile



class MatLoad(Structure):
    _fields_ = [("ChirpManual", c_uint32),
                ("TrigManual", c_uint32),
                ("FFTTRig", c_uint32),
                ("CurrentPixCount", c_uint32),
                ("LastPixCount", c_uint32),
                ("ERDATrig", c_uint32),
                ("FFTEdge", c_uint32)


                ]







class WorkerSignals(QObject):

    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(float)


class MatThread(QRunnable):

    def __init__(self, fn, *args, **kwargs):
        super(MatThread, self).__init__()

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





def MatThreadRun(progress_callback ):

    HOST = '192.168.20.190'  # Standard loopback interface address (localhost)
    PORT = 2515  # Port to listen on (non-privileged ports are > 1023)
    print("Starting the Client ")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_addr = (HOST, PORT)
    s.connect(server_addr)
    print('Client connection accepted for MAT Thread Listener ')
    FFTENB = 0
    FFTEdge = 0
    while True:

       
            

        
        if globalfile.ENFFT == 2 :
            FFTENB = 1
        else:
            FFTENB = 0

        if globalfile.FFTEdge == 2 :
            FFTEdge = 1
        else:
            FFTEdge = 0

        payload_out = MatLoad(c_uint32(1), c_uint32(1), c_uint32(FFTENB),c_uint32(1), c_uint32(1),c_uint32(1),c_uint32(FFTEdge))
        s.sendall(payload_out)


        paysize = sizeof(MatLoad)
        data = s.recv(paysize)
        payload_in = MatLoad.from_buffer_copy(data)

        print("chirp is %d", payload_in.ChirpManual)



        time.sleep(0.5)



            


    #s.close()





def print_mat( s):
    print(s)

def mat_thread_complete():
    print("THREAD COMPLETE for Mat Reciever")
