# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'help.ui',
# licensing of 'help.ui' applies.
#
# Created: Thu Nov  7 19:55:19 2019
#      by: pyside2-uic  running on PySide2 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Help(object):
    def setupUi(self, Help):
        Help.setObjectName("Help")
        Help.resize(902, 734)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Help.sizePolicy().hasHeightForWidth())
        Help.setSizePolicy(sizePolicy)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Help)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.splitter = QtWidgets.QSplitter(Help)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.treeWidget = QtWidgets.QTreeWidget(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.treeWidget.sizePolicy().hasHeightForWidth())
        self.treeWidget.setSizePolicy(sizePolicy)
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.headerItem().setText(0, "Fast guide to LearnBlock")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.splitter)
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.layoutWebKit = QtWidgets.QVBoxLayout()
        self.layoutWebKit.setObjectName("layoutWebKit")
        self.verticalLayout.addLayout(self.layoutWebKit)
        self.horizontalLayoutButtons = QtWidgets.QHBoxLayout()
        self.horizontalLayoutButtons.setObjectName("horizontalLayoutButtons")
        self.pushButtonPrevious = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButtonPrevious.setObjectName("pushButtonPrevious")
        self.horizontalLayoutButtons.addWidget(self.pushButtonPrevious)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayoutButtons.addItem(spacerItem)
        self.pushButtonNext = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButtonNext.setObjectName("pushButtonNext")
        self.horizontalLayoutButtons.addWidget(self.pushButtonNext)
        self.verticalLayout.addLayout(self.horizontalLayoutButtons)
        self.horizontalLayout.addWidget(self.splitter)

        self.retranslateUi(Help)
        QtCore.QMetaObject.connectSlotsByName(Help)

    def retranslateUi(self, Help):
        Help.setWindowTitle(QtWidgets.QApplication.translate("Help", "Help", None, -1))
        self.pushButtonPrevious.setText(QtWidgets.QApplication.translate("Help", "Previous", None, -1))
        self.pushButtonNext.setText(QtWidgets.QApplication.translate("Help", "Next", None, -1))

