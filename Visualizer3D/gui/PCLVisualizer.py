import datetime
import os
import re
import time

import numpy as np
import pyqtgraph
from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtWidgets import QWidget, QFileDialog
from PyQt5.QtCore import pyqtSlot

import Visualizer3D.gui.resources.resources

import pyqtgraph.opengl as gl
import pyqtgraph as pg
import model.GlobalFile as globalfile
def relpath(path):
    return os.path.join(os.path.dirname(__file__), path)
defaultColorMap = 'CET-R4'


class PCLVisualizerWindow(QtWidgets.QWidget):
    def __init__(self, model, main_controller):
        super().__init__()

        self._model = model
        self._main_controller = main_controller

        # loading the ui file
        self._ui = uic.loadUi(relpath('PCLVisualizer.ui'), self)

        # listen to model signals
        self.listenToModelSignals()

        # widgets initialization
        self.initializeWidgets()

        # widgets Bindings
        self.widgetsBinding()



    ######## online Listeners/Slots ########
    @QtCore.pyqtSlot()
    def newDataArrive(self):
        self._model.packet = globalfile.data2D
    ########################################

    ######## Model Signal/Slots ########
    def listenToModelSignals(self):
        self._model.packet_read.connect(self.on_packet_read)
        self._model.folderPath_read.connect(self.on_folderPath_read)
        self._model.pcd_read.connect(self.on_pcd_read)
        self._model.dataSet_read.connect(self.on_dataSet_read)
        self._model.colorSet_read.connect(self.on_colorSet_read)
        self._model.dataChoice_read.connect(self.on_dataChoice_read)
        self._model.colorPtsChoice_read.connect(self.on_colorPtsChoice_read)
    def widgetsBinding(self):
        # file reading
        # self._ui.loadCloudFolderMenu_btn.clicked.connect(self.on_loadCloudFolderMenu_btn_clicked) # called automatically
        self._ui.vwOptData_comboBox.currentIndexChanged.connect(self.on_vwOptData_comboBox_IndexChanged)
        self._ui.vwOptColorPts_comboBox.currentIndexChanged.connect(self.on_vwOptColorPts_comboBox_IndexChanged)

        # colormap
        self._ui.vwOptColormap_comboBox.currentIndexChanged.connect(self.on_vwOptColormap_comboBox_IndexChanged)
        self._ui.vwOptColormapMax_edit.textChanged.connect(self.vwOptColormapMax_lineEdit_onStateChanged)
        self._ui.vwOptColormapMin_edit.textChanged.connect(self.vwOptColormapMin_lineEdit_onStateChanged)
        # self._ui.vwOptColormapMin_btn.clicked.connect(self.on_vwOptColormapMin_btn_clicked) # called automatically
        # self._ui.vwOptColormapMas_btn.clicked.connect(self.on_vwOptColormapMax_btn_clicked) # called automatically

        # Axes
        self._ui.vwOptAxes_checkBox.stateChanged.connect(self.vwOptAxes_checkBox_onStateChanged)

        # Grid
        self._ui.vwOptGrid_checkBox.stateChanged.connect(self.vwOptGrid_checkBox_onStateChanged)
        self._ui.vwOptGridXSize_edit.textChanged.connect(self.vwOptGridXSize_lineEdit_onStateChanged)
        self._ui.vwOptGridYSize_edit.textChanged.connect(self.vwOptGridYSize_lineEdit_onStateChanged)
        self._ui.vwOptGridSpacing_edit.textChanged.connect(self.vwOptGridSpacing_lineEdit_onStateChanged)
        self._ui.vwOptGridXSize_slider.valueChanged.connect(self.vwOptGridXSize_slider_onStateChanged)
        self._ui.vwOptGridYSize_slider.valueChanged.connect(self.vwOptGridYSize_slider_onStateChanged)
        self._ui.vwOptGridSpacing_slider.valueChanged.connect(self.vwOptGridSpacing_slider_onStateChanged)
        # self._ui.vwOptGridColor_btn.clicked.connect(self.on_vwOptGridColor_btn_clicked) # called auatomatically

        # Grid Marker
        self._ui.vwOptGridMarkers_checkBox.stateChanged.connect(self.on_vwOptGridMarkers_checkBox_onStateChanged)
        # self._ui.vwOptGridMarkersColor_btn.clicked.connect(self.on_vwOptGridMarkersColor_btn_clicked) # called automatically
        self.vwOptGridMarkersFontSize_slider.valueChanged.connect(self.on_vwOptGridMarkersFontSize_slider_onStateChanged)

        # Viewer
        # to create labelled sliders
        self._ui.vwOptPtsSize_edit.editingFinished.connect(self.on_vwOptPtsSize_lineEdit_onEditingFinished)
        self._ui.vwOptPtsSize_slider.valueChanged.connect(self.on_vwOptPtsSize_slider_onStateChanged)
        # self._ui.vwOptBackGroundColor_btn.clicked.connect(self.on_vwOptBackGroundColor_btn_clicked) # called automatically

        # file sequence
        # self._ui.playFrame_btn.clicked.connect(self.on_playFrame_btn_clicked) # called automatically
        # self._ui.stopFrame_btn.clicked.connect(self.on_stopFrame_btn_clicked) # called automatically
        # self._ui.previousFrame_btn.clicked.connect(self.on_previousFrame_btn_clicked) # called automatically
        # self._ui.nextFrame_btn.clicked.connect(self.on_nextFrame_btn_clicked) # called automatically
        self._ui.offline_checkbox.stateChanged.connect(self.on_offline_checkbox_onStateChanged)
        self._ui.frameViewer_slider.valueChanged.connect(self.on_frameViewer_slider_onStateChanged)
        self._ui.stepFrame_edit.editingFinished.connect(self.on_stepFrame_lineEdit_onEditingFinished)
        self._ui.currentFrame_edit.editingFinished.connect(self.on_currentFrame_lineEdit_onEditingFinished)
        self._ui.playSpeed_edit.editingFinished.connect(self.on_playSpeed_lineEdit_onEditingFinished)
        self._ui.firstFrame_edit.editingFinished.connect(self.on_firstFrame_lineEdit_onEditingFinished)
        self._ui.lastFrame_edit.editingFinished.connect(self.on_lastFrame_lineEdit_onEditingFinished)


        # filter
        self._ui.postProcessing_checkBox.stateChanged.connect(self.on_postProcessing_checkBox_onStateChanged)
        self._ui.filters_comboBox.currentIndexChanged.connect(self.on_filters_comboBox_IndexChanged)
        self._ui.chosenFilter_checkBox.stateChanged.connect(self.on_chosenFilter_checkBox_onStateChanged)
        # self._ui.addFilter_btn.clicked.connect(self.on_addFilter_btn_clicked) # called automatically
        # self._ui.removeAlgorithm_btn.clicked.connect(self.on_removeAlgorithm_btn_clicked) # called automatically
        # self._ui.clearAlgorithm_btn.clicked.connect(self.on_clearAlgorithm_btn_clicked)  # called automatically
        # self._ui.moveDownAlgorithm_btn.clicked.connect(self.on_moveDownAlgorithm_btn_clicked) # called automatically
        # self._ui.moveUpAlgorithm_btn.clicked.connect(self.on_moveUpAlgorithm_btn_clicked) # called automatically


        # bounding box filter
        self._ui.filterMinx_edit.editingFinished.connect(self.on_anyFilterBdLimits_lineEdit_onEditingFinished)
        self._ui.filterMiny_edit.editingFinished.connect(self.on_anyFilterBdLimits_lineEdit_onEditingFinished)
        self._ui.filterMinz_edit.editingFinished.connect(self.on_anyFilterBdLimits_lineEdit_onEditingFinished)
        self._ui.filterMaxx_edit.editingFinished.connect(self.on_anyFilterBdLimits_lineEdit_onEditingFinished)
        self._ui.filterMaxy_edit.editingFinished.connect(self.on_anyFilterBdLimits_lineEdit_onEditingFinished)
        self._ui.filterMaxz_edit.editingFinished.connect(self.on_anyFilterBdLimits_lineEdit_onEditingFinished)

        # velocity filter
        self._ui.filterMinVelocity_edit.editingFinished.connect(
            self.on_anyFilterVelocityThresh_lineEdit_onEditingFinished)
        self._ui.filterMaxVelocity_edit.editingFinished.connect(
            self.on_anyFilterVelocityThresh_lineEdit_onEditingFinished)

        # intensity filter
        self._ui.filterMinIntensity_edit.editingFinished.connect(
            self._on_anyFilterIntensityThresh_lineEdit_onEditingFinished)
        self._ui.filterMaxIntensity_edit.editingFinished.connect(
            self._on_anyFilterIntensityThresh_lineEdit_onEditingFinished)
    ####################################

    ######## initializers ########
    def initializeWidgets(self):
        self.intializeColorDialogs()
        self.initializeColormap()
        self.initializeViewer()
        self.initializeAxes()
        self.initializeGrid()
        self.initializeGridMarkers()
        self.initializeOfflinePlayBtns()
        self.initializeFilters()
        self.update()

    def intializeColorDialogs(self):
        self.gridColorDialog = QtWidgets.QColorDialog(self)
        self.BGColorDialog = QtWidgets.QColorDialog(self)
        self.gridMarkersDialog = QtWidgets.QColorDialog(self)

    ## viewer Initializer ##
    def initializeViewer(self):
        # print("initializeViewer")
        self._plot = gl.GLScatterPlotItem()
        self._ui.cloudViewer_widget.addItem(self._plot)
        self._plot.setGLOptions("opaque")
        self._backgroundColor = QtGui.QColor.fromRgb(0, 0, 0)
        self._ui.vwOptBGColor_btn.setStyleSheet("background-color: %s" % self._backgroundColor.name())
        self._ui.cloudViewer_widget.setBackgroundColor(self._backgroundColor)

        self.adjustLogo()

        self._ptSize = 0.02
        self._ui.vwOptPtsSize_edit.setText(str(self._ptSize))
        self._ui.vwOptPtsSize_slider.setSingleStep(self._ptSize*1000)
        self._ui.vwOptPtsSize_slider.setMinimum(self._ptSize*1000)
        self._ui.vwOptPtsSize_slider.setMaximum(0.1*1000)

        # adjusting camera for target that is at a distance 300 meters
        # decrease setZ (30 meters) if the distance to target is less than 50 meters
        # position = QtGui.QVector3D()
        # self._cameraXPos = 20.0
        # self._cameraYPos = -20.0
        # self._cameraZPos = 100.0
        # position.setX(self._cameraXPos)
        # position.setY(self._cameraYPos)
        # position.setZ(self._cameraZPos)
        # self._ui.cloudViewer_widget.setCameraPosition(pos = position)
        self._cameraDistance = 60
        self._cameraElevation = 50.0
        self._cameraAzimuth = -65.0
        self._ui.cloudViewer_widget.setCameraPosition(distance = self._cameraDistance)
        self._ui.cloudViewer_widget.setCameraPosition(elevation = self._cameraElevation)
        self._ui.cloudViewer_widget.setCameraPosition(azimuth = self._cameraAzimuth)
    def adjustLogo(self):
        color = self._backgroundColor.getRgb()
        if (color[0] * 0.299 + color[1] * 0.587 + color[2] * 0.114) > 186:
            self._ui.logo_widget.setStyleSheet("image: url(:/icons/icons/Logo_Scantinel_Black_Transparent.png)")
        else:
            self._ui.logo_widget.setStyleSheet("image: url(:/icons/icons/Logo_Scantinel_white_Transparent.png)")

    ## colormap Initializer ##
    def initializeColormap(self):
        # print("initializeColormap")
        self._model._maxReset = 1.0
        self._model._minReset = 0.0
        colormapsStr = self._model.colormaps
        self._ui.vwOptColormap_comboBox.addItems(colormapsStr)
        self._ui.vwOptColormapMin_edit.setText(str(self._model._minReset))
        self._ui.vwOptColormapMax_edit.setText(str(self._model._maxReset))

        self._ui.vwOptColormap_comboBox.setCurrentText(defaultColorMap)
        self.colormap = pg.colormap.get(self._ui.vwOptColormap_comboBox.currentText())

        self._ui.vwOptColormapViewer_widget.paintEvent = \
            lambda event, localSelf=self._ui.vwOptColormapViewer_widget: \
                QtGui.QPainter(localSelf).fillRect(
                    localSelf.rect(),
                    self.colormap.getGradient(localSelf.rect().topLeft(),
                                              localSelf.rect().topRight()))

    ## Axes Initializer ##
    def initializeAxes(self):
        # print("initializeAxes")
        self._axesSize = 1
        self._axesBool = False

        self._xaxis = None
        self._yaxis = None
        self._zaxis = None

        self._xaxis = gl.GLLinePlotItem(pos=np.asarray([[0, 0, 0], [self._axesSize, 0, 0]]), color=(1, 0, 0, 1),
                                        width=2)
        self._xaxis.setGLOptions('opaque')
        self._yaxis = gl.GLLinePlotItem(pos=np.asarray([[0, 0, 0], [0, self._axesSize, 0]]), color=(0, 1, 0, 1),
                                        width=2)
        self._yaxis.setGLOptions('opaque')
        self._zaxis = gl.GLLinePlotItem(pos=np.asarray([[0, 0, 0], [0, 0, self._axesSize]]), color=(0, 0, 1, 1),
                                        width=2)
        self._zaxis.setGLOptions('opaque')

        self._ui.cloudViewer_widget.addItem(self._xaxis)
        self._ui.cloudViewer_widget.addItem(self._yaxis)
        self._ui.cloudViewer_widget.addItem(self._zaxis)

        self._ui.vwOptAxes_checkBox.setChecked(self._axesBool)
        self._xaxis.setVisible(self._axesBool)
        self._yaxis.setVisible(self._axesBool)
        self._zaxis.setVisible(self._axesBool)

    ## Grid Initializer ##
    def initializeGrid(self):
        # print("initializeGrid")
        self._grid = gl.GLGridItem()
        self._gridBool = True
        self._gridSpacing = 2
        self._gridXSize = 8
        self._gridYSize = 20

        self._grid.setVisible(self._gridBool)
        self._ui.vwOptGrid_checkBox.setChecked(self._gridBool)
        self._ui.cloudViewer_widget.addItem(self._grid)

        self._ui.vwOptGridXSize_edit.setText(str(self._gridXSize))
        self._ui.vwOptGridYSize_edit.setText(str(self._gridYSize))
        self._ui.vwOptGridSpacing_edit.setText(str(self._gridSpacing))

        self._ui.vwOptGridXSize_slider.setMinimum(1)
        self._ui.vwOptGridXSize_slider.setMaximum(300)
        self._ui.vwOptGridXSize_slider.setValue(self._gridXSize)

        self._ui.vwOptGridYSize_slider.setMinimum(1)
        self._ui.vwOptGridYSize_slider.setMaximum(300)
        self._ui.vwOptGridYSize_slider.setValue(self._gridYSize)

        self._ui.vwOptGridSpacing_slider.setMinimum(1)
        self._ui.vwOptGridSpacing_slider.setMaximum(20)
        self._ui.vwOptGridSpacing_slider.setValue(self._gridSpacing)

        self._gridColor = QtGui.QColor.fromRgb(0, 0, 0)
        self._ui.vwOptGridColor_btn.setStyleSheet("background-color: %s" % self._gridColor.name())
        self._grid.setColor(self._gridColor)
        self._setGrid()
    def initializeGridMarkers(self):
        self._fontSize = self._model.gridMarkersFontSizes[self._ui.vwOptGridMarkersFontSize_slider.value()]
        self._fontType = 'Helvetica'
        self._gridMarkersColor = self._gridColor
        self._gridMarkerBool = True
        self._gridMarkers = []

        self._setGridMarker()

    ## offline Initializers ##
    def initializeOfflinePlayBtns_offlineMode(self):
        self._model._stepFrame = 1
        self._model._currentFrame = 0
        self._model._firstFrame = 0
        self._model._lastFrame = len(self._model._filesList)-1
        # self._model._firstFrame = 816
        # self._model._lastFrame = 1181
        self._model._playSpeed = 10

        self.enable_PlayOfflineKeys()
        self._ui.stopFrame_btn.setEnabled(False)

        self._ui.frameViewer_slider.setMinimum(0)
        self._ui.frameViewer_slider.setMaximum(len(self._model._filesList)-1)

        self._totalFramesCount = len(self._model._filesList)
        self._ui.stepFrame_edit.setText(str(self._model._stepFrame))
        self._ui.currentFrame_edit.setText(str(self._model._currentFrame))
        self._ui.totalFrame_lbl.setText(str(f"/{self._totalFramesCount}"))
        self._ui.playSpeed_edit.setText(str(f"{self._model._playSpeed}"))

        self._ui.firstFrame_edit.setText(str(self._model._firstFrame))
        self._ui.lastFrame_edit.setText(str(self._model._lastFrame))
    def initializeOfflinePlayBtns(self):
        self.disable_PlayOfflineKeys()

    ## filters Initializers ##
    def initializeFilters(self):
        self._model._postProcessingBool = False
        self._ui.postProcessing_checkBox.setChecked(self._model._postProcessingBool)
        self._ui.filters_comboBox.addItems(self._model.filters)
        self.setFilterSummary()

        self._model._chosenFilter = self._ui.filters_comboBox.currentText()
        self._ui.boundingBoxFilter_frame.setVisible(True)
        self._ui.filterVelocity_frame.setVisible(False)
        self._ui.filterIntensity_frame.setVisible(False)

        # bounding box filter
        self._model._filterBdBoxMin = [-6, 0, -5]
        self._model._filterBdBoxMax = [6, 20, 5]

        self._ui.filterMinx_edit.setText(str(self._model._filterBdBoxMin[0]))
        self._ui.filterMiny_edit.setText(str(self._model._filterBdBoxMin[1]))
        self._ui.filterMinz_edit.setText(str(self._model._filterBdBoxMin[2]))
        self._ui.filterMaxx_edit.setText(str(self._model._filterBdBoxMax[0]))
        self._ui.filterMaxy_edit.setText(str(self._model._filterBdBoxMax[1]))
        self._ui.filterMaxz_edit.setText(str(self._model._filterBdBoxMax[2]))

        # velocity filters
        self._model._filterVelocityMin = 0
        self._model._filterVelocityMax = 35
        self._ui.filterMinVelocity_edit.setText(str(self._model._filterVelocityMin))
        self._ui.filterMaxVelocity_edit.setText(str(self._model._filterVelocityMax))

        # intensity filter
        self._model._filterIntensityMin = 0
        self._model._filterIntensityMax = 10
        self._ui.filterMinIntensity_edit.setText(str(self._model._filterIntensityMin))
        self._ui.filterMaxIntensity_edit.setText(str(self._model._filterIntensityMax))

        self._ui.filters_frame.setEnabled(False)
    ######################################

    ######## Slots ########
    ## colormap slots ##
    @pyqtSlot()
    def on_vwOptColorPts_comboBox_IndexChanged(self):
        # print("on_vwOptColorPts_comboBox_IndexChanged")
        self._model.colorPtsChoice = self._ui.vwOptColorPts_comboBox.currentText()

    @pyqtSlot()
    def on_vwOptColormapMax_btn_clicked(self):
        # print("on_vwOptColormapMax_btn_clicked")
        if self._model.dataSet:
            self._model.colorPtsChoice = self._ui.vwOptColorPts_comboBox.currentText()

            if self._model.colorPtsChoice != '':
                self._model._maxReset = np.max(self._model.colorSet[self._model.colorPtsChoice])
                self._ui.vwOptColormapMax_edit.setText(f"{self._model._maxReset:.3f}")

    @pyqtSlot()
    def on_vwOptColormapMin_btn_clicked(self):
        # print("on_vwOptColormapMin_btn_clicked")
        if self._model.dataSet:
            self._model.colorPtsChoice = self._ui.vwOptColorPts_comboBox.currentText()

            if self._model.colorPtsChoice != '':
                self._model._minReset = np.min(self._model.colorSet[self._model.colorPtsChoice])
                self._ui.vwOptColormapMin_edit.setText(f"{self._model._minReset:.3f}")

    @pyqtSlot()
    def vwOptColormapMax_lineEdit_onStateChanged(self):
        # print("vwOptColormapMax_lineEdit_onStateChanged")
        try:
            self._model._maxReset = float(self._ui.vwOptColormapMax_edit.text())
            if self._model.dataSet:
                self._model.colorPtsChoice = self._ui.vwOptColorPts_comboBox.currentText()
        except:
            pass

    @pyqtSlot()
    def vwOptColormapMin_lineEdit_onStateChanged(self):
        # print("vwOptColormapMin_lineEdit_onStateChanged")
        try:
            self._model._minReset = float(self._ui.vwOptColormapMin_edit.text())
            if self._model.dataSet:
                self._model.colorPtsChoice = self._ui.vwOptColorPts_comboBox.currentText()
        except:
            pass

    @pyqtSlot()
    def on_vwOptColormap_comboBox_IndexChanged(self):
        # print("on_vwOptColormap_comboBox_IndexChanged")
        self.setColorChoice()
    ###################################

    ## viewer slots ##
    @pyqtSlot()
    def on_vwOptBGColor_btn_clicked(self):
        # print("on_vwOptBGColor_btn_clicked")
        try:
            self.BGColorDialog.setCurrentColor(self._backgroundColor)
            self.BGColorDialog.setStandardColor(1, self._backgroundColor)
            self.BGColorDialog.exec_()
            if not self.BGColorDialog.selectedColor().isValid():  # user canceled
                return

            self._backgroundColor = self.BGColorDialog.selectedColor()
            self._ui.vwOptBGColor_btn.setStyleSheet("background-color: %s" % self._backgroundColor.name())
            self._ui.cloudViewer_widget.setBackgroundColor(self._backgroundColor)

            self.adjustLogo()

        except Exception as e:
            raise(e)

    @pyqtSlot()
    def on_vwOptPtsSize_lineEdit_onEditingFinished(self):
        # print("on_vwOptPtsSize_lineEdit_onStateChanged")
        try:
            self._ptSize = float(self._ui.vwOptPtsSize_edit.text())
            self._plot.setData(size=self._ptSize)
        except Exception as e:
            pass

    def on_vwOptPtsSize_slider_onStateChanged(self):
        # print("on_vwOptPtsSize_slider_onStateChanged")
        self._ptSize = self._ui.vwOptPtsSize_slider.value()/1000
        self._ui.vwOptPtsSize_edit.setText(str(self._ptSize))
        self._plot.setData(size=self._ptSize)
    ###################################

    ## grid slots ##
    @pyqtSlot()
    def on_vwOptGridMarkers_checkBox_onStateChanged(self):
        # print("vwOptGrid_checkBox_onStateChanged")
        self._gridMarkerBool = self._ui.vwOptGridMarkers_checkBox.isChecked()
        for item in self._gridMarkers:
            item.setVisible(self._gridMarkerBool)

    @pyqtSlot()
    def on_vwOptGridMarkersFontSize_slider_onStateChanged(self):
        # print("on_vwOptGridMarkersFontSize_slider_onStateChanged")
        self._fontSize = self._model.gridMarkersFontSizes[self._ui.vwOptGridMarkersFontSize_slider.value()]
        for oldItem in self._gridMarkers:
            oldItem.setData(font = QtGui.QFont(self._fontType, self._fontSize))

    @pyqtSlot()
    def on_vwOptGridColor_btn_clicked(self):
        # print("on_vwOptGridColor_btn_clicked")
        self.gridColorDialog.setCurrentColor(self._gridColor)
        self.gridColorDialog.setStandardColor(1, self._gridColor)
        self.gridColorDialog.exec_()

        if not self.gridColorDialog.selectedColor().isValid():  # user canceled
            return

        self._gridColor = self.gridColorDialog.selectedColor()
        self._ui.vwOptGridColor_btn.setStyleSheet("background-color: %s" % self._gridColor.name())
        self._grid.setColor(self._gridColor)

        try:
            for gridMarker in self._gridMarkers:
                gridMarker.setData(color = self._gridColor)
        except Exception as e:
            pass

    @pyqtSlot()
    def vwOptGridSpacing_lineEdit_onStateChanged(self):
        # print("vwOptGridSpacing_lineEdit_onStateChanged")
        try:
            self._gridSpacing = int(self._ui.vwOptGridSpacing_edit.text())
            self._setGrid()
            self._setGridMarker()
        except Exception as e:
            pass

    @pyqtSlot()
    def vwOptGridSpacing_slider_onStateChanged(self):
        # print("vwOptGridSpacing_slider_onStateChanged")
        try:
            self._gridSpacing = int(self._ui.vwOptGridSpacing_slider.value())
            self._ui.vwOptGridSpacing_edit.setText(str(self._gridSpacing))
            self._setGrid()
            self._setGridMarker()
        except Exception as e:
            pass

    @pyqtSlot()
    def vwOptGridYSize_lineEdit_onStateChanged(self):
        # print("vwOptGridYSize_lineEdit_onStateChanged")
        try:
            self._gridYSize = int(self._ui.vwOptGridYSize_edit.text())
            self._setGrid()
            self._setGridMarker()
        except Exception as e:
            pass

    @pyqtSlot()
    def vwOptGridYSize_slider_onStateChanged(self):
        # print("vwOptGridYSize_slider_onStateChanged")
        try:
            self._gridYSize = int(self._ui.vwOptGridYSize_slider.value())
            self._ui.vwOptGridYSize_edit.setText(str(self._gridYSize))
            self._setGrid()
            self._setGridMarker()
        except Exception as e:
            pass

    @pyqtSlot()
    def vwOptGridXSize_lineEdit_onStateChanged(self):
        # print("vwOptGridXSize_lineEdit_onStateChanged")
        try:
            self._gridXSize = int(self._ui.vwOptGridXSize_edit.text())
            self._setGrid()
            self._setGridMarker()
        except Exception as e:
            pass

    @pyqtSlot()
    def vwOptGridXSize_slider_onStateChanged(self):
        # print("vwOptGridXSize_slider_onStateChanged")
        try:
            self._gridXSize = int(self._ui.vwOptGridXSize_slider.value())
            self._ui.vwOptGridXSize_edit.setText(str(self._gridXSize))
            self._setGrid()
            self._setGridMarker()
        except Exception as e:
            pass

    @pyqtSlot()
    def vwOptGrid_checkBox_onStateChanged(self):
        # print("vwOptGrid_checkBox_onStateChanged")
        self._grid.setVisible(self._ui.vwOptGrid_checkBox.isChecked())

    def _setGrid(self):
        # print("_setGrid")
        spacing = self._gridSpacing
        xSize = self._gridXSize
        ySize = self._gridYSize
        self._grid.resetTransform()
        self._grid.setSize(xSize, ySize, 0)

        self._grid.translate(-np.floor(xSize/2/spacing)*spacing + xSize/2,ySize/2,0)
        self._grid.setSpacing(spacing, spacing, 0)
        self._grid.setColor(self._gridColor)

    def _setGridMarker(self):
        # print("_setGridMarker")
        self._ui.vwOptGridMarkers_checkBox.setChecked(self._gridMarkerBool)
        self._gridMarkersColor = self._gridColor

        try:
            if self._gridMarkers:
                for gridMarker in self._gridMarkers:
                    self._ui.cloudViewer_widget.removeItem(gridMarker)
                self._gridMarkers.clear()

            xpos = np.arange(-self._gridXSize/2, self._gridXSize/2+1e-3, self._gridSpacing)
            xpos += self._gridXSize/2 - np.floor(self._gridXSize/2/self._gridSpacing)*self._gridSpacing
            for xp in xpos:
                strMeter = f"{xp}m"
                markerItem = gl.GLTextItem(text=strMeter, pos=[xp, 0, 0],
                                           font=QtGui.QFont(self._fontType, self._fontSize),
                                           color=self._gridMarkersColor)
                self._gridMarkers.append(markerItem)
                markerItem.setVisible(self._gridMarkerBool)
                self._ui.cloudViewer_widget.addItem(markerItem)

            ypos = np.arange(-self._gridYSize / 2, self._gridYSize / 2 + 1e-3, self._gridSpacing)
            ypos += self._gridYSize / 2
            for yp in ypos:
                strMeter = f"{yp}m"
                markerItem = gl.GLTextItem(text=strMeter, pos=[0,yp, 0],
                                           font=QtGui.QFont(self._fontType, self._fontSize),
                                           color=self._gridMarkersColor)
                self._gridMarkers.append(markerItem)
                markerItem.setVisible(self._gridMarkerBool)
                self._ui.cloudViewer_widget.addItem(markerItem)
        except Exception as e:
            pass
    ###################################

    ## axes slots ##
    @pyqtSlot()
    def vwOptAxes_checkBox_onStateChanged(self):
        # print("vwOptAxes_checkBox_onStateChanged")
        self._axesBool = self._ui.vwOptAxes_checkBox.isChecked()

        self._xaxis.setVisible(self._axesBool)
        self._yaxis.setVisible(self._axesBool)
        self._zaxis.setVisible(self._axesBool)
    ###################################

    ## offline playing slots ##
    @pyqtSlot()
    def on_offline_checkbox_onStateChanged(self):
        self._model._offlineBool = not self._model._offlineBool
        self._ui.offline_checkbox.setChecked(self._model._offlineBool)

        if self._model._offlineBool:
            if self._model._filesList:
                self.enable_PlayOfflineKeys()
                self._ui.stopFrame_btn.setEnabled(False)
            else:
                self.disable_PlayOfflineKeys()
                self._ui.loadCloudFolderMenu_btn.setEnabled(True)
        else:
            self.disable_PlayOfflineKeys()

    @pyqtSlot()
    def on_loadCloudFolderMenu_btn_clicked(self):
        # print("on_loadCloudFolderMenu_btn_clicked")
        try:
            dialog = QFileDialog()
            # folderPath = r"..\rawdata"
            folderPath = dialog.getExistingDirectory(self, 'title', '.')
            if folderPath:
                self._model.folderPath = folderPath
                self._ui.loadCloudFolderMenu_edit.setText(folderPath)
                if self._model._filesList:
                    self.initializeOfflinePlayBtns_offlineMode()
                    self._totalFramesCount = len(self._model._filesList)
                    self._ui.totalFrame_lbl.setText(f"/{self._totalFramesCount - 1}")

        except Exception as e:
            raise(e)

    @pyqtSlot(str)
    def on_folderPath_read(self, value):
        # print("on_file_read")
        self._model._filesList = self._main_controller.readFileSeq(value)
        if self._model._filesList:
            self._model._currentFrame = 0
            self._model._filePath = self._model._filesList[self._model._currentFrame]
            self.readFrame(self._model._filePath)

    @pyqtSlot()
    def on_playSpeed_lineEdit_onEditingFinished(self):
        # print("on_playSpeed_lineEdit_onStateChanged")
        try:
            self._model._playSpeed = int(self._ui.playSpeed_edit.text())
            if self.timer.isActive():
                self.timer.stop()
                self.timer.deleteLater()

                self.timer = QtCore.QTimer(self)
                self.timer.start(self._model._playSpeed)
                self.timer.timeout.connect(self.playFrames)
        except Exception as e:
            pass

    @pyqtSlot()
    def on_frameViewer_slider_onStateChanged(self):
        self._model._currentFrame = self._ui.frameViewer_slider.value()
        self._model._filePath = self._model._filesList[self._model._currentFrame]
        self.readFrame(self._model._filePath)

    @pyqtSlot()
    def on_stepFrame_lineEdit_onEditingFinished(self):
        try:
            self._model._stepFrame = int(self._ui.stepFrame_edit.text())
            self._ui.frameViewer_slider.setTickInterval(0)
            self._ui.frameViewer_slider.setSingleStep(self._model._stepFrame)
        except Exception as e:
            pass

    @pyqtSlot()
    def on_currentFrame_lineEdit_onEditingFinished(self):
        try:
            self._model._currentFrame = int(self._ui.currentFrame_edit.text())
            self.setFrameSliderMessage(self._model._currentFrame)
            self._model._filePath = self._model._filesList[self._model._currentFrame]
            self.readFrame(self._model._filePath)
        except Exception as e:
            pass

    @pyqtSlot()
    def on_nextFrame_btn_clicked(self):
        self._model._currentFrame = self._model._currentFrame + self._model._stepFrame
        if self._model._currentFrame > self._model._lastFrame or self._model._currentFrame < self._model._firstFrame:
            self._model._currentFrame = self._model._firstFrame
        self.setFrameSliderMessage(self._model._currentFrame)
        self._model._filePath = self._model._filesList[self._model._currentFrame]
        self.readFrame(self._model._filePath)

    @pyqtSlot()
    def on_previousFrame_btn_clicked(self):
        self._model._currentFrame = self._model._currentFrame - self._model._stepFrame
        if self._model._currentFrame < self._model._firstFrame or self._model._currentFrame < self._model._firstFrame:
            self._model._currentFrame = self._model._lastFrame
        self.setFrameSliderMessage(self._model._currentFrame)
        self._model._filePath = self._model._filesList[self._model._currentFrame]
        self.readFrame(self._model._filePath)

    def readFrame(self, fileName):
        try:
            ext = os.path.splitext(fileName)[1].split('.')[1]
            if ext in self._model.fileTypes:
                if ext == "bin":
                    if self.isVisible():
                        if re.match(".*carla.*",fileName):
                            dist, velo = self._main_controller.bin_data_extraction_carlaFiles(fileName)
                            intensity = 0*dist
                        else:
                            # dist, velo, intensity,framenumber = self._main_controller.bin_data_extraction_binFiles(fileName)
                            data2D = self._main_controller.bin_data_extraction_binFiles(
                                fileName)
                        self.setcurrentFrameEditMessage(self._model._currentFrame)
                        # globalfile.data2D = (dist, velo, intensity, framenumber)
                        globalfile.data2D = data2D

                        self.newDataArrive()
                    else:
                        pass
            else:
                raise Exception("File Type is not supported")
        except Exception as e:
            raise(e)

    def disable_PlayOfflineKeys(self):
        widgets = [self._ui.playFrame_btn,
                   self._ui.stopFrame_btn,
                   self._ui.nextFrame_btn,
                   self._ui.previousFrame_btn,
                   self._ui.frameViewer_slider,
                   self._ui.stepFrame_edit,
                   self._ui.stepFrame_edit,
                   self._ui.currentFrame_edit,
                   self._ui.playSpeed_edit,
                   self._ui.firstFrame_edit,
                   self._ui.lastFrame_edit,
                   self._ui.loadCloudFolderMenu_btn]

        self.disableWidgets(widgets)

    def enable_PlayOfflineKeys(self):
        widgets = [self._ui.playFrame_btn,
                   self._ui.stopFrame_btn,
                   self._ui.nextFrame_btn,
                   self._ui.previousFrame_btn,
                   self._ui.frameViewer_slider,
                   self._ui.stepFrame_edit,
                   self._ui.currentFrame_edit,
                   self._ui.playSpeed_edit,
                   self._ui.firstFrame_edit,
                   self._ui.lastFrame_edit,
                   self._ui.loadCloudFolderMenu_btn]

        self.enableWidgets(widgets)

    def enable_PlayOfflineKeys_OnPlay(self):
        widgets = [self._ui.stopFrame_btn,
                   self._ui.playFrame_btn,
                   self._ui.nextFrame_btn,
                   self._ui.previousFrame_btn,
                   self._ui.frameViewer_slider,
                   self._ui.currentFrame_edit,
                   self._ui.loadCloudFolderMenu_btn,
                   self._ui.offline_checkbox]

        self.enableWidgets(widgets)
        self._ui.stopFrame_btn.setEnabled(False)

    def disable_PlayOfflineKeys_OnStop(self):
        widgets = [self._ui.stopFrame_btn,
                   self._ui.playFrame_btn,
                   self._ui.nextFrame_btn,
                   self._ui.previousFrame_btn,
                   self._ui.frameViewer_slider,
                   self._ui.currentFrame_edit,
                   self._ui.loadCloudFolderMenu_btn,
                   self._ui.offline_checkbox]

        self.disableWidgets(widgets)
        self._ui.stopFrame_btn.setEnabled(True)

    @pyqtSlot()
    def on_stopFrame_btn_clicked(self):
        self._model._autoRunBool = False
        self.timer.stop()
        self.timer.deleteLater()
        self.enable_PlayOfflineKeys_OnPlay()

    @pyqtSlot()
    def on_playFrame_btn_clicked(self):
        self._model._autoRunBool = True
        self.disable_PlayOfflineKeys_OnStop()

        self.timer = QtCore.QTimer(self)
        self.timer.start(self._model._playSpeed)
        self.timer.timeout.connect(self.playFrames)

    @pyqtSlot()
    def on_firstFrame_lineEdit_onEditingFinished(self):
        try:
            self._model._firstFrame = int(self._ui.firstFrame_edit.text())
        except Exception as e:
            pass

    @pyqtSlot()
    def on_lastFrame_lineEdit_onEditingFinished(self):
        try:
            self._model._lastFrame = int(self._ui.lastFrame_edit.text())
        except Exception as e:
            pass

    def setFrameSliderMessage(self, val):
        self._ui.frameViewer_slider.blockSignals(True)
        self._ui.frameViewer_slider.setValue(val)
        self._ui.frameViewer_slider.blockSignals(False)

    def setcurrentFrameEditMessage(self, val):
        self._ui.currentFrame_edit.blockSignals(True)
        self._ui.currentFrame_edit.setText(str(val))
        self._ui.currentFrame_edit.blockSignals(False)

    def playFrames(self):
        if not self._model._autoRunBool:
            return
        self._model._currentFrame = self._model._currentFrame + self._model._stepFrame
        if self._model._currentFrame > self._model._lastFrame or self._model._currentFrame < self._model._firstFrame:
            self._model._currentFrame = self._model._firstFrame

        self.setFrameSliderMessage(self._model._currentFrame)
        self._model._filePath = self._model._filesList[self._model._currentFrame]
        self.readFrame(self._model._filePath)
    ###################################

    ## model slots ##
    @pyqtSlot(np.ndarray)
    def on_packet_read(self, value):
        # print(' on packet read')
        if self.isVisible():
            self._main_controller.packet_data_extraction_bin(value)
        else:
            pass

    @pyqtSlot(np.ndarray)
    def on_pcd_read(self, value):
        # print("on_pcd_read")
        self.setFilterSummary()
        self._plot.setData(pos=value, size=self._ptSize, pxMode=False)

    @pyqtSlot(dict)
    def on_dataSet_read(self, value):
        # print("on_dataSet_read")
        if not self._model._dataReceived:
            self._ui.vwOptData_comboBox.addItems(value.keys())
            self._ui.vwOptData_comboBox.setCurrentText("xyz")
            self._model._dataReceived = True

        if sorted(value.keys()) == sorted(self._model.checkDataList):
            self.setDataChoice()
        else:
            raise Exception("Data Type Choices is not as expected")

    def setDataChoice(self):
        # print("setDataChoice")
        self._model.dataChoice = self._ui.vwOptData_comboBox.currentText()

    @pyqtSlot()
    def on_vwOptData_comboBox_IndexChanged(self):
        # print("on_vwOptData_comboBox_IndexChanged")
        self.setDataChoice()

    @pyqtSlot(dict)
    def on_colorSet_read(self, value):
        # print("on_colorSet_read")
        if not self._model._colorReceived:
            self._ui.vwOptColorPts_comboBox.addItems(value.keys())
            self._ui.vwOptColorPts_comboBox.setCurrentText("r_image")
            self._model._colorReceived = True

        if sorted(value.keys()) == sorted(self._model.checkColorList):
            self.setColorChoice()
        else:
            raise Exception("Color Data Choices is not as expected")

    def setColorChoice(self):
        # print("setColorChoice")
        self.colormap = pg.colormap.get(self._ui.vwOptColormap_comboBox.currentText())

        self._ui.vwOptColormapViewer_widget.paintEvent = \
            lambda event, localSelf=self._ui.vwOptColormapViewer_widget: \
                QtGui.QPainter(localSelf).fillRect(
                    localSelf.rect(),
                    self.colormap.getGradient(localSelf.rect().topLeft(),
                                              localSelf.rect().topRight()))

        if self._model.dataSet:
            self._model.colorPtsChoice = self._ui.vwOptColorPts_comboBox.currentText()

        self.update()

    @pyqtSlot()
    def on_dataChoice_read(self):
        if self._model.dataChoice != '':
            self._model.pcd = self._model.dataSet[self._model.dataChoice]

    @pyqtSlot()
    def on_colorPtsChoice_read(self):
        if self._model.colorPtsChoice != '':
            dataColor = self._model.colorSet[self._model.colorPtsChoice]

            cm = pg.colormap.get(self._ui.vwOptColormap_comboBox.currentText())
            min_v = self._model._minReset
            max_v = self._model._maxReset
            dataColorCM = self._main_controller.calcColormap(min_v, max_v, dataColor, cm)

            self.setFilterSummary()
            self._plot.setData(color = dataColorCM)

    ## filter slots ##
    def setFilterSummary(self):
        if self._model._postProcessingBool:
            self._ui.cntBefore_lbl.setText(str(f"Count Before: {self._model._cntBefore[0]}"))
            self._ui.cntAfter_lbl.setText(str(f"Count After: {self._model._cntAfter[0]}"))
            self._ui.ptsRemove_lbl.setText(str(f"Points Removed : {self._model._cntBefore[0] - self._model._cntAfter[0]}"))
        else:
            self._ui.cntBefore_lbl.setText(str(f"Count Before: -"))
            self._ui.cntAfter_lbl.setText(str(f"Count After: -"))
            self._ui.ptsRemove_lbl.setText(str(f"Points Removed : -"))

    @pyqtSlot()
    def on_postProcessing_checkBox_onStateChanged(self):
        self._model._postProcessingBool = not self._model._postProcessingBool
        self._ui.postProcessing_checkBox.setChecked(self._model._postProcessingBool)

        if self._model._postProcessingBool:
            self._ui.filters_frame.setEnabled(True)
        else:
            self._ui.filters_frame.setEnabled(False)

    @pyqtSlot()
    def on_chosenFilter_checkBox_onStateChanged(self):
        self._model._chosenFilterBool = not self._model._chosenFilterBool
        self._ui.chosenFilter_checkBox.setChecked(self._model._chosenFilterBool)

    @pyqtSlot()
    def on_filters_comboBox_IndexChanged(self):
        self._model._chosenFilter = self._ui.filters_comboBox.currentText()
        widgets = [self._ui.filterIntensity_frame,
                   self._ui.filterVelocity_frame,
                   self._ui.boundingBoxFilter_frame]

        if self._model._chosenFilter == self._model.filters[0]:
            self.hideWidgets(widgets)
            self._ui.boundingBoxFilter_frame.setVisible(True)
        elif self._model._chosenFilter == self._model.filters[1]:
            self.hideWidgets(widgets)
            self._ui.filterVelocity_frame.setVisible(True)
        elif self._model._chosenFilter == self._model.filters[2]:
            self.hideWidgets(widgets)
            self._ui.filterIntensity_frame.setVisible(True)

    @pyqtSlot()
    def on_anyFilterBdLimits_lineEdit_onEditingFinished(self):
        try:
            self._model._filterBdBoxMin[0] = float(self._ui.filterMinx_edit.text())
            self._model._filterBdBoxMin[1] = float(self._ui.filterMiny_edit.text())
            self._model._filterBdBoxMin[2] = float(self._ui.filterMinz_edit.text())

            self._model._filterBdBoxMax[0] = float(self._ui.filterMaxx_edit.text())
            self._model._filterBdBoxMax[1] = float(self._ui.filterMaxy_edit.text())
            self._model._filterBdBoxMax[2] = float(self._ui.filterMaxz_edit.text())
        except Exception as e:
            pass

    @pyqtSlot()
    def _on_anyFilterIntensityThresh_lineEdit_onEditingFinished(self):
        try:
            self._model._filterIntensityMin = float(self._ui.filterMinIntensity_edit.text())
            self._model._filterIntensityMax = float(self._ui.filterMaxIntensity_edit.text())
        except Exception as e:
            pass

    @pyqtSlot()
    def on_anyFilterVelocityThresh_lineEdit_onEditingFinished(self):
        try:
            self._model._filterVelocityMin = float(self._ui.filterMinVelocity_edit.text())
            self._model._filterVelocityMax = float(self._ui.filterMaxVelocity_edit.text())
        except Exception as e:
            pass

    @pyqtSlot()
    def on_addFilter_btn_clicked(self):
        chosenFilter = self._ui.filters_comboBox.currentText()
        if chosenFilter == self._model.filters[0]:
            item = self._model.filters[0] + " filter: "
            item = item + f"min Bound: {self._model._filterBdBoxMin}, "
            item = item + f"max  Bound: {self._model._filterBdBoxMax}"
        elif chosenFilter == self._model.filters[1]:
            item = self._model.filters[1] + " filter: "
            item = item + f"min Thresh: {self._model._filterVelocityMin}, "
            item = item + f"max Thresh: {self._model._filterVelocityMax}"
        elif chosenFilter == self._model.filters[2]:
            item = self._model.filters[2] + " filter: "
            item = item + f"min Thresh: {self._model._filterIntensityMin}, "
            item = item + f"max Thresh: {self._model._filterIntensityMax}"

        self._ui.algorithms_list.addItem(item)

        self.updateFiltersList()

    def updateFiltersList(self):
        indicies = self._ui.algorithms_list.count()
        filtersListStr = []
        for idx in range(indicies):
            item = self._ui.algorithms_list.item(idx)
            filtersListStr.append(item.text())

        self._model._filtersListStr = filtersListStr
    @pyqtSlot()
    def on_removeAlgorithm_btn_clicked(self):
        try:
            names = self._ui.algorithms_list.selectedItems()
            for name in names:
                row = self._ui.algorithms_list.row(name)
                item = self._ui.algorithms_list.takeItem(row)
                del item

            self.updateFiltersList()
        except Exception as e:
            pass

    @pyqtSlot()
    def on_clearAlgorithm_btn_clicked(self):
        self._ui.algorithms_list.clear()
        self.updateFiltersList()

    @pyqtSlot()
    def on_moveDownAlgorithm_btn_clicked(self):
        try:
            currentRow = self._ui.algorithms_list.currentRow()
            currentItem = self._ui.algorithms_list.takeItem(currentRow)
            self._ui.algorithms_list.insertItem(currentRow + 1, currentItem)
            self._ui.algorithms_list.setCurrentRow(currentRow+1)
            self.updateFiltersList()
        except Exception as e:
            pass

    @pyqtSlot()
    def on_moveUpAlgorithm_btn_clicked(self):
        try:
            currentRow = self._ui.algorithms_list.currentRow()
            currentItem = self._ui.algorithms_list.takeItem(currentRow)
            self._ui.algorithms_list.insertItem(currentRow - 1, currentItem)
            self._ui.algorithms_list.setCurrentRow(currentRow - 1)
            self.updateFiltersList()
        except Exception as e:
            pass

    ###################################

    ## helpers' slots ##
    def hideWidgets(self, widgets):
        for w in widgets:
            w.setVisible(False)

    def showWidgets(self, widgets):
        for w in widgets:
            w.setVisible(True)

    def disableWidgets(self, widgets):
        for w in widgets:
            w.setEnabled(False)

    def enableWidgets(self, widgets):
        for w in widgets:
            w.setEnabled(True)
    ###################################