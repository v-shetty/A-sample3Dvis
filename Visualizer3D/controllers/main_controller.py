import glob
import os

from PyQt5.QtCore import QObject, QThreadPool
from Visualizer3D.controllers.binReaders.carla_bin_reader import CarlaBinReader as carlaReader
from Visualizer3D.controllers.binReaders.bin_reader import BinReader as binReader

import Visualizer3D.controllers.services.calc as calc
import Visualizer3D.controllers.services.filter as filter

import numpy as np
import re

def relpath(path):
    return os.path.join(os.path.dirname(__file__), path)

azimuthal_mat_deg_lr = np.load(relpath(r"data/azimuthal_mat_lr.npy"))
azimuthal_mat_deg_rl = np.load(relpath(r"data/azimuthal_mat_deg_rl.npy"))
elev_vec_deg = np.load(relpath(r"data/elev_vec_deg.npy"))

class MainController(QObject):
    def __init__(self, model):
        super().__init__()
        self.threadpool = QThreadPool()
        self._model = model

    def packet_data_extraction_bin(self, data):
            if (data[3] % 2) == 0:
                self.processData(azimuthal_mat_deg_lr, elev_vec_deg, np.fliplr(data[0].T), np.fliplr(data[1].T),
                                 np.fliplr(data[2].T))
            elif (data[3] %2) != 0:
                self.processData(azimuthal_mat_deg_rl, elev_vec_deg, np.fliplr(data[0].T), np.fliplr(data[1].T),
                                 np.fliplr(data[2].T))
            # self.processData(azimuthal_mat_deg_lr, elev_vec_deg, np.fliplr(data[0].T), np.fliplr(data[1].T),
            #                  np.fliplr(data[2].T))

    def bin_data_extraction_binFiles(self, path):
        reader = binReader(path)
        file_name_ = os.path.basename(path)
        file_name = os.path.splitext(file_name_)
        self._model._fileName = file_name[0]
        return reader.bin_data_extraction_binFiles()

    def bin_data_extraction_carlaFiles(self, path):
        reader = carlaReader(path)
        file_name_ = os.path.basename(path)
        file_name = os.path.splitext(file_name_)
        self._model._fileName = file_name[0]
        return reader.bin_data_extraction_carlaFiles()

    def processData(self, azimuthal_matrix, elevation_matrix, distance, velocity, intensity):
        [dataSet, colorSet] = calc.conversion_2D_3D_PC(azimuthal_matrix, elevation_matrix, distance, velocity, intensity)
        [dataSet, colorSet] = self.applyFilters(dataSet, colorSet)

        self._model.dataSet = dataSet
        self._model.colorSet = colorSet

    def applyFilters(self, dataSet, colorSet):
        filtersListStr = self._model._filtersListStr

        if self._model._postProcessingBool:
            self._model._cntBefore = list(dataSet.values())[0].shape
            if self._model._chosenFilterBool:
                if self._model._chosenFilter == self._model.filters[0]:
                    [dataSet, colorSet] = filter.boundBoxFilter(self._model._filterBdBoxMin,
                                                                self._model._filterBdBoxMax,
                                                                dataSet, colorSet)

                elif self._model._chosenFilter == self._model.filters[1]:
                    [dataSet, colorSet] = filter.velocityFilter(self._model._filterVelocityMin,
                                                                 self._model._filterVelocityMax,
                                                                 dataSet, colorSet)

                elif self._model._chosenFilter == self._model.filters[2]:
                    [dataSet, colorSet] = filter.intensityFilter(self._model._filterIntensityMin,
                                                                 self._model._filterIntensityMax,
                                                                 dataSet, colorSet)
            elif not self._model._chosenFilterBool:
                if self._model._filtersListStr:
                    for filterStr in filtersListStr:
                        if self._model.filters[0] in filterStr:
                            vals = re.findall(r"[-+]?(?:\d*\.\d+|\d+)", filterStr)
                            vals = [float(i) for i in vals]
                            self._model._filterBdBoxMax = vals[0:3]
                            self._model._filterBdBoxMax = vals[3:]
                            [dataSet, colorSet] = filter.boundBoxFilter(self._model._filterBdBoxMin,
                                                                        self._model._filterBdBoxMax,
                                                                        dataSet, colorSet)

                        elif self._model.filters[1] in filterStr:
                            vals = re.findall(r"[-+]?(?:\d*\.\d+|\d+)", filterStr)
                            vals = [float(i) for i in vals]
                            self._model._filterVelocityMin = vals[0]
                            self._model._filterVelocityMax = vals[1]
                            [dataSet, colorSet] = filter.velocityFilter(self._model._filterVelocityMin,
                                                                        self._model._filterVelocityMax,
                                                                        dataSet, colorSet)
                        elif self._model.filters[2] in filterStr:
                            vals = re.findall(r"[-+]?(?:\d*\.\d+|\d+)", filterStr)
                            vals = [float(i) for i in vals]
                            self._model._filterIntensityMin = vals[0]
                            self._model._filterIntensityMax = vals[1]
                            [dataSet, colorSet] = filter.intensityFilter(self._model._filterIntensityMin,
                                                                         self._model._filterIntensityMax,
                                                                         dataSet, colorSet)
                else:
                    pass

            self._model._cntAfter = list(dataSet.values())[0].shape

        return [dataSet, colorSet]

    def readFileSeq(self, filePath):
        return glob.glob(filePath + "./*.bin")

    def calcColormap(self, min_v, max_v, point_data, cm):
        return calc.getColormap(min_v, max_v, point_data, cm)
