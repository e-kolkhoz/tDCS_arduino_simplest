# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_frm.ui'
#
# Created: Tue Jul  4 03:52:25 2017
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(623, 445)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.widget_3 = QtGui.QWidget(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_3.sizePolicy().hasHeightForWidth())
        self.widget_3.setSizePolicy(sizePolicy)
        self.widget_3.setObjectName("widget_3")
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.widget_3)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.btnStart = QtGui.QPushButton(self.widget_3)
        self.btnStart.setObjectName("btnStart")
        self.verticalLayout_4.addWidget(self.btnStart)
        self.verticalLayout_2.addWidget(self.widget_3)
        self.widget_4 = QtGui.QWidget(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_4.sizePolicy().hasHeightForWidth())
        self.widget_4.setSizePolicy(sizePolicy)
        self.widget_4.setMinimumSize(QtCore.QSize(0, 220))
        self.widget_4.setObjectName("widget_4")
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.widget_4)
        self.horizontalLayout_3.setContentsMargins(0, -1, 0, -1)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.lblImg = QtGui.QLabel(self.widget_4)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblImg.sizePolicy().hasHeightForWidth())
        self.lblImg.setSizePolicy(sizePolicy)
        self.lblImg.setMinimumSize(QtCore.QSize(400, 220))
        self.lblImg.setFrameShape(QtGui.QFrame.StyledPanel)
        self.lblImg.setFrameShadow(QtGui.QFrame.Plain)
        self.lblImg.setText("")
        self.lblImg.setObjectName("lblImg")
        self.horizontalLayout_3.addWidget(self.lblImg)
        self.widget_5 = QtGui.QWidget(self.widget_4)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_5.sizePolicy().hasHeightForWidth())
        self.widget_5.setSizePolicy(sizePolicy)
        self.widget_5.setMinimumSize(QtCore.QSize(200, 0))
        self.widget_5.setObjectName("widget_5")
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.widget_5)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.lblTarget_mA = QtGui.QLabel(self.widget_5)
        self.lblTarget_mA.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.lblTarget_mA.setObjectName("lblTarget_mA")
        self.verticalLayout_5.addWidget(self.lblTarget_mA)
        self.lblReal = QtGui.QLabel(self.widget_5)
        self.lblReal.setEnabled(True)
        self.lblReal.setObjectName("lblReal")
        self.verticalLayout_5.addWidget(self.lblReal)
        self.lblVoltage = QtGui.QLabel(self.widget_5)
        self.lblVoltage.setObjectName("lblVoltage")
        self.verticalLayout_5.addWidget(self.lblVoltage)
        self.lblState = QtGui.QLabel(self.widget_5)
        self.lblState.setObjectName("lblState")
        self.verticalLayout_5.addWidget(self.lblState)
        self.lblTime = QtGui.QLabel(self.widget_5)
        self.lblTime.setObjectName("lblTime")
        self.verticalLayout_5.addWidget(self.lblTime)
        self.btnConnect = QtGui.QPushButton(self.widget_5)
        self.btnConnect.setObjectName("btnConnect")
        self.verticalLayout_5.addWidget(self.btnConnect)
        spacerItem = QtGui.QSpacerItem(20, 150, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
        self.verticalLayout_5.addItem(spacerItem)
        self.horizontalLayout_3.addWidget(self.widget_5)
        self.verticalLayout_2.addWidget(self.widget_4)
        self.widget_2 = QtGui.QWidget(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy)
        self.widget_2.setObjectName("widget_2")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.widget_2)
        self.verticalLayout_3.setContentsMargins(0, -1, 0, -1)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.widget = QtGui.QWidget(self.widget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setObjectName("widget")
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lblTarg = QtGui.QLabel(self.widget)
        self.lblTarg.setObjectName("lblTarg")
        self.horizontalLayout_2.addWidget(self.lblTarg)
        self.sliderMcA = QtGui.QSlider(self.widget)
        self.sliderMcA.setMinimum(10)
        self.sliderMcA.setMaximum(1000)
        self.sliderMcA.setSingleStep(10)
        self.sliderMcA.setPageStep(50)
        self.sliderMcA.setProperty("value", 200)
        self.sliderMcA.setSliderPosition(200)
        self.sliderMcA.setOrientation(QtCore.Qt.Horizontal)
        self.sliderMcA.setObjectName("sliderMcA")
        self.horizontalLayout_2.addWidget(self.sliderMcA)
        self.verticalLayout_3.addWidget(self.widget)
        self.tbMain = QtGui.QTextBrowser(self.widget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tbMain.sizePolicy().hasHeightForWidth())
        self.tbMain.setSizePolicy(sizePolicy)
        self.tbMain.setMinimumSize(QtCore.QSize(0, 100))
        self.tbMain.setMaximumSize(QtCore.QSize(16777215, 100))
        self.tbMain.setObjectName("tbMain")
        self.verticalLayout_3.addWidget(self.tbMain)
        self.verticalLayout_2.addWidget(self.widget_2)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.btnStart.setText(QtGui.QApplication.translate("MainWindow", "Start", None, QtGui.QApplication.UnicodeUTF8))
        self.lblTarget_mA.setText(QtGui.QApplication.translate("MainWindow", "Target, mA: 0", None, QtGui.QApplication.UnicodeUTF8))
        self.lblReal.setText(QtGui.QApplication.translate("MainWindow", "Real, mA: 0", None, QtGui.QApplication.UnicodeUTF8))
        self.lblVoltage.setText(QtGui.QApplication.translate("MainWindow", "Voltage, V: 0", None, QtGui.QApplication.UnicodeUTF8))
        self.lblState.setText(QtGui.QApplication.translate("MainWindow", "State: Not Connected", None, QtGui.QApplication.UnicodeUTF8))
        self.lblTime.setText(QtGui.QApplication.translate("MainWindow", "Time: 0", None, QtGui.QApplication.UnicodeUTF8))
        self.btnConnect.setText(QtGui.QApplication.translate("MainWindow", "Connect/Reconnect", None, QtGui.QApplication.UnicodeUTF8))
        self.lblTarg.setText(QtGui.QApplication.translate("MainWindow", "Target, mA", None, QtGui.QApplication.UnicodeUTF8))
        self.tbMain.setHtml(QtGui.QApplication.translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"><br /></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))

