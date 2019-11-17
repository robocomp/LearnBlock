from __future__ import print_function, absolute_import
import os, sys, json
from PySide2 import QtGui, QtWidgets
import learnbot_dsl.guis.TabLibrary as TabLibrary
from learnbot_dsl.blocksConfig.parserConfigBlock import reload_functions
from learnbot_dsl.blocksConfig.blocks import *
from learnbot_dsl.blocksConfig.blocks import pathBlocks as imgPath
from learnbot_dsl.learnbotCode.Block import *
from learnbot_dsl.learnbotCode.Button import Block_Button


class Library(QtWidgets.QWidget):

    def __init__(self, parent, path):
        QtWidgets.QWidget.__init__(self)
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
                            with open(subsubPath, "rb") as f:
                                text = f.read()
                            self.load(json.loads(text))

    def load(self, blocks):
        listRepitFuntions = []
        for b in blocks:
            if b["name"] in self.parent.listNameUserFunctions or b["name"] in self.parent.listNameLibraryFunctions:
                listRepitFuntions.append(b["name"])
                continue
            self.namesFunctions.append(b["name"])
            self.parent.listNameLibraryFunctions.append(b["name"])
            variables = []
            funtionType = LIBRARY
            HUE = HUE_LIBRARY
            for img in b["shape"]:
                img = os.path.join(imgPath, img)
                blockType, connections = loadConfigBlock(img)
                table = self.ui.tableLibrary
                table.insertRow(table.rowCount())
                tooltip = {}
                languages = {}
                if "languages" in b:
                    languages = b["languages"]
                if "tooltip" in b:
                    tooltip = b["tooltip"]
                button = Block_Button((self.parent, b["name"], languages, HUE, self.parent.view, self.parent.scene,
                                       img + ".png", connections,
                                       variables, blockType, table, table.rowCount() - 1,
                                       funtionType, tooltip))
                self.parent.listButtons.append(button)
                self.listButons.append((button, table.rowCount() - 1))
                table.setCellWidget(table.rowCount() - 1, 0, button)
        if len(listRepitFuntions) is not 0:
            text = ""
            for name in listRepitFuntions:
                text += "\t * " + name + "\n"
            msgBox = QtWidgets.QMessageBox()
            msgBox.setWindowTitle(self.tr("Warning"))
            msgBox.setIcon(QtWidgets.QMessageBox.Warning)
            msgBox.setText(
                self.tr("The following functions have not been imported because there are others with the same name:"))
            msgBox.setInformativeText(text)
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msgBox.setDefaultButton(QtWidgets.QMessageBox.Ok)
            ret = msgBox.exec_()

    def delete(self):
        for button, row in self.listButons:
            self.parent.listButtons.remove(button)
            button.delete(row)
        for name in self.namesFunctions:
            self.parent.listNameLibraryFunctions.remove(name)

    def __del__(self):
        print("delete Library")
