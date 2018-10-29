# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/ivan/robocomp/components/learnbot/learnbot_dsl/learnbotCode/guis/TabLibrary.ui'
#
# Created: Thu Oct 25 10:33:07 2018
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableLibrary = QtGui.QTableWidget(Form)
        self.tableLibrary.setShowGrid(False)
        self.tableLibrary.setGridStyle(QtCore.Qt.NoPen)
        self.tableLibrary.setObjectName("tableLibrary")
        self.tableLibrary.setColumnCount(0)
        self.tableLibrary.setRowCount(0)
        self.tableLibrary.horizontalHeader().setVisible(False)
        self.tableLibrary.verticalHeader().setVisible(False)
        self.verticalLayout.addWidget(self.tableLibrary)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))

