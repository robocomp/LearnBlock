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
        for subPath in [os.path.join(path, x) for x in os.listdir(path)]:
            if os.path.isdir(os.path.abspath(subPath)):
                for subsubPath in [os.path.join(subPath, x) for x in os.listdir(subPath)]:
                    if os.path.splitext(subsubPath)[-1] == ".conf":
                        self.load(parserConfigBlock(subsubPath))

    def load(self, functions):
        for f in functions:
            if f.name[0] in self.parent.listNameUserFunctions:
                continue # TODO Show QMenssage funtion alredy exist
            self.parent.listNameUserFunctions.append(f.name[0])
            self.parent.listNameBlock.append(f.name)
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
                table.setCellWidget(table.rowCount() - 1, 0, button)

