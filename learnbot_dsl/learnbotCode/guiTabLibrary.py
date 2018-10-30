from __future__ import print_function, absolute_import
import os, sys
from PySide import QtGui
import learnbot_dsl.guis.TabLibrary as TabLibrary
from learnbot_dsl.blocksConfig.parserConfigBlock import parserConfigBlock
from learnbot_dsl.blocksConfig.blocks import *
from learnbot_dsl.blocksConfig.blocks import pathBlocks as imgPath
from learnbot_dsl.learnbotCode.Block import *
from learnbot_dsl.learnbotCode.Button import Block_Button
class Library(QtGui.QWidget):

    def __init__(self, parent, path):
        QtGui.QWidget.__init__(self)
        self.ui = TabLibrary.Ui_Form()
        self.parent = parent
        self.ui.setupUi(self)
        self.ui.tableLibrary.verticalHeader().setVisible(False)
        self.ui.tableLibrary.horizontalHeader().setVisible(False)
        self.ui.tableLibrary.setColumnCount(1)
        self.ui.tableLibrary.setRowCount(0)
        self.namesFunctions = []
        self.listButons = []
        if not os.path.exists(path):
            dirs = [self.parent.libraryPath]
            exist = False
            for dir in dirs:
                for p in os.listdir(dir):
                    if p == os.path.basename(path):
                        path = os.path.join(dir, p)
                        dirs = []
                        exist = True
                        break
                    if os.path.isdir(os.path.join(dir, p)):
                        dirs.append(os.path.join(dir, p))
                    if os.path.isfile(os.path.join(dir, p)):
                        continue
            if not exist:
                path = None
        self.pathLibrary = path
        if path is not None:
            for subPath in [os.path.join(path, x) for x in os.listdir(path)]:
                if os.path.isdir(os.path.abspath(subPath)):
                    for subsubPath in [os.path.join(subPath, x) for x in os.listdir(subPath)]:
                        if os.path.splitext(subsubPath)[-1] == ".conf":
                            self.load(parserConfigBlock(subsubPath))

    def load(self, functions):
        listRepitFuntions = []
        for f in functions:
            if f.name[0] in self.parent.listNameUserFunctions or f.name[0] in self.parent.listNameLibraryFunctions:
                listRepitFuntions.append(f.name[0])
                continue
            self.namesFunctions.append(f.name[0])
            self.parent.listNameLibraryFunctions.append(f.name[0])
            variables = []
            funtionType = LIBRARY
            HUE = HUE_LIBRARY
            # blockType = None
            for img in f.img:
                img = os.path.join(imgPath, img)
                blockType, connections = loadConfigBlock(img)
                table = self.ui.tableLibrary
                table.insertRow(table.rowCount())
                dicTrans = {}
                for l in f.translations:
                    dicTrans[l.language] = l.translation
                dicToolTip = {}
                for l in f.tooltip:
                    dicToolTip[l.language] = l.translation
                button = Block_Button((self.parent, f.name[0], dicTrans, HUE, self.parent.view, self.parent.scene,
                                       img + ".png", connections,
                                       variables, blockType, table, table.rowCount() - 1,
                                       funtionType, dicToolTip))
                self.parent.listButtons.append(button)
                self.listButons.append((button,table.rowCount()- 1))
                table.setCellWidget(table.rowCount() - 1, 0, button)
        if len(listRepitFuntions) is not 0:
            text = ""
            for name in listRepitFuntions:
                text += "\t * " + name + "\n"
            msgBox = QtGui.QMessageBox()
            msgBox.setWindowTitle(self.trUtf8("Warning"))
            msgBox.setIcon(QtGui.QMessageBox.Warning)
            msgBox.setText(self.trUtf8("The following functions have not been imported because there are others with the same name:"))
            msgBox.setInformativeText(text)
            msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
            msgBox.setDefaultButton(QtGui.QMessageBox.Ok)
            ret = msgBox.exec_()

    def delete(self):
        for button,row in self.listButons:
            self.parent.listButtons.remove(button)
            button.delete(row)
        for name in self.namesFunctions:
            self.parent.listNameLibraryFunctions.remove(name)

    def __del__(self):
        print("delete Library")
