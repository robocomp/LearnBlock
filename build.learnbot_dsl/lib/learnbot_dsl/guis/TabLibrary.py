# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/ivan/robocomp/components/learnbot/learnbot_dsl/guis/TabLibrary.ui',
# licensing of '/home/ivan/robocomp/components/learnbot/learnbot_dsl/guis/TabLibrary.ui' applies.
#
# Created: Thu Mar  7 12:39:25 2019
#      by: pyside2-uic  running on PySide2 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableLibrary = QtWidgets.QTableWidget(Form)
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
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Form", None, -1))

