# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/ivan/robocomp/components/learnbot/learnbot_dsl/guis/AddVar.ui',
# licensing of '/home/ivan/robocomp/components/learnbot/learnbot_dsl/guis/AddVar.ui' applies.
#
# Created: Thu Mar  7 12:39:25 2019
#      by: pyside2-uic  running on PySide2 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(300, 89)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.text = QtWidgets.QLabel(Dialog)
        self.text.setObjectName("text")
        self.horizontalLayout_2.addWidget(self.text)
        self.nameLineEdit = QtWidgets.QLineEdit(Dialog)
        self.nameLineEdit.setObjectName("nameLineEdit")
        self.horizontalLayout_2.addWidget(self.nameLineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.cancelPushButton = QtWidgets.QPushButton(Dialog)
        self.cancelPushButton.setAutoDefault(False)
        self.cancelPushButton.setObjectName("cancelPushButton")
        self.horizontalLayout.addWidget(self.cancelPushButton)
        self.okPushButton = QtWidgets.QPushButton(Dialog)
        self.okPushButton.setObjectName("okPushButton")
        self.horizontalLayout.addWidget(self.okPushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtWidgets.QApplication.translate("Dialog", "Add Variable", None, -1))
        self.text.setText(QtWidgets.QApplication.translate("Dialog", "Nombre:", None, -1))
        self.cancelPushButton.setText(QtWidgets.QApplication.translate("Dialog", "Cancel", None, -1))
        self.okPushButton.setText(QtWidgets.QApplication.translate("Dialog", "Ok", None, -1))

