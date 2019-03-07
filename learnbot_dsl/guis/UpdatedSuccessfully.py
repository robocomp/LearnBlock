# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/ivan/robocomp/components/learnbot/learnbot_dsl/guis/UpdatedSuccessfully.ui',
# licensing of '/home/ivan/robocomp/components/learnbot/learnbot_dsl/guis/UpdatedSuccessfully.ui' applies.
#
# Created: Thu Mar  7 12:39:24 2019
#      by: pyside2-uic  running on PySide2 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Updated(object):
    def setupUi(self, Updated):
        Updated.setObjectName("Updated")
        Updated.resize(378, 81)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Updated)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Updated)
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
        Updated.setWindowTitle(QtWidgets.QApplication.translate("Updated", "Dialog", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("Updated", "Learnblock has been successfully updated,\n"
"to load the updates close and reopen the program.", None, -1))

