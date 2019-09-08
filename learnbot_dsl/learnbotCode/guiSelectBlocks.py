from __future__ import print_function, absolute_import
import os, tempfile, json, sys
from PySide2 import QtGui, QtWidgets, QtCore, Qt
import learnbot_dsl.guis.CreateBlock as CreateBlock
from learnbot_dsl.blocksConfig.blocks import pathBlocks
from learnbot_dsl.blocksConfig.parserConfigBlock import pathConfig
from learnbot_dsl.learnbotCode.Block import *
from learnbot_dsl.learnbotCode.toQImage import *


class guiSelectBlocks(QtWidgets.QDialog):

    def __init__(self, blockLists, action):
        self.selectionAction = action
        QtWidgets.QDialog.__init__(self)
        self.setWindowTitle(self.tr('Select visible blocks'))
        self.createTabWidget(blockLists)
        self.createButtons()
        self.createLayout()

    def createTabWidget(self, blockLists):	
        self.tabWidget = QtWidgets.QTabWidget()
        self.lists = []
        for key in blockLists.keys():
            bList = QtWidgets.QListWidget()
            self.lists.append(bList)
            self.createListView(bList, blockLists[key])
            self.tabWidget.addTab(bList, key)


    def createListView(self, bList, blockList):
        for i in range(len(blockList)):
            bList.addItem(blockList[i][0])
            item = bList.item(i)
            item.setFlags(item.flags() or Qt.ItemIsUserCheckable)
            if blockList[i][1]:
                item.setCheckState(QtCore.Qt.Checked)
            else:
                item.setCheckState(QtCore.Qt.Unchecked)

    def createButtons(self):
        self.viewBox = QtWidgets.QGroupBox()
        self.buttonBox = QtWidgets.QDialogButtonBox()
        self.okButton = self.buttonBox.addButton(QtWidgets.QDialogButtonBox.Ok)
        self.cancelButton = self.buttonBox.addButton(QtWidgets.QDialogButtonBox.Cancel)
        self.cancelButton.clicked.connect(self.close)
        self.okButton.clicked.connect(self.selectionAction)

    def createLayout(self):
        self.viewLayout = QtWidgets.QVBoxLayout()
        self.viewLayout.addWidget(self.tabWidget)
        self.viewBox.setLayout(self.viewLayout)

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.addWidget(self.buttonBox)

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.addWidget(self.viewBox)
        self.mainLayout.addLayout(self.horizontalLayout)

        self.setLayout(self.mainLayout)


