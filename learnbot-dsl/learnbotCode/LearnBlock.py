import cPickle as pickle
import os

from blocksConfig import configBlocks

import guis.addVar as addVar
import guis.gui as gui
from Block import *
from Scene import *
from View import *
from guiCreateBlock import *


def loadfile(file):
    fh = open(file, "r")
    code = fh.read()
    fh.close()
    return code


class MyButtom(QtGui.QPushButton):

    def __init__(self,text,view,scene,imgFile,connections, vars, blockType,table,row,type):
        self.__text=text
        self.__view = view
        self.__scene = scene
        self.__file = imgFile
        self.__connections = connections
        self.__vars = vars
        self.__blockType = blockType
        self.__type = type
        self.tmpFile = "tmp/"+text+str(row)+".png"
        QtGui.QPushButton.__init__(self)
        im = cv2.imread(imgFile,cv2.IMREAD_UNCHANGED)
        table.setRowHeight(row-1,im.shape[0])
        img = generateBlock2(im,34,text,blockType,connections,None,type)
        cv2.imwrite(self.tmpFile, img, (cv2.IMWRITE_PNG_COMPRESSION, 9))
        self.setIcon(QtGui.QIcon(self.tmpFile))
        self.setIconSize(QtCore.QSize(100,100))
        self.setFixedSize(QtCore.QSize(150, im.shape[0]))
        self.clicked.connect(self.clickedButton)

    def removeTmpFile(self):
        os.remove(self.tmpFile)

    def clickedButton(self):
        block = AbstractBlockItem(0,0,self.__text,self.__file,copy.deepcopy(self.__vars), self.__connections,self.__blockType,self.__type)
        self.__scene.addItem(block)

class LearnBlock:

    def __init__(self):
        self.__fileProject = None
        app = QtGui.QApplication(sys.argv)
        self.Dialog = QtGui.QMainWindow()
        self.ui = gui.Ui_MainWindow()
        self.ui.setupUi(self.Dialog)
        self.Dialog.showMaximized()
        self.ui.pushButton.clicked.connect(self.printProgram)

        self.view = MyView(self.ui.frame)
        self.view.setObjectName("view")
        self.ui.verticalLayout_3.addWidget(self.view)
        self.scene = MyScene(self.view)
        self.view.setScene(self.scene)
        self.view.show()
        self.createBlockGui = None
        #READ FUNTIONS
        functions = configBlocks

        self.dicTables = {'control':self.ui.tableControl,'motor':self.ui.tableMotor, 'perceptual':self.ui.tablePerceptual,
                     'proprioceptive':self.ui.tablePropioperceptive,'operador':self.ui.tableOperadores}
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
        for f in functions:
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
                fh = open(img, "r")
                text = fh.readlines()
                fh.close()
                connections = []
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
                        line = line.replace("\n","")
                        line = line.replace(" ", "")
                        c = line.split(",")
                        type = None
                        if "TOP" in c[2] :
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

                table = self.dicTables[f[1]["type"][0]]
                table.insertRow(table.rowCount())
                button = MyButtom(f[1]["name"][0], self.view, self.scene, img+".png", connections, variables, blockType,
                                  table,table.rowCount(),funtionType)
                self.listButtons.append(button)
                table.setCellWidget(table.rowCount()-1, 0, button)
            self.listBlock.append(Block(f[1]["name"][0],funtionType,variables,f[1]["file"]))

        self.timer = QtCore.QTimer()
        self.timer.start(1000)
        self.ui.actionCreate_New_block.triggered.connect(self.showCreateBlock)
        self.ui.actionSave.triggered.connect(self.saveInstance)
        self.ui.actionSave_As.triggered.connect(self.saveAs)
        self.ui.actionOpen_Proyect.triggered.connect(self.openProyect)
        self.ui.tabWidget_2.setFixedWidth(221)
        r = app.exec_()



        for b in self.listButtons:
            b.removeTmpFile()
        os.rmdir("tmp")
        sys.exit(r)

    def saveInstance(self):
        if self.__fileProject is None:
            fileName = QtGui.QFileDialog.getSaveFileName(self.Dialog, 'Save Project', '.',
                                                         'Block Project file (*.blockProject)')
            if fileName[0] != "":
                self.__fileProject = fileName[0]
                self.saveInstance()
        if self.__fileProject is not None:
            with open(self.__fileProject, 'wb') as fichero:
                pickle.dump(self.scene.dicBlockItem, fichero,0)

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
                    self.scene.setBlockDict(d)
                    self.scene.startAllblocks()
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
        self.createBlockGui = guiCreateBlock()
        self.createBlockGui.open()

    def printProgram(self):
        inst = self.scene.getListInstructions()
        if inst is not None:
            self.ui.plainTextEdit_2.clear()
            self.ui.plainTextEdit_2.appendPlainText(self.toLBotPy(inst[1]["BOTTOMIN"]))
            self.generateTmpFile()

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
        inst = self.scene.getListInstructions()
        if inst is not None:
            text = """
import sys
import cv2
import time
import LearnBotClient
from functions import *

#EXECUTION: python code_example.py Ice.Config=config

global lbot
lbot = LearnBotClient.Client(sys.argv)

"""
            text += self.toLBotPy(inst[1]["BOTTOMIN"])
            fh = open("../main_tmp.py","wr")
            fh.writelines(text)
            fh.close()
            while True:
                try:
                    execfile("../main_tmp.py",{"":"../config"})
                    break
                except Exception as e:
                    msgBox = QtGui.QMessageBox()
                    msgBox.setText("Error to the execute program.")
                    msgBox.setInformativeText(e.message)
                    msgBox.setStandardButtons(QtGui.QMessageBox.Retry | QtGui.QMessageBox.Ok)
                    msgBox.setDefaultButton(QtGui.QMessageBox.Ok)
                    ret = msgBox.exec_()
                    if ret == QtGui.QMessageBox.Ok:
                        break

    def toLBotPy(self,inst,ntab=1):
        text = inst[0]
        if inst[1]["TYPE"] is FUNTION:
            text = "functions.get(\"" + inst[0] + "\")(lbot"
            if inst[1]["VARIABLES"] is not None:
                text += ", ["
                for var in inst[1]["VARIABLES"]:
                    text += var + ", "
                text = text[0:-2] + "]"
            text += ")"

        if inst[1]["RIGHT"] is not None:
            text += " " + self.toLBotPy(inst[1]["RIGHT"])
        if inst[1]["BOTTOMIN"] is not None:
            text += ":\n" + "\t" * ntab + self.toLBotPy(inst[1]["BOTTOMIN"], ntab + 1)
        if inst[1]["BOTTOM"] is not None:
            text += "\n" + "\t" * (ntab - 1) + self.toLBotPy(inst[1]["BOTTOM"], ntab)
        return text

    def newVariable(self):
        ui = addVar.Ui_Dialog()
        ui.setupUi(self.Dialog)