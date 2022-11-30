# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'baseUI_tab.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1066, 628)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        MainWindow.setFont(font)
        MainWindow.setIconSize(QtCore.QSize(100, 100))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.la_logo = QtWidgets.QLabel(self.groupBox)
        self.la_logo.setObjectName("la_logo")
        self.horizontalLayout.addWidget(self.la_logo)
        self.pb_connect = QtWidgets.QPushButton(self.groupBox)
        self.pb_connect.setObjectName("pb_connect")
        self.horizontalLayout.addWidget(self.pb_connect)
        self.verticalLayout.addWidget(self.groupBox)
        self.groupBox_17 = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_17.sizePolicy().hasHeightForWidth())
        self.groupBox_17.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_17.setFont(font)
        self.groupBox_17.setObjectName("groupBox_17")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox_17)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.tabWidget = QtWidgets.QTabWidget(self.groupBox_17)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_10 = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab_10.sizePolicy().hasHeightForWidth())
        self.tab_10.setSizePolicy(sizePolicy)
        self.tab_10.setObjectName("tab_10")
        self.verticalLayout_16 = QtWidgets.QVBoxLayout(self.tab_10)
        self.verticalLayout_16.setObjectName("verticalLayout_16")
        self.groupBox_6 = QtWidgets.QGroupBox(self.tab_10)
        self.groupBox_6.setObjectName("groupBox_6")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_6)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.SM_Laser_ON = QtWidgets.QPushButton(self.groupBox_6)
        self.SM_Laser_ON.setEnabled(False)
        self.SM_Laser_ON.setObjectName("SM_Laser_ON")
        self.gridLayout_2.addWidget(self.SM_Laser_ON, 1, 1, 1, 1)
        self.SM_init = QtWidgets.QPushButton(self.groupBox_6)
        self.SM_init.setEnabled(False)
        self.SM_init.setObjectName("SM_init")
        self.gridLayout_2.addWidget(self.SM_init, 0, 1, 1, 1)
        self.SM_start = QtWidgets.QPushButton(self.groupBox_6)
        self.SM_start.setObjectName("SM_start")
        self.gridLayout_2.addWidget(self.SM_start, 0, 0, 1, 1)
        self.SM_stop = QtWidgets.QPushButton(self.groupBox_6)
        self.SM_stop.setEnabled(True)
        self.SM_stop.setObjectName("SM_stop")
        self.gridLayout_2.addWidget(self.SM_stop, 0, 2, 1, 1)
        self.verticalLayout_16.addWidget(self.groupBox_6)
        self.groupBox_8 = QtWidgets.QGroupBox(self.tab_10)
        self.groupBox_8.setObjectName("groupBox_8")
        self.verticalLayout_16.addWidget(self.groupBox_8)
        self.tabWidget.addTab(self.tab_10, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.tab_4)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.groupBox_19 = QtWidgets.QGroupBox(self.tab_4)
        self.groupBox_19.setTitle("")
        self.groupBox_19.setObjectName("groupBox_19")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.groupBox_19)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.groupBox_16 = QtWidgets.QGroupBox(self.groupBox_19)
        self.groupBox_16.setTitle("")
        self.groupBox_16.setObjectName("groupBox_16")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.groupBox_16)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.label_3 = QtWidgets.QLabel(self.groupBox_16)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_7.addWidget(self.label_3)
        self.le_temp = QtWidgets.QLineEdit(self.groupBox_16)
        self.le_temp.setEnabled(False)
        self.le_temp.setObjectName("le_temp")
        self.verticalLayout_7.addWidget(self.le_temp)
        self.pb_save = QtWidgets.QPushButton(self.groupBox_16)
        self.pb_save.setObjectName("pb_save")
        self.verticalLayout_7.addWidget(self.pb_save)
        self.gridLayout_6.addWidget(self.groupBox_16, 0, 1, 1, 1)
        self.groupBox_20 = QtWidgets.QGroupBox(self.groupBox_19)
        self.groupBox_20.setTitle("")
        self.groupBox_20.setObjectName("groupBox_20")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.groupBox_20)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.label_8 = QtWidgets.QLabel(self.groupBox_20)
        self.label_8.setObjectName("label_8")
        self.gridLayout_8.addWidget(self.label_8, 0, 0, 1, 1)
        self.pb_lsren = QtWidgets.QPushButton(self.groupBox_20)
        self.pb_lsren.setObjectName("pb_lsren")
        self.gridLayout_8.addWidget(self.pb_lsren, 1, 1, 1, 1)
        self.cb_tempsource = QtWidgets.QComboBox(self.groupBox_20)
        self.cb_tempsource.setObjectName("cb_tempsource")
        self.cb_tempsource.addItem("")
        self.cb_tempsource.addItem("")
        self.cb_tempsource.addItem("")
        self.cb_tempsource.addItem("")
        self.cb_tempsource.addItem("")
        self.cb_tempsource.addItem("")
        self.cb_tempsource.addItem("")
        self.cb_tempsource.addItem("")
        self.cb_tempsource.addItem("")
        self.gridLayout_8.addWidget(self.cb_tempsource, 0, 1, 1, 1)
        self.pb_interlock = QtWidgets.QPushButton(self.groupBox_20)
        self.pb_interlock.setObjectName("pb_interlock")
        self.gridLayout_8.addWidget(self.pb_interlock, 1, 0, 1, 1)
        self.label_37 = QtWidgets.QLabel(self.groupBox_20)
        self.label_37.setObjectName("label_37")
        self.gridLayout_8.addWidget(self.label_37, 2, 0, 1, 1)
        self.le_pixcount = QtWidgets.QLineEdit(self.groupBox_20)
        self.le_pixcount.setObjectName("le_pixcount")
        self.gridLayout_8.addWidget(self.le_pixcount, 2, 1, 1, 1)
        self.gridLayout_6.addWidget(self.groupBox_20, 0, 0, 1, 1)
        self.verticalLayout_3.addWidget(self.groupBox_19)
        self.tabWidget.addTab(self.tab_4, "")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout(self.tab_5)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.groupBox_23 = QtWidgets.QGroupBox(self.tab_5)
        self.groupBox_23.setTitle("")
        self.groupBox_23.setObjectName("groupBox_23")
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout(self.groupBox_23)
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.cb_ChirpMan = QtWidgets.QCheckBox(self.groupBox_23)
        self.cb_ChirpMan.setObjectName("cb_ChirpMan")
        self.horizontalLayout_12.addWidget(self.cb_ChirpMan)
        self.cb_ENFFT = QtWidgets.QCheckBox(self.groupBox_23)
        self.cb_ENFFT.setObjectName("cb_ENFFT")
        self.horizontalLayout_12.addWidget(self.cb_ENFFT)
        self.cb_LSRMan = QtWidgets.QCheckBox(self.groupBox_23)
        self.cb_LSRMan.setObjectName("cb_LSRMan")
        self.horizontalLayout_12.addWidget(self.cb_LSRMan)
        self.cb_ChirpSim = QtWidgets.QCheckBox(self.groupBox_23)
        self.cb_ChirpSim.setObjectName("cb_ChirpSim")
        self.horizontalLayout_12.addWidget(self.cb_ChirpSim)
        self.cb_laser = QtWidgets.QCheckBox(self.groupBox_23)
        self.cb_laser.setObjectName("cb_laser")
        self.horizontalLayout_12.addWidget(self.cb_laser)
        self.cb_start = QtWidgets.QCheckBox(self.groupBox_23)
        self.cb_start.setObjectName("cb_start")
        self.horizontalLayout_12.addWidget(self.cb_start)
        self.pb_start = QtWidgets.QPushButton(self.groupBox_23)
        self.pb_start.setObjectName("pb_start")
        self.horizontalLayout_12.addWidget(self.pb_start)
        self.verticalLayout_12.addWidget(self.groupBox_23)
        self.groupBox_42 = QtWidgets.QGroupBox(self.tab_5)
        self.groupBox_42.setTitle("")
        self.groupBox_42.setObjectName("groupBox_42")
        self.horizontalLayout_22 = QtWidgets.QHBoxLayout(self.groupBox_42)
        self.horizontalLayout_22.setObjectName("horizontalLayout_22")
        self.groupBox_43 = QtWidgets.QGroupBox(self.groupBox_42)
        self.groupBox_43.setTitle("")
        self.groupBox_43.setObjectName("groupBox_43")
        self.horizontalLayout_23 = QtWidgets.QHBoxLayout(self.groupBox_43)
        self.horizontalLayout_23.setObjectName("horizontalLayout_23")
        self.label_46 = QtWidgets.QLabel(self.groupBox_43)
        self.label_46.setObjectName("label_46")
        self.horizontalLayout_23.addWidget(self.label_46)
        self.le_chirpsource = QtWidgets.QLineEdit(self.groupBox_43)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.le_chirpsource.sizePolicy().hasHeightForWidth())
        self.le_chirpsource.setSizePolicy(sizePolicy)
        self.le_chirpsource.setObjectName("le_chirpsource")
        self.horizontalLayout_23.addWidget(self.le_chirpsource)
        self.pb_AcquireData = QtWidgets.QPushButton(self.groupBox_43)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pb_AcquireData.sizePolicy().hasHeightForWidth())
        self.pb_AcquireData.setSizePolicy(sizePolicy)
        self.pb_AcquireData.setObjectName("pb_AcquireData")
        self.horizontalLayout_23.addWidget(self.pb_AcquireData)
        self.horizontalLayout_22.addWidget(self.groupBox_43)
        self.verticalLayout_12.addWidget(self.groupBox_42)
        self.groupBox_37 = QtWidgets.QGroupBox(self.tab_5)
        self.groupBox_37.setTitle("")
        self.groupBox_37.setObjectName("groupBox_37")
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout(self.groupBox_37)
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.cb_DEBA = QtWidgets.QCheckBox(self.groupBox_37)
        self.cb_DEBA.setObjectName("cb_DEBA")
        self.horizontalLayout_14.addWidget(self.cb_DEBA)
        self.cb_DEBB = QtWidgets.QCheckBox(self.groupBox_37)
        self.cb_DEBB.setObjectName("cb_DEBB")
        self.horizontalLayout_14.addWidget(self.cb_DEBB)
        self.cb_ENFFTEdge = QtWidgets.QCheckBox(self.groupBox_37)
        self.cb_ENFFTEdge.setObjectName("cb_ENFFTEdge")
        self.horizontalLayout_14.addWidget(self.cb_ENFFTEdge)
        self.cb_DoTrig = QtWidgets.QCheckBox(self.groupBox_37)
        self.cb_DoTrig.setObjectName("cb_DoTrig")
        self.horizontalLayout_14.addWidget(self.cb_DoTrig)
        self.verticalLayout_12.addWidget(self.groupBox_37)
        self.tabWidget.addTab(self.tab_5, "")
        self.tab_8 = QtWidgets.QWidget()
        self.tab_8.setObjectName("tab_8")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.tab_8)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.groupBox_27 = QtWidgets.QGroupBox(self.tab_8)
        self.groupBox_27.setTitle("")
        self.groupBox_27.setObjectName("groupBox_27")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBox_27)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.temp_matrix = QtWidgets.QTableWidget(self.groupBox_27)
        self.temp_matrix.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.temp_matrix.sizePolicy().hasHeightForWidth())
        self.temp_matrix.setSizePolicy(sizePolicy)
        self.temp_matrix.setLineWidth(1)
        self.temp_matrix.setRowCount(8)
        self.temp_matrix.setColumnCount(1)
        self.temp_matrix.setObjectName("temp_matrix")
        item = QtWidgets.QTableWidgetItem()
        self.temp_matrix.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.temp_matrix.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.temp_matrix.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.temp_matrix.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.temp_matrix.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.temp_matrix.setVerticalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.temp_matrix.setVerticalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.temp_matrix.setVerticalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.temp_matrix.setHorizontalHeaderItem(0, item)
        self.temp_matrix.horizontalHeader().setVisible(False)
        self.horizontalLayout_2.addWidget(self.temp_matrix)
        self.groupBox_2 = QtWidgets.QGroupBox(self.groupBox_27)
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2.addWidget(self.groupBox_2)
        self.verticalLayout_9.addWidget(self.groupBox_27)
        self.tabWidget.addTab(self.tab_8, "")
        self.tab_9 = QtWidgets.QWidget()
        self.tab_9.setObjectName("tab_9")
        self.verticalLayout_15 = QtWidgets.QVBoxLayout(self.tab_9)
        self.verticalLayout_15.setObjectName("verticalLayout_15")
        self.groupBox_38 = QtWidgets.QGroupBox(self.tab_9)
        self.groupBox_38.setObjectName("groupBox_38")
        self.verticalLayout_19 = QtWidgets.QVBoxLayout(self.groupBox_38)
        self.verticalLayout_19.setObjectName("verticalLayout_19")
        self.groupBox_47 = QtWidgets.QGroupBox(self.groupBox_38)
        self.groupBox_47.setObjectName("groupBox_47")
        self.horizontalLayout_28 = QtWidgets.QHBoxLayout(self.groupBox_47)
        self.horizontalLayout_28.setObjectName("horizontalLayout_28")
        self.groupBox_49 = QtWidgets.QGroupBox(self.groupBox_47)
        self.groupBox_49.setObjectName("groupBox_49")
        self.verticalLayout_22 = QtWidgets.QVBoxLayout(self.groupBox_49)
        self.verticalLayout_22.setObjectName("verticalLayout_22")
        self.pb_send_voltage = QtWidgets.QPushButton(self.groupBox_49)
        self.pb_send_voltage.setObjectName("pb_send_voltage")
        self.verticalLayout_22.addWidget(self.pb_send_voltage)
        self.pb_cb_0 = QtWidgets.QCheckBox(self.groupBox_49)
        self.pb_cb_0.setEnabled(False)
        self.pb_cb_0.setChecked(True)
        self.pb_cb_0.setObjectName("pb_cb_0")
        self.verticalLayout_22.addWidget(self.pb_cb_0)
        self.pb_cb_1 = QtWidgets.QCheckBox(self.groupBox_49)
        self.pb_cb_1.setEnabled(False)
        self.pb_cb_1.setMouseTracking(True)
        self.pb_cb_1.setTabletTracking(False)
        self.pb_cb_1.setAutoFillBackground(False)
        self.pb_cb_1.setChecked(True)
        self.pb_cb_1.setObjectName("pb_cb_1")
        self.verticalLayout_22.addWidget(self.pb_cb_1)
        self.pb_cb_2 = QtWidgets.QCheckBox(self.groupBox_49)
        self.pb_cb_2.setObjectName("pb_cb_2")
        self.verticalLayout_22.addWidget(self.pb_cb_2)
        self.pb_cb_3 = QtWidgets.QCheckBox(self.groupBox_49)
        self.pb_cb_3.setObjectName("pb_cb_3")
        self.verticalLayout_22.addWidget(self.pb_cb_3)
        self.pb_cb_4 = QtWidgets.QCheckBox(self.groupBox_49)
        self.pb_cb_4.setObjectName("pb_cb_4")
        self.verticalLayout_22.addWidget(self.pb_cb_4)
        self.pb_cb_5 = QtWidgets.QCheckBox(self.groupBox_49)
        self.pb_cb_5.setObjectName("pb_cb_5")
        self.verticalLayout_22.addWidget(self.pb_cb_5)
        self.pb_cb_6 = QtWidgets.QCheckBox(self.groupBox_49)
        self.pb_cb_6.setObjectName("pb_cb_6")
        self.verticalLayout_22.addWidget(self.pb_cb_6)
        self.pb_cb_7 = QtWidgets.QCheckBox(self.groupBox_49)
        self.pb_cb_7.setObjectName("pb_cb_7")
        self.verticalLayout_22.addWidget(self.pb_cb_7)
        self.horizontalLayout_28.addWidget(self.groupBox_49)
        self.groupBox_50 = QtWidgets.QGroupBox(self.groupBox_47)
        self.groupBox_50.setObjectName("groupBox_50")
        self.verticalLayout_21 = QtWidgets.QVBoxLayout(self.groupBox_50)
        self.verticalLayout_21.setObjectName("verticalLayout_21")
        self.pb_cb_0_st = QtWidgets.QCheckBox(self.groupBox_50)
        self.pb_cb_0_st.setEnabled(False)
        self.pb_cb_0_st.setObjectName("pb_cb_0_st")
        self.verticalLayout_21.addWidget(self.pb_cb_0_st)
        self.pb_cb_1_st = QtWidgets.QCheckBox(self.groupBox_50)
        self.pb_cb_1_st.setEnabled(False)
        self.pb_cb_1_st.setObjectName("pb_cb_1_st")
        self.verticalLayout_21.addWidget(self.pb_cb_1_st)
        self.pb_cb_2_st = QtWidgets.QCheckBox(self.groupBox_50)
        self.pb_cb_2_st.setEnabled(False)
        self.pb_cb_2_st.setObjectName("pb_cb_2_st")
        self.verticalLayout_21.addWidget(self.pb_cb_2_st)
        self.pb_cb_3_st = QtWidgets.QCheckBox(self.groupBox_50)
        self.pb_cb_3_st.setEnabled(False)
        self.pb_cb_3_st.setObjectName("pb_cb_3_st")
        self.verticalLayout_21.addWidget(self.pb_cb_3_st)
        self.pb_cb_4_st = QtWidgets.QCheckBox(self.groupBox_50)
        self.pb_cb_4_st.setEnabled(False)
        self.pb_cb_4_st.setObjectName("pb_cb_4_st")
        self.verticalLayout_21.addWidget(self.pb_cb_4_st)
        self.pb_cb_5_st = QtWidgets.QCheckBox(self.groupBox_50)
        self.pb_cb_5_st.setEnabled(False)
        self.pb_cb_5_st.setObjectName("pb_cb_5_st")
        self.verticalLayout_21.addWidget(self.pb_cb_5_st)
        self.pb_cb_6_st = QtWidgets.QCheckBox(self.groupBox_50)
        self.pb_cb_6_st.setEnabled(False)
        self.pb_cb_6_st.setObjectName("pb_cb_6_st")
        self.verticalLayout_21.addWidget(self.pb_cb_6_st)
        self.pb_cb_7_st = QtWidgets.QCheckBox(self.groupBox_50)
        self.pb_cb_7_st.setEnabled(False)
        self.pb_cb_7_st.setObjectName("pb_cb_7_st")
        self.verticalLayout_21.addWidget(self.pb_cb_7_st)
        self.horizontalLayout_28.addWidget(self.groupBox_50)
        self.groupBox_48 = QtWidgets.QGroupBox(self.groupBox_47)
        self.groupBox_48.setObjectName("groupBox_48")
        self.pb_slider = QtWidgets.QSlider(self.groupBox_48)
        self.pb_slider.setGeometry(QtCore.QRect(10, 40, 191, 20))
        self.pb_slider.setOrientation(QtCore.Qt.Horizontal)
        self.pb_slider.setObjectName("pb_slider")
        self.pb_fan_speed = QtWidgets.QLabel(self.groupBox_48)
        self.pb_fan_speed.setGeometry(QtCore.QRect(10, 80, 121, 31))
        self.pb_fan_speed.setObjectName("pb_fan_speed")
        self.pb_temperature = QtWidgets.QLabel(self.groupBox_48)
        self.pb_temperature.setGeometry(QtCore.QRect(10, 129, 111, 31))
        self.pb_temperature.setObjectName("pb_temperature")
        self.label_47 = QtWidgets.QLabel(self.groupBox_48)
        self.label_47.setGeometry(QtCore.QRect(146, 80, 141, 31))
        self.label_47.setObjectName("label_47")
        self.label_48 = QtWidgets.QLabel(self.groupBox_48)
        self.label_48.setGeometry(QtCore.QRect(156, 129, 131, 31))
        self.label_48.setObjectName("label_48")
        self.horizontalLayout_28.addWidget(self.groupBox_48)
        self.verticalLayout_19.addWidget(self.groupBox_47)
        self.verticalLayout_15.addWidget(self.groupBox_38)
        self.tabWidget.addTab(self.tab_9, "")
        self.tab_11 = QtWidgets.QWidget()
        self.tab_11.setObjectName("tab_11")
        self.horizontalLayout_29 = QtWidgets.QHBoxLayout(self.tab_11)
        self.horizontalLayout_29.setObjectName("horizontalLayout_29")
        self.VisWidget = QtWidgets.QWidget(self.tab_11)
        self.VisWidget.setObjectName("VisWidget")
        self.horizontalLayout_30 = QtWidgets.QHBoxLayout(self.VisWidget)
        self.horizontalLayout_30.setObjectName("horizontalLayout_30")
        self.VisWidget_2 = QtWidgets.QWidget(self.VisWidget)
        self.VisWidget_2.setObjectName("VisWidget_2")
        self.horizontalLayout_30.addWidget(self.VisWidget_2)
        self.horizontalLayout_29.addWidget(self.VisWidget)
        self.tabWidget.addTab(self.tab_11, "")
        self.tab_12 = QtWidgets.QWidget()
        self.tab_12.setObjectName("tab_12")
        self.verticalLayout_18 = QtWidgets.QVBoxLayout(self.tab_12)
        self.verticalLayout_18.setObjectName("verticalLayout_18")
        self.groupBox_45 = QtWidgets.QGroupBox(self.tab_12)
        self.groupBox_45.setObjectName("groupBox_45")
        self.verticalLayout_18.addWidget(self.groupBox_45)
        self.groupBox_41 = QtWidgets.QGroupBox(self.tab_12)
        self.groupBox_41.setObjectName("groupBox_41")
        self.gridLayout_10 = QtWidgets.QGridLayout(self.groupBox_41)
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.cb_range = QtWidgets.QComboBox(self.groupBox_41)
        self.cb_range.setObjectName("cb_range")
        self.cb_range.addItem("")
        self.cb_range.addItem("")
        self.cb_range.addItem("")
        self.gridLayout_10.addWidget(self.cb_range, 0, 0, 1, 1)
        self.pb_imageupdate = QtWidgets.QPushButton(self.groupBox_41)
        self.pb_imageupdate.setObjectName("pb_imageupdate")
        self.gridLayout_10.addWidget(self.pb_imageupdate, 1, 1, 1, 1)
        self.cb_intensity = QtWidgets.QComboBox(self.groupBox_41)
        self.cb_intensity.setObjectName("cb_intensity")
        self.cb_intensity.addItem("")
        self.cb_intensity.addItem("")
        self.cb_intensity.addItem("")
        self.gridLayout_10.addWidget(self.cb_intensity, 2, 0, 1, 1)
        self.cb_doppler = QtWidgets.QComboBox(self.groupBox_41)
        self.cb_doppler.setObjectName("cb_doppler")
        self.cb_doppler.addItem("")
        self.gridLayout_10.addWidget(self.cb_doppler, 1, 0, 1, 1)
        self.pb_viswindow = QtWidgets.QPushButton(self.groupBox_41)
        self.pb_viswindow.setObjectName("pb_viswindow")
        self.gridLayout_10.addWidget(self.pb_viswindow, 1, 2, 1, 1)
        self.verticalLayout_18.addWidget(self.groupBox_41)
        self.tabWidget.addTab(self.tab_12, "")
        self.verticalLayout_4.addWidget(self.tabWidget)
        self.verticalLayout.addWidget(self.groupBox_17)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1066, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(5)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Scan-IT"))
        self.groupBox.setTitle(_translate("MainWindow", "Enviornment"))
        self.la_logo.setText(_translate("MainWindow", "TextLabel"))
        self.pb_connect.setText(_translate("MainWindow", "Connect"))
        self.groupBox_17.setTitle(_translate("MainWindow", "Calibration Parameters"))
        self.groupBox_6.setTitle(_translate("MainWindow", "STATE"))
        self.SM_Laser_ON.setText(_translate("MainWindow", "LASER ON "))
        self.SM_init.setText(_translate("MainWindow", "INIT"))
        self.SM_start.setText(_translate("MainWindow", "START"))
        self.SM_stop.setText(_translate("MainWindow", "STOP"))
        self.groupBox_8.setTitle(_translate("MainWindow", "STATUS"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_10), _translate("MainWindow", "State Machine"))
        self.label_3.setText(_translate("MainWindow", "Temparature (°C):"))
        self.pb_save.setText(_translate("MainWindow", "Save Temperature"))
        self.label_8.setText(_translate("MainWindow", "Temparature Source"))
        self.pb_lsren.setText(_translate("MainWindow", "Laser Enable"))
        self.cb_tempsource.setItemText(0, _translate("MainWindow", "NTC_NW"))
        self.cb_tempsource.setItemText(1, _translate("MainWindow", "NTC_NE"))
        self.cb_tempsource.setItemText(2, _translate("MainWindow", "NTC_SW"))
        self.cb_tempsource.setItemText(3, _translate("MainWindow", "NTC_SE"))
        self.cb_tempsource.setItemText(4, _translate("MainWindow", "NTC_HotPlate"))
        self.cb_tempsource.setItemText(5, _translate("MainWindow", "NTC_Main"))
        self.cb_tempsource.setItemText(6, _translate("MainWindow", "NTC_ColdPlate"))
        self.cb_tempsource.setItemText(7, _translate("MainWindow", "NTC_ND"))
        self.cb_tempsource.setItemText(8, _translate("MainWindow", "NTC_SD"))
        self.pb_interlock.setText(_translate("MainWindow", "InterlockSummary"))
        self.label_37.setText(_translate("MainWindow", "Pix Count"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("MainWindow", "Temparature"))
        self.cb_ChirpMan.setText(_translate("MainWindow", "ChirpManual"))
        self.cb_ENFFT.setText(_translate("MainWindow", "EN_FFT"))
        self.cb_LSRMan.setText(_translate("MainWindow", "Laser_Manual"))
        self.cb_ChirpSim.setText(_translate("MainWindow", "Chirp_Sim_EN"))
        self.cb_laser.setText(_translate("MainWindow", "LASER ON"))
        self.cb_start.setText(_translate("MainWindow", "START"))
        self.pb_start.setText(_translate("MainWindow", "Send"))
        self.label_46.setText(_translate("MainWindow", "Select Chirp Source"))
        self.pb_AcquireData.setText(_translate("MainWindow", "Acquire Data"))
        self.cb_DEBA.setText(_translate("MainWindow", "Galvo_Static"))
        self.cb_DEBB.setText(_translate("MainWindow", "Scan_Static"))
        self.cb_ENFFTEdge.setText(_translate("MainWindow", "EN_FFT_Edge"))
        self.cb_DoTrig.setText(_translate("MainWindow", "Do_Trigger"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), _translate("MainWindow", "LASER"))
        self.temp_matrix.setSortingEnabled(False)
        item = self.temp_matrix.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "NW"))
        item = self.temp_matrix.verticalHeaderItem(1)
        item.setText(_translate("MainWindow", "NE"))
        item = self.temp_matrix.verticalHeaderItem(2)
        item.setText(_translate("MainWindow", "SW"))
        item = self.temp_matrix.verticalHeaderItem(3)
        item.setText(_translate("MainWindow", "SE"))
        item = self.temp_matrix.verticalHeaderItem(4)
        item.setText(_translate("MainWindow", "Chip"))
        item = self.temp_matrix.verticalHeaderItem(5)
        item.setText(_translate("MainWindow", "Cold Plate"))
        item = self.temp_matrix.verticalHeaderItem(6)
        item.setText(_translate("MainWindow", "North Drv"))
        item = self.temp_matrix.verticalHeaderItem(7)
        item.setText(_translate("MainWindow", "South Drv"))
        item = self.temp_matrix.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Deg C"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_8), _translate("MainWindow", "Driver"))
        self.groupBox_38.setTitle(_translate("MainWindow", "Power Board"))
        self.groupBox_47.setTitle(_translate("MainWindow", "Check"))
        self.groupBox_49.setTitle(_translate("MainWindow", "PWR Enable"))
        self.pb_send_voltage.setText(_translate("MainWindow", "SEND VOLTAGE"))
        self.pb_cb_0.setText(_translate("MainWindow", "bit0_EN_5V"))
        self.pb_cb_1.setText(_translate("MainWindow", "bit1_EN_PC"))
        self.pb_cb_2.setText(_translate("MainWindow", "bit2_EN_12V"))
        self.pb_cb_3.setText(_translate("MainWindow", "bit3_EN_24V"))
        self.pb_cb_4.setText(_translate("MainWindow", "bit4_EN_GALVO"))
        self.pb_cb_5.setText(_translate("MainWindow", "bit5_EN_34V"))
        self.pb_cb_6.setText(_translate("MainWindow", "bit6_IO_RD6"))
        self.pb_cb_7.setText(_translate("MainWindow", "bit7_IO_RD7"))
        self.groupBox_50.setTitle(_translate("MainWindow", "STATUS (READ ONLY) "))
        self.pb_cb_0_st.setText(_translate("MainWindow", "bit0_BUTTON"))
        self.pb_cb_1_st.setText(_translate("MainWindow", "bit1_STATUS12V"))
        self.pb_cb_2_st.setText(_translate("MainWindow", "bit2_RB2"))
        self.pb_cb_3_st.setText(_translate("MainWindow", "bit3_LED2"))
        self.pb_cb_4_st.setText(_translate("MainWindow", "bit4_LED1"))
        self.pb_cb_5_st.setText(_translate("MainWindow", "bit5_STATUS_PC"))
        self.pb_cb_6_st.setText(_translate("MainWindow", "bit6_RB6"))
        self.pb_cb_7_st.setText(_translate("MainWindow", "bit7_RB7"))
        self.groupBox_48.setTitle(_translate("MainWindow", "Fan and Temperature"))
        self.pb_fan_speed.setText(_translate("MainWindow", "Fan speed"))
        self.pb_temperature.setText(_translate("MainWindow", "Temperature"))
        self.label_47.setText(_translate("MainWindow", "__  /__"))
        self.label_48.setText(_translate("MainWindow", "__  /__"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_9), _translate("MainWindow", "PowerBoard"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_11), _translate("MainWindow", "DSP"))
        self.groupBox_45.setTitle(_translate("MainWindow", "GroupBox"))
        self.groupBox_41.setTitle(_translate("MainWindow", "Visualization"))
        self.cb_range.setItemText(0, _translate("MainWindow", "Range"))
        self.cb_range.setItemText(1, _translate("MainWindow", "Range Up Chirp"))
        self.cb_range.setItemText(2, _translate("MainWindow", "Range DownChirp"))
        self.pb_imageupdate.setText(_translate("MainWindow", "Update"))
        self.cb_intensity.setItemText(0, _translate("MainWindow", "Intensity"))
        self.cb_intensity.setItemText(1, _translate("MainWindow", "Intensity Up"))
        self.cb_intensity.setItemText(2, _translate("MainWindow", "Intensity Down"))
        self.cb_doppler.setItemText(0, _translate("MainWindow", "Doppler"))
        self.pb_viswindow.setText(_translate("MainWindow", "VisWindow"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_12), _translate("MainWindow", "Setting"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
