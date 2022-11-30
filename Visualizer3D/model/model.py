from PyQt5.QtCore import QObject, pyqtSignal
import numpy as np


class Model(QObject):
    packet_read = pyqtSignal(tuple)
    folderPath_read = pyqtSignal(str)

    pcd_read = pyqtSignal(np.ndarray)

    dataSet_read = pyqtSignal(dict)
    colorSet_read = pyqtSignal(dict)
    dataChoice_read = pyqtSignal(str)
    colorPtsChoice_read = pyqtSignal(str)

    fileTypes = ['bin']
    colormaps = ['CET-C6', 'CET-CBTL1', 'CET-D1A', 'CET-L1', 'CET-L3', 'CET-R4', 'PAL-relaxed_bright']
    gridMarkersFontSizes = [8, 12, 14]
    filters = ['Bounding Box','Velocity','Intensity']

    checkDataList = ['xyz']
    checkColorList = ['range','velocity','intensity']

    def __init__(self):
        super().__init__()

        # Main properties
        self._packet = None
        self._folderPath = None
        self._filePath = None
        self._fileName = None

        self._dataSet = None
        self._colorSet = None

        self._dataChoice = None
        self._colorPtsChoice = None

        # offline variables
        self._offlineBool = False
        self._filesList = None

        # receiving data check variables
        self._dataReceived = False
        self._colorReceived = False

        # frames variables
        self._currentFrame = 0
        self._firstFrame = 0
        self._lastFrame = float("inf")
        self._stepFrame = 0
        self._playSpeed = 0
        self._autoRunBool = False

        # post-processing
        self._postProcessingBool = None
        self._chosenFilterBool = None
        self._cntBefore = None
        self._cntAfter = None
        self._chosenFilter = None
        self._filtersListStr = None

        # Bounding Box Filter
        self._filterBdBoxMin = None
        self._filterBdBoxMax = None

        # Intensity Filter
        self._filterIntensityMin = None
        self._filterIntensityMax = None

        # Velocity Filter
        self._filterVelocityMin = None
        self._filterVelocityMax = None

    @property
    def packet(self):
        return self._packet

    @packet.setter
    def packet(self, value):
        self._packet = value
        self.packet_read.emit(value)

    @property
    def dataChoice(self):
        return self._dataChoice

    @dataChoice.setter
    def dataChoice(self, value):
        self._dataChoice = value
        self.dataChoice_read.emit(value)

    @property
    def colorPtsChoice(self):
        return self._colorPtsChoice

    @colorPtsChoice.setter
    def colorPtsChoice(self, value):
        self._colorPtsChoice = value
        self.colorPtsChoice_read.emit(value)

    @property
    def colorSet(self):
        return self._colorSet

    @colorSet.setter
    def colorSet(self, value):
        self._colorSet = value
        self.colorSet_read.emit(value)

    @property
    def dataSet(self):
        return self._dataSet

    @dataSet.setter
    def dataSet(self, value):
        self._dataSet = value
        self.dataSet_read.emit(value)

    @property
    def folderPath(self):
        return self._file

    @folderPath.setter
    def folderPath(self, value):
        self._folderPath = value
        self.folderPath_read.emit(value)

    @property
    def pcd(self):
        return self._pcd

    @ pcd.setter
    def pcd(self, value):
        self._pcd = value
        self.pcd_read.emit(value)


