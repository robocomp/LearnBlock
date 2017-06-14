# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/mainUI.ui'
#
# Created: Wed Mar 11 13:13:42 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_guiDlg(object):
    def setupUi(self, guiDlg):
        guiDlg.setObjectName("guiDlg")
        guiDlg.resize(832, 292)
        self.graphicsViewCamera = QtGui.QGraphicsView(guiDlg)
        self.graphicsViewCamera.setGeometry(QtCore.QRect(10, 20, 320, 240))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphicsViewCamera.sizePolicy().hasHeightForWidth())
        self.graphicsViewCamera.setSizePolicy(sizePolicy)
        self.graphicsViewCamera.setProperty("cursor", QtCore.Qt.ArrowCursor)
        self.graphicsViewCamera.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.graphicsViewCamera.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.graphicsViewCamera.setObjectName("graphicsViewCamera")
        self.graphicsViewUltrasound = QtGui.QGraphicsView(guiDlg)
        self.graphicsViewUltrasound.setGeometry(QtCore.QRect(350, 20, 221, 240))
        self.graphicsViewUltrasound.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.graphicsViewUltrasound.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.graphicsViewUltrasound.setObjectName("graphicsViewUltrasound")
        self.graphicsViewJoyStick = QtGui.QGraphicsView(guiDlg)
        self.graphicsViewJoyStick.setGeometry(QtCore.QRect(590, 20, 221, 241))
        self.graphicsViewJoyStick.setProperty("cursor", QtCore.Qt.CrossCursor)
        self.graphicsViewJoyStick.setMouseTracking(True)
        self.graphicsViewJoyStick.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.graphicsViewJoyStick.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.graphicsViewJoyStick.setObjectName("graphicsViewJoyStick")

        self.retranslateUi(guiDlg)
        QtCore.QMetaObject.connectSlotsByName(guiDlg)

    def retranslateUi(self, guiDlg):
        guiDlg.setWindowTitle(QtGui.QApplication.translate("guiDlg", "displaybot", None, QtGui.QApplication.UnicodeUTF8))

