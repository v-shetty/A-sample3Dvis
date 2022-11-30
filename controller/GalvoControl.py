import socket
from ctypes import *
import json
import numpy as np
from PyQt5.QtCore import *

import time
import traceback, sys
import model.GlobalFile as globalfile
import array as arr
from imageio import imread


import os

class GalvoLoad(Structure):
    _fields_ = [("Flag", c_uint32),
                ("VIC", c_float),
                ("VBC", c_float),
                ("Pix_Per_Frame", c_uint32),
                ("Trigger_Angle_Deg", c_float),
                ("Pause_After_Trigger_ms", c_uint32),
                ("Galvo_Mech_Deg_Per_V", c_float)
                ]

class WorkerSignals(QObject):

    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(float)


class GalvoControl(QRunnable):
    '''
    Worker thread
    '''

    def __init__(self, fn, *args, **kwargs):
        super(GalvoControl, self).__init__()

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





def Run_Galvo(progress_callback):

    HOST = '192.168.20.140'  # Standard loopback interface address (localhost)
    PORT = 2031  # Port to listen on (non-privileged ports are > 1023)
    print("Starting the server for Galvo Thread ")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(3)

    while 1:
        conn, addr = s.accept()
        print('Client connection accepted for Galvo thread ', addr)
        while 1:
            try:
                if(globalfile.GalvoFlag ):

                    print("Taken the Galvo Command")
                    payload_out = GalvoLoad(c_uint32(1), c_float(globalfile.Galvo.VIC), c_float(globalfile.Galvo.VBC), c_uint32(globalfile.Galvo.Pix_Per_Frame), c_float(globalfile.Galvo.Trigger_Angle_Deg), c_uint32(globalfile.Galvo.Pause_After_Trigger_ms),c_float(globalfile.Galvo.Galvo_Mech_Deg_Per_V) )
                    conn.sendall(payload_out)
                    time.sleep(1)
                    globalfile.GalvoFlag = False

                else:

                    print("Waiting for the Galvo Command")
                    time.sleep(1)


            except:
                print('Client connection closed for Galvo thread', addr)
                conn.close()
                break
    conn.close()





def Print_Galvo( s):
    print(s)

def Exit_Glavo():
    print("THREAD COMPLETE! for Galvo")




