# Created by VikasVasanth at 21/04/2022
# *Copyright (C)  - All Rights Reserved at Scantinel Photonics GmbH*

import socket
import time
import traceback, sys
from PyQt5.QtCore import *
import model.GlobalFile as globalfile

Sending_data = [0xaa, 0x15, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]


class WorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(float)


class PowerControl(QRunnable):
    """
    Worker thread
    """

    def __init__(self, fn, *args, **kwargs):
        super(PowerControl, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        # Add the callback to our kwargs
        self.kwargs['progress_callback'] = self.signals.progress

    def run(self):
        """
        Initialise the runner function with passed args, kwargs.
        """

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


def RecvPowerBoardThread(progress_callback):
    HOST = '192.168.20.190'  # Standard loopback interface address (localhost)
    PORT = 2071  # Port to listen on (non-privileged ports are > 1023)
    print("Starting the server for Power Thread ")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_addr = (HOST, PORT)
    s.connect(server_addr)
    print('Client connection accepted for Power thread ')
    while True:
        if True:
            globalfile.PowerBoard.Sending_data[5] = 0
            globalfile.PowerBoard.Sending_data[6] = 0
            globalfile.PowerBoard.Sending_data[-1] = 0
            if globalfile.NTCData[0] <= globalfile.PowerBoard.temp_threshold and \
                    globalfile.NTCData[3] <= globalfile.PowerBoard.temp_threshold and \
                    globalfile.NTCData[7] <= globalfile.PowerBoard.temp_threshold and \
                    globalfile.NTCData[8] <= globalfile.PowerBoard.temp_threshold:
                if globalfile.PowerBoard.PowerBoardFlag and not globalfile.PowerBoard.SDL_priority:
                    # print('Temp ok ')
                    for i in range(8):
                        if globalfile.PowerBoard.port_C[i] == 2:
                            globalfile.PowerBoard.Sending_data[5] += 1 << i
                    for j in range(8):
                        if globalfile.PowerBoard.port_D[j] == 2:
                            globalfile.PowerBoard.Sending_data[6] += 1 << j
                    # print('total......', globalfile.PowerBoard.Sending_data[6])
                    globalfile.comvariable.crc = sum(globalfile.PowerBoard.Sending_data[:-1])
                    globalfile.PowerBoard.Sending_data[-1] = globalfile.comvariable.crc
                    data = s.send(bytearray(globalfile.PowerBoard.Sending_data))
                    b = s.recv(len(globalfile.PowerBoard.Sending_data))
                    globalfile.PowerBoard.Receiving_data = list(b)
                    globalfile.PowerBoard.time_pause += 1
                    arrange()
                    progress_callback.emit(globalfile.PowerBoard.Receiving_data[4])
                elif globalfile.PowerBoard.SDL_priority:
                    globalfile.comvariable.crc = sum(globalfile.PowerBoard.Sending_data[:-1])
                    globalfile.PowerBoard.Sending_data[-1] = globalfile.comvariable.crc
                    data = s.send(bytearray(globalfile.PowerBoard.Sending_data))
                    # print(globalfile.PowerBoard.Sending_data)
                    globalfile.PowerBoard.Receiving_data = list(s.recv(len(globalfile.PowerBoard.Sending_data)))
                    globalfile.PowerBoard.SDL_priority = False
                    globalfile.PowerBoard.PowerBoardFlag = True
                    arrange()
                    progress_callback.emit(globalfile.PowerBoard.Receiving_data[4])
                    print('All voltage are force shut down')
            # auto shutdown
            else:
                if globalfile.PowerBoard.PowerBoardFlag and not globalfile.PowerBoard.SDL_priority:
                    globalfile.PowerBoard.auto_shut_down = True
                    for i in range(8):
                        if globalfile.PowerBoard.port_C[i] == 2:
                            globalfile.PowerBoard.Sending_data[5] += 1 << i
                    for j in range(8):
                        if j == 5:
                            pass
                            globalfile.PowerBoard.port_D[5] = 0
                        elif globalfile.PowerBoard.port_D[j] == 2:
                            globalfile.PowerBoard.Sending_data[6] += 1 << j
                    # print('total', globalfile.PowerBoard.Sending_data[6] )
                    globalfile.comvariable.crc = sum(globalfile.PowerBoard.Sending_data[:-1])
                    globalfile.PowerBoard.Sending_data[-1] = globalfile.comvariable.crc
                    data = s.send(bytearray(globalfile.PowerBoard.Sending_data))
                    b = s.recv(len(globalfile.PowerBoard.Sending_data))
                    globalfile.PowerBoard.Receiving_data = list(b)
                    globalfile.PowerBoard.time_pause += 1
                    arrange()
                    progress_callback.emit(globalfile.PowerBoard.Receiving_data[4])

        else:
            print("Waiting for the Power Board Command")
            time.sleep(1)


def arrange():
    globalfile.PowerBoard.Read_status = []
    store = []
    for i in range(7, 31):
        store.append(hex(globalfile.PowerBoard.Receiving_data[i]))
        if i % 2 == 0:
            data = str(store[1][2:]) + str(store[0][2:])
            globalfile.PowerBoard.Read_status.append(data)
            store.clear()
    # print("Read status...", globalfile.PowerBoard.Read_status)


def Print_PowerBoard(s):
    print(s)


def Exit_PowerBoard():
    print("THREAD COMPLETE! for Power Board")
