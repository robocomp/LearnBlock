from PySide import QtGui
from guis import tabLibrary
import os
from blocksConfig.parserConfigBlock import parserConfigBlock
from blocksConfig.blocks import *
from blocksConfig.blocks import pathBlocks as imgPath
from Block import *
from Button import Block_Button
class Library(QtGui.QWidget):

    def __init__(self, parent, path):
        QtGui.QWidget.__init__(self)
        self.ui = tabLibrary.Ui_Form()
        self.parent = parent
        self.ui.setupUi(self)
        self.pathLibrary = path
        self.ui.tableLibrary.verticalHeader().setVisible(False)
        self.ui.tableLibrary.horizontalHeader().setVisible(False)
        self.ui.tableLibrary.setColumnCount(1)
        self.ui.tableLibrary.setRowCount(0)
        self.namesFunctions = []
        self.listButons = []
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
                continue # TODO Show QMenssage funtion alredy exist
            self.namesFunctions.append(f.name[0])
            self.parent.listNameLibraryFunctions.append(f.name[0])
            variables = []
            funtionType = LIBRARY
            HUE = HUE_LIBRARY
            # blockType = None
            for img in f.img:
                img = imgPath + "/" + img
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
        print "delete Library"