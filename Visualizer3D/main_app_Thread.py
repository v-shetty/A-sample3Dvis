from Visualizer3D.model.model import Model
from Visualizer3D.controllers.main_controller import MainController
from Visualizer3D.gui.PCLVisualizer import PCLVisualizerWindow
from PyQt5.QtCore import *

import time
import traceback, sys


class WorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(float)

class App(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super().__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        # Add the callback to our kwargs
        self.kwargs['progress_callback'] = self.signals.progress

        self.model = Model()
        self.main_controller = MainController(self.model)
        self.main_view = PCLVisualizerWindow(self.model, self.main_controller)



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


def Run_visualization(progress_callback):

    while 1:
        if 1:
            print(f"hello {QThread.currentThread()}")
            time.sleep(0.001)
        else:
            print("Waiting for the Laser Command")
            time.sleep(1)

def Print_visualization(s):
    print(s)

def Exit_visualization():
    print("THREAD COMPLETE! for Laser")