# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/ivan/robocomp/components/learnbot/learnbot_dsl/learnbotCode/guis/addVar.ui'
#
# Created: Sun Aug 27 22:27:00 2017
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(300, 89)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.text = QtGui.QLabel(Dialog)
        self.text.setObjectName("text")
        self.horizontalLayout_2.addWidget(self.text)
        self.nameLineEdit = QtGui.QLineEdit(Dialog)
        self.nameLineEdit.setObjectName("nameLineEdit")
        self.horizontalLayout_2.addWidget(self.nameLineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.cancelPushButton = QtGui.QPushButton(Dialog)
        self.cancelPushButton.setAutoDefault(False)
        self.cancelPushButton.setObjectName("cancelPushButton")
        self.horizontalLayout.addWidget(self.cancelPushButton)
        self.okPushButton = QtGui.QPushButton(Dialog)
        self.okPushButton.setObjectName("okPushButton")
        self.horizontalLayout.addWidget(self.okPushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.text.setText(QtGui.QApplication.translate("Dialog", "Nombre:", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelPushButton.setText(QtGui.QApplication.translate("Dialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.okPushButton.setText(QtGui.QApplication.translate("Dialog", "Ok", None, QtGui.QApplication.UnicodeUTF8))

