#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cPickle as pickle
import learnbot_dsl.LearnBotClient as LearnBotClient
import paramiko, shutil, subprocess, sys
from multiprocessing import Process
from threading import Timer

from Button import *
from Parser import parserLearntBotCode
from Scene import *
from View import *
from blocksConfig import reload_functions
from blocksConfig.blocks import pathBlocks
from checkFile import compile
from guiAddNumberOrString import *
from guiCreateBlock import *
from guiaddWhen import *
from guis import addVar, gui, delVar, delWhen, createFunctions as guiCreateFunctions
from learnbot_dsl.functions import *
from parserConfig import configSSH
from guiTab import *

print sys.version_info[0]

HEADER = """
#EXECUTION: python code_example.py config
from learnbot_dsl.functions import *
import learnbot_dsl.<LearnBotClient> as <LearnBotClient>
import sys
import time
global lbot
global Robot_id
Robot_id = "Id"
try:
    lbot = <LearnBotClient>.Client(sys.argv, "Id")
except Exception as e:
    print "hay un Error"
    print e
"""

path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))


def loadfile(file):
    fh = open(file, "r")
    code = fh.read()
    fh.close()
    return code

currentTabNo = 0

class LearnBlock(QtGui.QMainWindow):

    def __init__(self):
        self.listNameUserFunctions = []
        self.listNameVars = []
        self.listNameBlock = []
        self.listNameWhens = []
        self.listButtonsWhen = []
        self.listVars = []
        self.listUserFunctions = []
        self.listButtons = []
        self.listBlock = []

        self.__fileProject = None
        self.hilo = None
        self.physicalRobot = False

        self.app = QtGui.QApplication(sys.argv)
        self.app.setWindowIcon(QtGui.QIcon(path + '/ico.png'))

        self.Dialog = QtGui.QMainWindow()
        QtGui.QMainWindow.__init__(self)
        self.ui = gui.Ui_MainWindow()
        self.ui.setupUi(self)
        self.showMaximized()
	self.ui.AddRobot.clicked.connect(self.addRobo)
        self.ui.actionExit.triggered.connect(self.exitProgram)
        #READ FUNTIONS
        #process

        #thread
        #self.hilo = threading.Thread(target=self.execTmp, args=[])

        self.timer = QtCore.QTimer()
        self.timer.start(1000)
        r = self.app.exec_()

        '''for b in self.listButtons:
            b.removeTmpFile()

        shutil.rmtree("tmp")
        #os.rmdir("tmp")'''
        sys.exit(r)
        
    def exitProgram(self):
    	sys.exit()
        
    def addRobo(self):
    	global currentTabNo
    	currentTabNo = currentTabNo + 1;
    	NewTab = QtGui.QWidget()
    	vBoxlayout = QtGui.QVBoxLayout()
    	NewTab.setLayout(vBoxlayout)
    	s = "Robot "
    	u = str(currentTabNo)
    	Robot = s+u
    	Robo = Tabs(Robot,self.app)
    	vBoxlayout.addWidget(Robo)
    	self.ui.collaborativeTabs.addTab(NewTab,Robot)
    	self.ui.actionCreate_New_block.triggered.connect(Robo.showCreateBlock)
        self.ui.actionSave.triggered.connect(Robo.saveInstance)
        self.ui.actionSave_As.triggered.connect(Robo.saveAs)
        self.ui.actionOpen_Proyect.triggered.connect(Robo.openProyect)
    	#self.load_blocks()
    	self.ui.collaborativeTabs.show()

    def avtiveEvents(self,isChecked):
        self.ui.addWhenpushButton.setEnabled(isChecked)
        self.mainButton.setEnabled(not isChecked)
        for b in self.listButtonsWhen:
            b.setEnabled(isChecked)

    def setZoom(self):
        self.view.setZoom(self.ui.zoompushButton.isChecked())

    def changeLanguage(self):
        l = ["ES","EN"]
        changeLanguageTo(l[self.ui.language.currentIndex()])

    def load_blocks(self):
        functions = reload_functions()
        for f in functions:
            if f.name in self.listNameBlock:
                continue
            self.listNameBlock.append( f.name )
            variables = []
            if f.variables:
                for v in f.variables:
                    variables.append(Variable(v[0], v[1], v[2]))
            funtionType = None
            if "control" == f.type[0]:
                funtionType = CONTROL
            elif "motor" == f.type[0]:
                funtionType = FUNTION
            elif "perceptual" == f.type[0]:
                funtionType = FUNTION
            elif "proprioceptive" == f.type[0]:
                funtionType = FUNTION
            elif "operador" == f.type[0]:
                funtionType = OPERATOR
            blockType = None
            for img in f.img:
                blockType, connections = self.loadConfigBlock(img)
                table = self.dicTables[f.type[0]]
                table.insertRow(table.rowCount())
                dicTrans = {}
                for l in f.translations:
                    dicTrans[l.language] = l.translation
                button = MyButtom((f.name[0], dicTrans, self.view, self.scene, img + ".png", connections, variables, blockType, table, table.rowCount()-1, funtionType))
                if f.name[0] == "main":
                    self.mainButton = button
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
                pickle.dump((dic,self.listVars,self.listButtonsWhen, self.listNameWhens ,self.listUserFunctions,self.listNameVars,self.listNameUserFunctions), fichero,0)
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
                    self.listButtonsWhen = d[1]
                    self.listNameWhens = d[2]
                    for id in dictBlock:
                        block = dictBlock[id]
                        block.file = pathImgBlocks + block.file
                    self.scene.setBlockDict(d[0])
                    self.scene.startAllblocks()
                    for name in self.listNameUserFunctions:
                        self.delUserFunction(name)
                    for name in self.listNameVars:
                        self.delVar(name)
                    for name in d[5]:
                        self.addVariable(name)
                    self.listNameVars = d[5]
                    for name in d[6]:
                        self.addUserFunction(name)
                    self.listNameUserFunctions = d[6]


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
        block = AbstractBlockItem(0,0,text, {}, imgPath,[], "" , connections, blockType,VARIABLE)
        self.scene.addItem(block)

    def showGuiAddWhen(self):
        self.addWhenGui = guiAddWhen()
        self.addWhenGui.ui.pushButtonOK.clicked.connect(self.addBlockWhen)
        self.addWhenGui.open()

    def addBlockWhen(self):
        text = self.addWhenGui.value
        imgPath = self.addWhenGui.imgName
        configImgPath = imgPath.replace(".png","")
        blockType, connections = self.loadConfigBlock(configImgPath)

        block = AbstractBlockItem(0,0,text, {'ES':"Cuando ", 'EN':"When " }, imgPath, [], self.addWhenGui.nameControl, connections, blockType,VARIABLE)
        self.scene.addItem(block)
        if configImgPath.split('/')[-1] == 'block8':
            blockType, connections = self.loadConfigBlock(pathBlocks + "/block1")
            table = self.dicTables['control']

            table.insertRow(table.rowCount())
            button = MyButtom( ( "active " + self.addWhenGui.nameControl, {'ES':"Activar " + self.addWhenGui.nameControl, 'EN':"Active " + self.addWhenGui.nameControl }, self.view, self.scene, pathBlocks + "/block1" + ".png", connections, [], blockType, table, table.rowCount() - 1, VARIABLE))
            self.listButtonsWhen.append(button)
            self.listButtons.append(button)
            table.setCellWidget(table.rowCount() - 1, 0, button)

            table.insertRow(table.rowCount())
            button = MyButtom( ( "deactive " + self.addWhenGui.nameControl, {'ES':"Desactivar " + self.addWhenGui.nameControl, 'EN':"Deactive " + self.addWhenGui.nameControl }, self.view, self.scene, pathBlocks + "/block1" + ".png", connections, [], blockType, table, table.rowCount() - 1, VARIABLE))
            self.listButtonsWhen.append(button)
            self.listButtons.append(button)
            table.setCellWidget(table.rowCount() - 1, 0, button)

        self.listNameWhens.append(self.addWhenGui.nameControl)
        self.ui.deleteWhenpushButton.setEnabled(True)

    def printProgram(self):
        blocks = self.scene.getListInstructions()
        if blocks is not None:
            self.physicalRobot = False
            self.generateTmpFile()

    def printProgramPR(self):
        blocks = self.scene.getListInstructions()
        if blocks is not None:
            self.physicalRobot = True
            self.generateTmpFile()

    #TODO Esperar a que termine el parseador de texto
    def generateTmpFilefromText(self):
        # code = self.ui.textCode.toPlainText() #TODO
        # if self.physicalRobot:
        #     # text = HEADER.replace('<LearnBotClient>','LearnBotClientPR')
        #     sys.argv = [' ','configPhysical']
        # else:
        #     # text = HEADER.replace('<LearnBotClient>','LearnBotClient')
        #     sys.argv = [' ','configSimulated']
        # text =""
        # fh = open("main_tmp.lb","wr")
        # fh.writelines(text + code)
        # fh.close()
        # try:
        #     parserLearntBotCode("main_tmp.lb", "main_tmp.py", self.physicalRobot)
        # except Exception as e:
        #     print e
        #     print("line: {}".format(e.line))
        #     print("    "+" "*e.col+"^")
        #     return
        # if compile("main_tmp.py"):
        #     self.hilo = Process(target=self.execTmp)
        #     self.hilo.start()
        #     self.ui.stopPushButton.setEnabled(True)
        #     self.ui.startPushButton.setEnabled(False)
        #     self.ui.startPRPushButton.setEnabled(False)
        # else:
        #     msgBox = QtGui.QMessageBox()
        #     msgBox.setText("Your code has an error. Check it out again")
        #     msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
        #     msgBox.setDefaultButton(QtGui.QMessageBox.Ok)
        #     ret = msgBox.exec_()
        pass

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
        if self.physicalRobot:
            # text = HEADER.replace('<LearnBotClient>','LearnBotClientPR')
            sys.argv = [' ','configPhysical']
        else:
            # text = HEADER.replace('<LearnBotClient>','LearnBotClient')
            sys.argv = [' ','configSimulated']
        text =""
        if len(self.listNameVars)>0:
            for name in self.listNameVars:
                text += name + " = None\n"

        if blocks is not None:
            code = self.parserBlocks(blocks,self.toLBotPy)
            fh = open("main_tmp.lb","wr")
            fh.writelines(text + code)
            fh.close()
            # self.ui.textCode.clear()
            # self.ui.textCode.appendPlainText(text + code)
            try:
                parserLearntBotCode("main_tmp.lb", "main_tmp.py", self.physicalRobot)
            except Exception as e:
                print e
                print("line: {}".format(e.line))
                print("    "+" "*e.col+"^")
                return
            if compile("main_tmp.py"):
                self.hilo = Process(target=self.execTmp)
                self.hilo.start()
                self.ui.stopPushButton.setEnabled(True)
                self.ui.startPushButton.setEnabled(False)
                self.ui.startPRPushButton.setEnabled(False)
            else:
                msgBox = QtGui.QMessageBox()
                msgBox.setText("Your code has an error. Check it out again")
                msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
                msgBox.setDefaultButton(QtGui.QMessageBox.Ok)
                ret = msgBox.exec_()

    def generateStopTmpFile(self):
        if self.physicalRobot:
            text = HEADER.replace('<LearnBotClient>','LearnBotClientPR')
            sys.argv = [' ','configPhysical']
        else:
            text = HEADER.replace('<LearnBotClient>','LearnBotClient')
            sys.argv = [' ','configSimulated']
        text += '\nfunctions.get("stop_bot")(lbot)'
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
            self.ui.startPRPushButton.setEnabled(True)
        except Exception as e:
            pass

    def parserBlocks(self,blocks,function): #TODO add parser for blocks when
        text = ""
        for b in blocks:
            print b
        if self.ui.useEventscheckBox.isChecked():
            text = self.parserWhenBlocks(blocks, function)
        else:
            text = self.parserOtherBlocks(blocks, function)
        #
        # for b in blocks:
        #     if "main" == b[0]:
        #         text += "\tdef "+b[0]+"(self):\n"
        #         if len(self.listNameVars) > 0:
        #             for name in self.listNameVars:
        #                 text += "\t\tglobal " + name + "\n"
        #         if b[1]["BOTTOMIN"] is not None:
        #             text += "\t\t" + function(b[1]["BOTTOMIN"],3)
        #         else:
        #             text += "pass"
        #         text += "\n\n"
        # for b in blocks:
        #     if "main" in b[0]:
        #         if b[1]["BOTTOMIN"] is not None:
        #             text += function(b[1]["BOTTOMIN"])
        #         else:
        #             text += "pass"
        #         text += "\n\n"
        print text
        return text

    def parserWhenBlocks(self, blocks, function):
        text = ""
        for b in blocks:
            if b[0] == "when":
                text += "when " + b[1]['NAMECONTROL']
                if b[1]['RIGHT'] is not None:
                    text += " = " + function(b[1]['RIGHT'],0)
                text += ":\n"

                if b[1]['BOTTOMIN'] is not None:
                    text += "\t" + function(b[1]['BOTTOMIN'],2) + "\n"
                else:
                    text += "pass\n"
                text += "end\n\n"
        return text

    def parserOtherBlocks(self, blocks, function):
        text = ""
        for b in blocks:
            if "main" == b[0]:
                text += b[0] + ":\n"
                if b[1]["BOTTOMIN"] is not None:
                    text += "\t" + function(b[1]["BOTTOMIN"],2)
                else:
                    text += "pass"
                text += "\n\n"
        return text

    def toLBotPy(self, inst, ntab = 1):
        text = inst[0]
        if inst[1]["TYPE"] is USERFUNCTION:
            text = inst[0]+"()"
        if inst[1]["TYPE"] is FUNTION :
            # function.set_move(30,40)
            text = "function." + inst[0] + "("
            if inst[1]["VARIABLES"] is not None:
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
        if inst[0] == "else" or (inst[0] in ["if", "elif"] and (inst[1]["BOTTOM"] is None or (inst[1]["BOTTOM"] is not  None and inst[1]["BOTTOM"][0] not in ["elif", "else"] ) ) ):
            text += "\n" + "\t" * (ntab - 1) +"end"
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
        button = MyButtom( ( name, {}, self.view, self.scene, pathBlocks + "/block1" + ".png", connections, variables, blockType, table, table.rowCount() - 1, VARIABLE))
        self.listButtons.append(button)
        table.setCellWidget(table.rowCount() - 1, 0, button)
        self.listVars.append(button.getAbstracBlockItem())
        for img in imgs:
            blockType, connections = self.loadConfigBlock(pathBlocks + "/" + img)
            table = self.dicTables['variables']
            table.insertRow(table.rowCount())
            button = MyButtom((name, {}, self.view, self.scene, pathBlocks + "/" + img + ".png", connections, [], blockType, table, table.rowCount() - 1, VARIABLE))
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

    def deleteWhen(self):
        self.delWhenGui = delWhen.Ui_Dialog()
        self.delWhenDialgo = QtGui.QDialog()
        self.delWhenGui.setupUi(self.delWhenDialgo)
        self.delWhenDialgo.open()
        self.delWhenGui.listWhencomboBox.clear()
        self.delWhenGui.listWhencomboBox.currentText()
        for name in self.listNameWhens:
            self.delWhenGui.listWhencomboBox.addItem(name)
        self.delWhenGui.cancelPushButton.clicked.connect(lambda :self.retdelWhenGui(0))
        self.delWhenGui.okPushButton.clicked.connect(lambda :self.retdelWhenGui(1))

    def retdelWhenGui(self, ret):
        if ret is 1:
            name = self.delWhenGui.listWhencomboBox.currentText()
            self.delWhen(name)
            self.scene.removeByNameControl(name)
        self.delWhenDialgo.close()
        if len(self.listNameWhens) == 0:
            self.ui.deleteWhenpushButton.setEnabled(False)

    def delWhen(self,name):
        table = self.dicTables['control']
        rango = reversed(range(0, table.rowCount()))
        for row in rango:
            item = table.cellWidget(row, 0)
            if item.getText() in ["active "+name, "deactive "+name]:
                item.delete(row)
                item.removeTmpFile()
                self.listButtons.remove(item)
        self.listNameWhens.remove(name)

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
            button = MyButtom((name, {}, self.view, self.scene, pathBlocks + "/" + img + ".png", connections, [], blockType, table, table.rowCount() - 1, USERFUNCTION))
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
