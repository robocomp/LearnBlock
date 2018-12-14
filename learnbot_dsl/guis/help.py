# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/ivan/robocomp/components/learnbot/learnbot_dsl/guis/help.ui'
#
# Created: Tue Nov  6 22:01:10 2018
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Help(object):
    def setupUi(self, Help):
        Help.setObjectName("Help")
        Help.resize(902, 734)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Help.sizePolicy().hasHeightForWidth())
        Help.setSizePolicy(sizePolicy)
        self.horizontalLayout = QtGui.QHBoxLayout(Help)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.splitter = QtGui.QSplitter(Help)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.treeWidget = QtGui.QTreeWidget(self.splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.treeWidget.sizePolicy().hasHeightForWidth())
        self.treeWidget.setSizePolicy(sizePolicy)
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.headerItem().setText(0, "1")
        self.verticalLayoutWidget = QtGui.QWidget(self.splitter)
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.layoutWebKit = QtGui.QVBoxLayout()
        self.layoutWebKit.setObjectName("layoutWebKit")
        self.verticalLayout.addLayout(self.layoutWebKit)
        self.horizontalLayoutButtons = QtGui.QHBoxLayout()
        self.horizontalLayoutButtons.setObjectName("horizontalLayoutButtons")
        self.pushButtonPrevious = QtGui.QPushButton(self.verticalLayoutWidget)
        self.pushButtonPrevious.setObjectName("pushButtonPrevious")
        self.horizontalLayoutButtons.addWidget(self.pushButtonPrevious)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayoutButtons.addItem(spacerItem)
        self.pushButtoNext = QtGui.QPushButton(self.verticalLayoutWidget)
        self.pushButtoNext.setObjectName("pushButtoNext")
        self.horizontalLayoutButtons.addWidget(self.pushButtoNext)
        self.verticalLayout.addLayout(self.horizontalLayoutButtons)
        self.horizontalLayout.addWidget(self.splitter)

        self.retranslateUi(Help)
        QtCore.QMetaObject.connectSlotsByName(Help)

    def retranslateUi(self, Help):
        Help.setWindowTitle(QtGui.QApplication.translate("Help", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonPrevious.setText(QtGui.QApplication.translate("Help", "Previous", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtoNext.setText(QtGui.QApplication.translate("Help", "Next", None, QtGui.QApplication.UnicodeUTF8))

