# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/ivan/robocomp/components/learnbot/learnbot_dsl/guis/AddNumberOrString.ui',
# licensing of '/home/ivan/robocomp/components/learnbot/learnbot_dsl/guis/AddNumberOrString.ui' applies.
#
# Created: Thu Mar  7 12:39:25 2019
#      by: pyside2-uic  running on PySide2 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(465, 201)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setMinimumSize(QtCore.QSize(102, 27))
        self.label_4.setMaximumSize(QtCore.QSize(102, 27))
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_10.addWidget(self.label_4)
        self.lineEditName = QtWidgets.QLineEdit(Dialog)
        self.lineEditName.setMinimumSize(QtCore.QSize(331, 27))
        self.lineEditName.setMaximumSize(QtCore.QSize(331, 27))
        self.lineEditName.setToolTip("")
        self.lineEditName.setObjectName("lineEditName")
        self.horizontalLayout_10.addWidget(self.lineEditName)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem)
        self.verticalLayout_4.addLayout(self.horizontalLayout_10)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setMinimumSize(QtCore.QSize(102, 27))
        self.label_2.setMaximumSize(QtCore.QSize(102, 27))
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.comboBoxBlockImage = QtWidgets.QComboBox(Dialog)
        self.comboBoxBlockImage.setMaximumSize(QtCore.QSize(110, 27))
        self.comboBoxBlockImage.setToolTip("")
        self.comboBoxBlockImage.setObjectName("comboBoxBlockImage")
        self.horizontalLayout_3.addWidget(self.comboBoxBlockImage)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_5.addLayout(self.verticalLayout)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem1)
        self.BlockImage = QtWidgets.QLabel(Dialog)
        self.BlockImage.setMinimumSize(QtCore.QSize(161, 111))
        self.BlockImage.setText("")
        self.BlockImage.setObjectName("BlockImage")
        self.horizontalLayout_5.addWidget(self.BlockImage)
        self.verticalLayout_4.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem2)
        self.pushButtonCancel = QtWidgets.QPushButton(Dialog)
        self.pushButtonCancel.setMaximumSize(QtCore.QSize(150, 16777215))
        self.pushButtonCancel.setAutoDefault(False)
        self.pushButtonCancel.setObjectName("pushButtonCancel")
        self.horizontalLayout_9.addWidget(self.pushButtonCancel)
        self.pushButtonOK = QtWidgets.QPushButton(Dialog)
        self.pushButtonOK.setMaximumSize(QtCore.QSize(150, 16777215))
        self.pushButtonOK.setObjectName("pushButtonOK")
        self.horizontalLayout_9.addWidget(self.pushButtonOK)
        self.verticalLayout_4.addLayout(self.horizontalLayout_9)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.pushButtonOK, self.lineEditName)
        Dialog.setTabOrder(self.lineEditName, self.comboBoxBlockImage)
        Dialog.setTabOrder(self.comboBoxBlockImage, self.pushButtonCancel)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtWidgets.QApplication.translate("Dialog", "Add Number Or String", None, -1))
        self.label_4.setText(QtWidgets.QApplication.translate("Dialog", "Value", None, -1))
        self.lineEditName.setPlaceholderText(QtWidgets.QApplication.translate("Dialog", "Name Block", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("Dialog", "Block image:", None, -1))
        self.pushButtonCancel.setText(QtWidgets.QApplication.translate("Dialog", "CANCEL", None, -1))
        self.pushButtonOK.setText(QtWidgets.QApplication.translate("Dialog", "OK", None, -1))

