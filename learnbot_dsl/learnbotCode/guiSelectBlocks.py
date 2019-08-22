from __future__ import print_function, absolute_import
import os, tempfile, json, sys
from PySide2 import QtGui, QtWidgets, QtCore, Qt
import learnbot_dsl.guis.CreateBlock as CreateBlock
from learnbot_dsl.blocksConfig.blocks import pathBlocks
from learnbot_dsl.blocksConfig.parserConfigBlock import pathConfig
from learnbot_dsl.learnbotCode.Block import *
from learnbot_dsl.learnbotCode.toQImage import *

listTypeBlock = ["express",
                 "motor",
                 "perceptual",
                 "proprioceptive",
                 "others"]



class guiSelectBlocks(QtWidgets.QDialog):

    def __init__(self, blockLists):
        QtWidgets.QDialog.__init__(self)
        self.setWindowTitle('Example List')
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
        bList.addItems(blockList)
        for i in range(len(blockList)):
            item = bList.item(i)
            item.setFlags(item.flags() or Qt.ItemIsUserCheckable)
            item.setCheckState(QtCore.Qt.Unchecked)

    def createButtons(self):
        self.viewBox = QtWidgets.QGroupBox()
        self.buttonBox = QtWidgets.QDialogButtonBox()
        self.saveButton = self.buttonBox.addButton(QtWidgets.QDialogButtonBox.Save)
        self.closeButton = self.buttonBox.addButton(QtWidgets.QDialogButtonBox.Close)
        self.closeButton.clicked.connect(self.close)
        self.saveButton.clicked.connect(self.printList)

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

    def printList(self):
        for l in self.lists:
            for i in range(l.count()):
                item = l.item(i)
                if item.checkState() == QtCore.Qt.Checked:
                    print(item.text())
    
        
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    selectBlocks =guiSelectBlocks({"tab1":["uno","dos","tres"], "tab2":["aaa","bbb","ccc"]})
    selectBlocks.show()
    sys.exit(app.exec_())
