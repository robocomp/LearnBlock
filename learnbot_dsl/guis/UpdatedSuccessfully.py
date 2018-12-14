# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/ivan/robocomp/components/learnbot/learnbot_dsl/learnbotCode/guis/UpdatedSuccessfully.ui'
#
# Created: Thu Oct 25 10:33:07 2018
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Updated(object):
    def setupUi(self, Updated):
        Updated.setObjectName("Updated")
        Updated.resize(378, 81)
        self.horizontalLayout = QtGui.QHBoxLayout(Updated)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtGui.QLabel(Updated)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setLineWidth(1)
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)

        self.retranslateUi(Updated)
        QtCore.QMetaObject.connectSlotsByName(Updated)

    def retranslateUi(self, Updated):
        Updated.setWindowTitle(QtGui.QApplication.translate("Updated", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Updated", "Learnblock has been successfully updated,\n"
"to load the updates close and reopen the program.", None, QtGui.QApplication.UnicodeUTF8))

