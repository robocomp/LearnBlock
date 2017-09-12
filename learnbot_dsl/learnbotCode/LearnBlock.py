#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cPickle as pickle
import os
from blocksConfig import reload_functions
import threading
import guis.addVar as addVar
import guis.gui as gui
import guis.delVar as delVar
import guis.createFunctions as guiCreateFunctions
from Block import *
from Scene import *
from View import *
from guiCreateBlock import *
from guiAddNumberOrString import *


from multiprocessing import Process

import shutil
import sys
import cv2
import time
import learnbot_dsl.LearnBotClient as LearnBotClient

from learnbot_dsl.functions import *
from blocksConfig.blocks import pathBlocks
from  parserText import parserFile
from checkFile import compile

def loadfile(file):
    fh = open(file, "r")
    code = fh.read()
    fh.close()
    return code


class MyButtom(QtGui.QPushButton):

    def __init__(self,args):
        if len(args) is 10:
            self.__text, self.__view, self.__scene, self.__file, self.__connections, self.__vars, self.__blockType,\
            self.__table, self.__row, self.__type = args
            self.tmpFile = "tmp/" + self.__text + str(self.__type) + str(self.__row) + ".png"

        elif len(args) is 5:
            abstracBlockItem, self.__view, self.__scene, self.__table, self.__row = args
            self.__text = abstracBlockItem.name
            self.__file = abstracBlockItem.file
            self.__connections = abstracBlockItem.connections
            self.__vars = abstracBlockItem.vars
            self.__blockType = abstracBlockItem.typeBlock
            self.__type = abstracBlockItem.type
            self.tmpFile = "tmp/" + self.__text + str(self.__type) + str(self.__row) + ".png"

        QtGui.QPushButton.__init__(self)
        im = cv2.imread(self.__file, cv2.IMREAD_UNCHANGED)

        img = generateBlock(im, 34, self.__text, self.__blockType, self.__connections, None, self.__type)
        cv2.imwrite(self.tmpFile, img, (cv2.IMWRITE_PNG_COMPRESSION, 9))
        self.setIcon(QtGui.QIcon(self.tmpFile))
        self.setIconSize(QtCore.QSize(135, im.shape[0]))
        self.setFixedSize(QtCore.QSize(150, im.shape[0]))
        self.__table.setRowHeight(self.__row, im.shape[0])
        self.clicked.connect(self.clickedButton)
        self.__item = self.__table.item(self.__row,0)

    def removeTmpFile(self):
        try:
            os.remove(self.tmpFile)
        except Exception as e:
            print e

    def clickedButton(self):
        block = AbstractBlockItem(0,0,self.__text,self.__file,copy.deepcopy(self.__vars), self.__connections,self.__blockType,self.__type)
        self.__scene.addItem(block)

    def getAbstracBlockItem(self):
        return AbstractBlockItem(0,0,self.__text,self.__file,copy.deepcopy(self.__vars), self.__connections, self.__blockType,self.__type)

    def delete(self,row):
        self.__table.removeCellWidget(row,0)
        self.__table.removeRow(row)
        self.__scene.removeByName(self.__text)
        del self

    def getText(self):
        return self.__text

class LearnBlock:

    def __init__(self):
        self.addNumberOrStringGui = None
        self.delUserFunctionsGui = None
        self.delUserFunctionsDialgo = None
        self.delVarGui = None
        self.delVarDialgo = None
        self.userFunctionsGui = None
        self.userFunctionsDialgo = None
        self.listNameUserFunctions = []
        self.listNameVars = []
        self.listNameBlock = []
        self.__fileProject = None
        app = QtGui.QApplication(sys.argv)
        self.Dialog = QtGui.QMainWindow()
        self.ui = gui.Ui_MainWindow()
        self.ui.setupUi(self.Dialog)
        self.Dialog.showMaximized()
        self.ui.startPushButton.clicked.connect(self.printProgram)
        self.ui.startTextPushButton.clicked.connect(self.generateTmpFilefromText)
        self.ui.stopPushButton.clicked.connect(self.stopthread)
        self.ui.stoptextPushButton.clicked.connect(self.stopthread)
        self.ui.addVarPushButton.clicked.connect(self.newVariable)
        self.ui.addNumberpushButton.clicked.connect(lambda: self.showGuiAddNumberOrString(1))
        self.ui.addStringpushButton.clicked.connect(lambda: self.showGuiAddNumberOrString(2))
        self.ui.stopPushButton.setEnabled(False)
        self.ui.startPushButton.setEnabled(True)
        self.ui.savepushButton.setIcon(QtGui.QIcon("guis/save.png"))
        self.ui.openpushButton.setIcon(QtGui.QIcon("guis/open.png"))
        self.ui.openpushButton.setFixedSize(QtCore.QSize(24,22))
        self.ui.savepushButton.setFixedSize(QtCore.QSize(24,22))
        self.ui.openpushButton.setIconSize(QtCore.QSize(24,22))
        self.ui.savepushButton.setIconSize(QtCore.QSize(24,22))
        self.ui.zoompushButton.setIcon(QtGui.QIcon("guis/zoom.png"))
        self.ui.zoompushButton.setIconSize(QtCore.QSize(30,30))
        self.ui.zoompushButton.setFixedSize(QtCore.QSize(30,30))
        self.ui.zoompushButton.clicked.connect(self.setZoom)
        self.listVars = []
        self.listUserFunctions = []
        self.addVarGui = None
        self.addVarDialgo = None
        self.view = MyView(self.ui.frame)
        self.view.setObjectName("view")
        self.ui.verticalLayout_3.addWidget(self.view)
        self.scene = MyScene(self.view)
        self.view.setScene(self.scene)
        self.view.show()
        self.view.setZoom(False)
        self.createBlockGui = None
        #READ FUNTIONS
        #process
        self.hilo = None

        #thread
        #self.hilo = threading.Thread(target=self.execTmp, args=[])

        self.dicTables = {'control':self.ui.tableControl,'motor':self.ui.tableMotor, 'perceptual':self.ui.tablePerceptual,
                     'proprioceptive':self.ui.tablePropioperceptive,'operador':self.ui.tableOperadores,'variables':self.ui.tableVariables,
                          'funtions':self.ui.tableUserfunctions}
        for t in self.dicTables:
            table = self.dicTables[t]
            table.verticalHeader().setVisible(False)
            table.horizontalHeader().setVisible(False)
            table.setColumnCount(1)
            table.setRowCount(0)

        self.listButtons = []
        self.listBlock = []
        try:
            os.mkdir("tmp")
        except:
            pass

        self.load_blocks()

        self.timer = QtCore.QTimer()
        self.timer.start(1000)
        self.ui.actionCreate_New_block.triggered.connect(self.showCreateBlock)
        self.ui.actionSave.triggered.connect(self.saveInstance)
        self.ui.actionSave_As.triggered.connect(self.saveAs)
        self.ui.savepushButton.clicked.connect(self.saveInstance)
        self.ui.actionOpen_Proyect.triggered.connect(self.openProyect)
        self.ui.openpushButton.clicked.connect(self.openProyect)
        self.ui.deleteVarPushButton.clicked.connect(self.deleteVar)
        self.ui.createFunctionsPushButton.clicked.connect(self.newUserFunctions)
        self.ui.deleteFuntionsPushButton.clicked.connect(self.deleteUserFunctions)
        self.ui.tabWidget_2.setFixedWidth(221)
        self.scene.setlistNameVars(self.listNameVars)
        r = app.exec_()

        for b in self.listButtons:
            b.removeTmpFile()

        shutil.rmtree("tmp")
        #os.rmdir("tmp")
        sys.exit(r)

    def setZoom(self):
        self.view.setZoom(self.ui.zoompushButton.isChecked())

    def load_blocks(self):
        functions = reload_functions()
        for f in functions:
            if f[1]["name"][0] in self.listNameBlock:
                continue
            self.listNameBlock.append(f[1]["name"][0])
            variables = []
            if "variables" in f[1]:
                for v in f[1]["variables"]:
                    variables.append(Variable(v[0], v[1], v[2]))
            funtionType = None
            if "control" in f[1]["type"][0]:
                funtionType = CONTROL
            elif "motor" in f[1]["type"][0]:
                funtionType = FUNTION
            elif "perceptual" in f[1]["type"][0]:
                funtionType = FUNTION
            elif "proprioceptive" in f[1]["type"][0]:
                funtionType = FUNTION
            elif "operador" in f[1]["type"][0]:
                funtionType = OPERATOR
            blockType = None
            for img in f[1]["img"]:
                blockType, connections = self.loadConfigBlock(img)
                table = self.dicTables[f[1]["type"][0]]
                table.insertRow(table.rowCount())
                button = MyButtom(
                    (f[1]["name"][0], self.view, self.scene, img + ".png", connections, variables, blockType,
                     table, table.rowCount()-1, funtionType))
                self.listButtons.append(button)
                table.setCellWidget(table.rowCount() - 1, 0, button)

    def loadConfigBlock(self, img):
        fh = open(img, "r")
        text = fh.readlines()
        fh.close()
        connections = []
        blockType = None
        for line in text:
            if "type" in line:
                line = line.replace("\n", "")
                line = line.split(" ")
                blockType = line[1]
                if "simple" in blockType:
                    blockType = SIMPLEBLOCK
                elif "complex" in blockType:
                    blockType = COMPLEXBLOCK
            else:
                line = line.replace("\n", "")
                line = line.replace(" ", "")
                c = line.split(",")
                type = None
                if "TOP" in c[2]:
                    type = TOP
                elif "BOTTOMIN" in c[2]:
                    type = BOTTOMIN
                elif "BOTTOM" in c[2]:
                    type = BOTTOM
                elif "RIGHT" in c[2]:
                    type = RIGHT
                elif "LEFT" in c[2]:
                    type = LEFT
                connections.append((QtCore.QPointF(int(c[0]), int(c[1])), type))
        return blockType, connections

    def execTmp(self):
        while True:
            try:
		sys.argv = [' ','configSimulated']
                execfile("main_tmp.py", globals())
                break
            except Exception as e:
                print e
                msgBox = QtGui.QMessageBox()
                msgBox.setText("Error to the execute program.")
                msgBox.setStandardButtons(QtGui.QMessageBox.Retry | QtGui.QMessageBox.Ok)
                msgBox.setDefaultButton(QtGui.QMessageBox.Ok)
                ret = msgBox.exec_()
                if ret is not QtGui.QMessageBox.Retry:
                    break

    def stopExecTmp(self):
         try:
	     sys.argv = [' ','configSimulated']
             execfile("stop_main_tmp.py", globals())
         except Exception as e:
             print e


    def saveInstance(self):
        if self.__fileProject is None:
            fileName = QtGui.QFileDialog.getSaveFileName(self.Dialog, 'Save Project', '.',
                                                         'Block Project file (*.blockProject)')
            file = fileName[0]
            if "." in file:
                file = file.split(".")[0]
            file = file+".blockProject"
            if file != "":
                self.__fileProject = file
                self.saveInstance()
        if self.__fileProject is not None:
            with open(self.__fileProject, 'wb') as fichero:
                dic=copy.deepcopy(self.scene.dicBlockItem)
                for id in dic:
                    block = dic[id]
                    block.file = block.file.replace(pathImgBlocks,"")
                pickle.dump((dic,self.listVars,self.listUserFunctions,self.listNameVars,self.listNameUserFunctions), fichero,0)
        self.scene.shouldSave = False

    def saveAs(self):
        fileName = QtGui.QFileDialog.getSaveFileName(self.Dialog, 'Save Project', '.',
                                                     'Block Project file (*.blockProject);;Learbot code text file (*.LearbotCode)')
        if fileName[0] != "":
            file = fileName[0]
            if "." in file:
                file = file.split(".")[0]
            if fileName[1] == "Learbot code text file (*.LearbotCode)":
                file = file+".LearbotCode"
                inst = self.scene.getListInstructions()
                if inst is not None:
                    fh = open(file, "wr")
                    fh.writelines(self.printInst(inst))
                    fh.close()
            elif fileName[1] == "Block Project file (*.blockProject)":
                file = file + ".blockProject"
                self.__fileProject = file
                self.saveInstance()

    def openProyect(self):
        if self.scene.shouldSave is False:
            fileName = QtGui.QFileDialog.getOpenFileName(self.Dialog, 'Open Project', '.','Block Project file (*.blockProject)')
            if fileName[0] != "":
                self.__fileProject = fileName[0]
                with open(self.__fileProject, 'rb') as fichero:
                    d = pickle.load(fichero)
                    dictBlock = d[0]
                    for id in dictBlock:
                        block = dictBlock[id]
                        block.file = pathImgBlocks + block.file
                    self.scene.setBlockDict(d[0])
                    self.scene.startAllblocks()
                    for name in self.listNameUserFunctions:
                        self.delUserFunction(name)
                    for name in self.listNameVars:
                        self.delVar(name)
                    for name in d[3]:
                        self.addVariable(name)
                    self.listNameVars = d[3]
                    for name in d[4]:
                        self.addUserFunction(name)
                    self.listNameUserFunctions = d[4]


        else:
            msgBox = QtGui.QMessageBox()
            msgBox.setText("The document has been modified.")
            msgBox.setInformativeText("Do you want to save your changes?")
            msgBox.setStandardButtons(QtGui.QMessageBox.Save | QtGui.QMessageBox.Discard | QtGui.QMessageBox.Cancel)
            msgBox.setDefaultButton(QtGui.QMessageBox.Save)
            ret = msgBox.exec_()
            if ret == 2048:
                self.saveInstance()
            elif ret == 8388608:
                self.scene.shouldSave=False
                self.openProyect()

    def showCreateBlock(self):
        self.createBlockGui = guiCreateBlock(self.load_blocks)
        #self.createBlockGui.ui.pushButtonOK.clicked.connect(self.load_blocks)
        self.createBlockGui.open()

    def showGuiAddNumberOrString(self,type):
        self.addNumberOrStringGui = guiAddNumberOrString(type)
        self.addNumberOrStringGui.ui.pushButtonOK.clicked.connect(self.addBlockNumberOrString)
        self.addNumberOrStringGui.open()

    def addBlockNumberOrString(self):
        text = self.addNumberOrStringGui.value
        imgPath = self.addNumberOrStringGui.imgName
        configImgPath = imgPath.replace(".png","")
        blockType, connections = self.loadConfigBlock(configImgPath)
        block = AbstractBlockItem(0,0,text,imgPath,[], connections, blockType,VARIABLE)
        self.scene.addItem(block)

    def printProgram(self):
        blocks = self.scene.getListInstructions()
        if blocks is not None:
            #self.ui.plainTextEdit_2.clear()
            #self.ui.plainTextEdit_2.appendPlainText(self.parserBlocks(blocks,self.toLBotPy))
            self.generateTmpFile()

    #TODO Esperar a que termine el parseador de texto
    def generateTmpFilefromText(self):
        text = self.ui.plainTextEdit_2.toPlainText() #TODO
        parserFile(text,"main_tmp.py")

    def printInst(self,inst,ntab=1):
        text = inst[0]
        if inst[1]["VARIABLES"] is not None:
            text += "("
            for var in inst[1]["VARIABLES"]:
                text += var + ", "
            text = text[0:-2] + ")"

        if inst[1]["RIGHT"] is not None:
            text += " " + self.printInst(inst[1]["RIGHT"])
        if inst[1]["BOTTOMIN"] is not None:
            text += ":\n"+"\t"*ntab + self.printInst(inst[1]["BOTTOMIN"],ntab+1)
        if inst[1]["BOTTOM"] is not None:
            text += "\n"+"\t"*(ntab-1) + self.printInst(inst[1]["BOTTOM"],ntab)
        return text

    def generateTmpFile(self):
        blocks = self.scene.getListInstructions()
        text = """

#EXECUTION: python code_example.py config

global lbot
lbot = LearnBotClient.Client(sys.argv)

"""
        if len(self.listNameVars)>0:
            for name in self.listNameVars:
                text += name + " = None\n"

        if blocks is not None:
            code = self.parserBlocks(blocks,self.toLBotPy)
            fh = open("main_tmp.py","wr")
            fh.writelines(text + code)
            fh.close()
            if compile("main_tmp.py"):
                self.hilo = Process(target=self.execTmp)
                self.hilo.start()
                self.ui.stopPushButton.setEnabled(True)
                self.ui.startPushButton.setEnabled(False)
            else:
                msgBox = QtGui.QMessageBox()
                msgBox.setText("Your code has an error. Check it out again")
                msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
                msgBox.setDefaultButton(QtGui.QMessageBox.Ok)
                ret = msgBox.exec_()

    def generateStopTmpFile(self):
        text = """

#EXECUTION: python code_example.py config

global lbot
lbot = LearnBotClient.Client(sys.argv)

functions.get("stop_bot")(lbot)
"""
        fh = open("stop_main_tmp.py","wr")
        fh.writelines(text)
        fh.close()


    def stopthread(self):
        try:
            self.hilo.terminate()
	    self.generateStopTmpFile()
            self.hilo = Process(target=self.stopExecTmp)
            self.hilo.start()
            self.hilo.join()
            self.ui.stopPushButton.setEnabled(False)
            self.ui.startPushButton.setEnabled(True)
        except Exception as e:
            pass

    def parserBlocks(self,blocks,funtion):
        text = ""
        if len(blocks) > 1:
            text = "class User:\n"
        for b in blocks:
            if "main" not in b[0]:
                text += "\tdef "+b[0]+"(self):\n"
                if len(self.listNameVars) > 0:
                    for name in self.listNameVars:
                        text += "\t\tglobal " + name + "\n"
                if b[1]["BOTTOMIN"] is not None:
                    text += "\t\t" + funtion(b[1]["BOTTOMIN"],3)
                else:
                    text += "pass"
                text += "\n\n"
        for b in blocks:
            if "main" in b[0]:
                if b[1]["BOTTOMIN"] is not None:
                    text += funtion(b[1]["BOTTOMIN"])
                else:
                    text += "pass"
                text += "\n\n"
        return text

    def toLBotPy(self,inst,ntab=1):
        text = inst[0]
        if inst[1]["TYPE"] is USERFUNCTION:
            text = "User()."+inst[0]+"()"
        if inst[1]["TYPE"] is FUNTION :
            text = "functions.get(\"" + inst[0] + "\")(lbot"
            if inst[1]["VARIABLES"] is not None:
                text += ", "
                for var in inst[1]["VARIABLES"]:
                    text += var + ", "
                text = text[0:-2] + ""
            text += ")"
        elif inst[1]["TYPE"] is VARIABLE:
            text = inst[0]
            if inst[1]["VARIABLES"] is not None:
                text += " = "
                for var in inst[1]["VARIABLES"]:
                    text += var

        if inst[1]["RIGHT"] is not None:
            text += " " + self.toLBotPy(inst[1]["RIGHT"])
        if inst[1]["BOTTOMIN"] is not None:
            text += ":\n" + "\t" * ntab + self.toLBotPy(inst[1]["BOTTOMIN"], ntab + 1)
        if inst[1]["BOTTOM"] is not None:
            text += "\n" + "\t" * (ntab - 1) + self.toLBotPy(inst[1]["BOTTOM"], ntab)
        return text

    def newVariable(self):
        self.addVarGui = addVar.Ui_Dialog()
        self.addVarDialgo = QtGui.QDialog()
        self.addVarGui.setupUi(self.addVarDialgo)
        self.addVarDialgo.open()
        self.addVarGui.cancelPushButton.clicked.connect(lambda :self.retaddVarGui(0))
        self.addVarGui.okPushButton.clicked.connect(lambda : self.retaddVarGui(1))

    def retaddVarGui(self,ret):
        if ret is 1:
            name = self.addVarGui.nameLineEdit.text()
            if name in self.listNameVars:
                msgBox = QtGui.QMessageBox()
                msgBox.setText("This name alredy exist")
                msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
                msgBox.setDefaultButton(QtGui.QMessageBox.Ok)
                ret = msgBox.exec_()
                return
            if " " in name:
                msgBox = QtGui.QMessageBox()
                msgBox.setText("The name can't contain ' '")
                msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
                msgBox.setDefaultButton(QtGui.QMessageBox.Ok)
                ret = msgBox.exec_()
                return
            """
            if name.find("ñ") is -1:
                msgBox = QtGui.QMessageBox()
                msgBox.setText("The name can't contain 'ñ'")
                msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
                msgBox.setDefaultButton(QtGui.QMessageBox.Ok)
                ret = msgBox.exec_()
                return
            """
            if name[0].isdigit():
                msgBox = QtGui.QMessageBox()
                msgBox.setText("The name can't start by number")
                msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
                msgBox.setDefaultButton(QtGui.QMessageBox.Ok)
                ret = msgBox.exec_()
                return
            self.addVariable(name)

        self.addVarDialgo.close()

    def addVariable(self,name):
        self.ui.deleteVarPushButton.setEnabled(True)
        imgs = ['block2', 'block3', 'block4']

        self.listNameVars.append(name)
        blockType, connections = self.loadConfigBlock(pathBlocks + "/block1")
        table = self.dicTables['variables']
        table.insertRow(table.rowCount())
        variables = []
        variables.append(Variable("float", "set to ", "0"))
        button = MyButtom(
            (name, self.view, self.scene, pathBlocks + "/block1" + ".png", connections, variables, blockType,
             table, table.rowCount() - 1, VARIABLE))
        self.listButtons.append(button)
        table.setCellWidget(table.rowCount() - 1, 0, button)
        self.listVars.append(button.getAbstracBlockItem())
        for img in imgs:
            blockType, connections = self.loadConfigBlock(pathBlocks + "/" + img)
            table = self.dicTables['variables']
            table.insertRow(table.rowCount())
            button = MyButtom((name, self.view, self.scene, pathBlocks + "/" + img + ".png", connections, [], blockType,
                               table, table.rowCount() - 1, VARIABLE))
            self.listButtons.append(button)
            table.setCellWidget(table.rowCount() - 1, 0, button)
            self.listVars.append(button.getAbstracBlockItem())

    def deleteVar(self):
        self.delVarGui = delVar.Ui_Dialog()
        self.delVarDialgo = QtGui.QDialog()
        self.delVarGui.setupUi(self.delVarDialgo)
        self.delVarDialgo.open()
        self.delVarGui.listVarcomboBox.clear()
        self.delVarGui.listVarcomboBox.currentText()
        for name in self.listNameVars:
            self.delVarGui.listVarcomboBox.addItem(name)
        self.delVarGui.cancelPushButton.clicked.connect(lambda :self.retdelVarGui(0))
        self.delVarGui.okPushButton.clicked.connect(lambda :self.retdelVarGui(1))

    def retdelVarGui(self, ret):
        if ret is 1:
            name = self.delVarGui.listVarcomboBox.currentText()
            self.delVar(name)
        self.delVarDialgo.close()
        if len(self.listNameVars) == 0:
            self.ui.deleteVarPushButton.setEnabled(False)

    def delVar(self,name):
        table = self.dicTables['variables']
        rango = reversed(range(0, table.rowCount()))
        for row in rango:
            item = table.cellWidget(row, 0)
            if item.getText() == name:
                item.delete(row)
                item.removeTmpFile()
                self.listButtons.remove(item)
        self.listNameVars.remove(name)

    def newUserFunctions(self):
        self.userFunctionsGui = guiCreateFunctions.Ui_Dialog()
        self.userFunctionsDialgo = QtGui.QDialog()
        self.userFunctionsGui.setupUi(self.userFunctionsDialgo)
        self.userFunctionsDialgo.open()
        self.userFunctionsGui.cancelPushButton.clicked.connect(lambda: self.retUserFunctions(0))
        self.userFunctionsGui.okPushButton.clicked.connect(lambda: self.retUserFunctions(1))

    def retUserFunctions(self,ret):
        if ret is 1:
            name = self.userFunctionsGui.nameLineEdit.text()
            if name in self.listNameUserFunctions:
                msgBox = QtGui.QMessageBox()
                msgBox.setText("This name alredy exist")
                msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
                msgBox.setDefaultButton(QtGui.QMessageBox.Ok)
                ret = msgBox.exec_()
                return
            if " " in name:
                msgBox = QtGui.QMessageBox()
                msgBox.setText("The name can't contain ' '")
                msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
                msgBox.setDefaultButton(QtGui.QMessageBox.Ok)
                ret = msgBox.exec_()
                return
            """
            if name.find("ñ") is -1:
                msgBox = QtGui.QMessageBox()
                msgBox.setText("The name can't contain 'ñ'")
                msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
                msgBox.setDefaultButton(QtGui.QMessageBox.Ok)
                ret = msgBox.exec_()
                return
            """
            if name[0].isdigit():
                msgBox = QtGui.QMessageBox()
                msgBox.setText("The name can't start by number")
                msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
                msgBox.setDefaultButton(QtGui.QMessageBox.Ok)
                ret = msgBox.exec_()
                return
            self.addUserFunction(name)

        self.userFunctionsDialgo.close()

    def addUserFunction(self,name):
        self.ui.deleteFuntionsPushButton.setEnabled(True)
        imgs = ['block8', 'block1']
        self.listNameUserFunctions.append(name)
        table = self.dicTables['funtions']
        i = 0
        for img in imgs:
            blockType, connections = self.loadConfigBlock(pathBlocks + "/" + img)
            table.insertRow(table.rowCount())
            button = MyButtom(
                (name, self.view, self.scene, pathBlocks + "/" + img + ".png", connections, [], blockType,
                 table, table.rowCount() - 1, USERFUNCTION))
            self.listButtons.append(button)
            table.setCellWidget(table.rowCount() - 1, 0, button)
            self.listUserFunctions.append(button.getAbstracBlockItem())
            i += 1

    def deleteUserFunctions(self):
        self.delUserFunctionsGui = delVar.Ui_Dialog()
        self.delUserFunctionsDialgo = QtGui.QDialog()
        self.delUserFunctionsGui.setupUi(self.delUserFunctionsDialgo)
        self.delUserFunctionsDialgo.open()
        self.delUserFunctionsGui.listVarcomboBox.clear()
        self.delUserFunctionsGui.listVarcomboBox.currentText()
        for name in self.listNameUserFunctions:
            self.delUserFunctionsGui.listVarcomboBox.addItem(name)
        self.delUserFunctionsGui.cancelPushButton.clicked.connect(lambda: self.retdelUserFunctionsGui(0))
        self.delUserFunctionsGui.okPushButton.clicked.connect(lambda: self.retdelUserFunctionsGui(1))

    def retdelUserFunctionsGui(self,ret):
        if ret is 1:
            name = self.delUserFunctionsGui.listVarcomboBox.currentText()
            self.delUserFunction(name)
        self.delUserFunctionsDialgo.close()
        if len(self.listNameUserFunctions) == 0:
            self.ui.deleteFuntionsPushButton.setEnabled(False)

    def delUserFunction(self,name):
        table = self.dicTables['funtions']
        rango = reversed(range(0, table.rowCount()))
        for row in rango:
            item = table.cellWidget(row, 0)
            if item.getText() == name:
                item.delete(row)
                item.removeTmpFile()
                self.listButtons.remove(item)
        self.listNameUserFunctions.remove(name)
