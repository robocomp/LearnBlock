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
from guis import addVar, guiupdatedSuccessfully, guiGui, delVar, delWhen, createFunctions as guiCreateFunctions
from learnbot_dsl.functions import *
from parserConfig import configSSH
from blocksConfig.blocks import *
print sys.version_info[0]
import git, urllib2
HEADER = """
#EXECUTION: python code_example.py config
from learnbot_dsl.functions import *
import learnbot_dsl.<LearnBotClient> as <LearnBotClient>
import sys
import time
try:
    lbot = <LearnBotClient>.Client(sys.argv)
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


# Create de streamer





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

        # Create the application
        self.app = QtGui.QApplication(sys.argv)
        # self.app.aboutToQuit.connect(self.exit)

        # Load tranlators
        self.translators = {}
        pathLanguages = {'EN': "t_en.qm", "ES": "t_es.qm"}
        for l in ['EN', 'ES']:
            translator = QtCore.QTranslator()
            print('Localization loaded: ', translator.load(pathLanguages[l], path + "/languages"))
            qttranslator = QtCore.QTranslator()
            qttranslator.load("q"+pathLanguages[l],QtCore.QLibraryInfo.location( QtCore.QLibraryInfo.TranslationsPath))
            self.translators[l] = (translator, qttranslator)
        self.currentTranslator = self.translators[getLanguage()]

        # install translators
        translator, qttranslator = self.translators[getLanguage()]
        self.app.installTranslator(translator)
        self.app.installTranslator(qttranslator)

        self.app.setWindowIcon(QtGui.QIcon(path + '/ico.png'))

        self.Dialog = QtGui.QMainWindow()
        QtGui.QMainWindow.__init__(self)
        self.ui = guiGui.Ui_MainWindow()
        self.ui.setupUi(self)
        self.showMaximized()

        self.ui.startPushButton.clicked.connect(self.StartProgramSR)
        self.ui.startPRPushButton.clicked.connect(self.StartProgramPR)
        self.ui.startPRTextPushButton.clicked.connect(lambda: self.generateTmpFilefromText(False))
        self.ui.startSRTextPushButton.clicked.connect(lambda: self.generateTmpFilefromText(True))
        self.ui.stopPushButton.clicked.connect(self.stopthread)
        self.ui.stoptextPushButton.clicked.connect(self.stopthread)
        self.ui.addVarPushButton.clicked.connect(self.newVariable)
        self.ui.addNumberpushButton.clicked.connect(lambda: self.showGuiAddNumberOrString(1))
        self.ui.addStringpushButton.clicked.connect(lambda: self.showGuiAddNumberOrString(2))
        self.ui.addWhenpushButton.clicked.connect(self.showGuiAddWhen)
        self.ui.zoompushButton.clicked.connect(self.setZoom)
        self.ui.openpushButton.clicked.connect(self.openProyect)
        self.ui.deleteVarPushButton.clicked.connect(self.deleteVar)
        self.ui.deleteWhenpushButton.clicked.connect(self.deleteWhen)
        self.ui.createFunctionsPushButton.clicked.connect(self.newUserFunctions)
        self.ui.deleteFuntionsPushButton.clicked.connect(self.deleteUserFunctions)
        self.ui.savepushButton.clicked.connect(self.saveInstance)
        self.ui.useEventscheckBox.stateChanged.connect(lambda: self.avtiveEvents(self.ui.useEventscheckBox.isChecked()))
        self.ui.language.currentIndexChanged.connect(self.changeLanguage)
        self.ui.SearchlineEdit.textChanged.connect(lambda: self.searchUpdate(self.ui.SearchlineEdit.text()))
        self.ui.actionCreate_New_block.triggered.connect(self.showCreateBlock)
        self.ui.actionSave.triggered.connect(self.saveInstance)
        self.ui.actionSave_As.triggered.connect(self.saveAs)
        self.ui.actionOpen_Proyect.triggered.connect(self.openProyect)
        self.ui.actionStart_components.triggered.connect(self.startRobot)
        self.ui.actionStart_Simulator.triggered.connect(self.startSimulatorRobot)
        self.ui.actionReboot.triggered.connect(self.rebootRobot)
        self.ui.actionShutdown.triggered.connect(self.shutdownRobot)
        self.ui.actionNew_project.triggered.connect(self.newProject)
        self.ui.actionExit.triggered.connect(self.close)
        self.ui.connectCameraRobotpushButton.clicked.connect(self.connectCameraRobot)

        self.ui.savepushButton.setIcon(QtGui.QIcon("guis/save.png"))
        self.ui.openpushButton.setIcon(QtGui.QIcon("guis/open.png"))
        self.ui.openpushButton.setFixedSize(QtCore.QSize(24, 22))
        self.ui.savepushButton.setFixedSize(QtCore.QSize(24, 22))
        self.ui.openpushButton.setIconSize(QtCore.QSize(24, 22))
        self.ui.savepushButton.setIconSize(QtCore.QSize(24, 22))
        self.ui.zoompushButton.setIcon(QtGui.QIcon("guis/zoom.png"))
        self.ui.zoompushButton.setIconSize(QtCore.QSize(30, 30))
        self.ui.zoompushButton.setFixedSize(QtCore.QSize(30, 30))
        self.ui.stopPushButton.setEnabled(False)
        self.ui.startPushButton.setEnabled(True)
        self.ui.functions.setFixedWidth(221)

        self.view = MyView(self, self.ui.frame)
        self.view.setObjectName("view")
        self.ui.verticalLayout_3.addWidget(self.view)
        self.scene = MyScene(self, self.view)
        self.view.setScene(self.scene)
        self.view.show()
        self.view.setZoom(False)
        self.ui.block2textpushButton.clicked.connect(self.blocksToText)
        self.dicTables = {'control': self.ui.tableControl, 'motor': self.ui.tableMotor,
                          'perceptual': self.ui.tablePerceptual,
                          'proprioceptive': self.ui.tablePropioperceptive, 'operador': self.ui.tableOperadores,
                          'variables': self.ui.tableVariables,
                          'funtions': self.ui.tableUserfunctions, 'express': self.ui.tableExpress,
                          'others': self.ui.tableOthers}

        for t in self.dicTables:
            table = self.dicTables[t]
            table.verticalHeader().setVisible(False)
            table.horizontalHeader().setVisible(False)
            table.setColumnCount(1)
            table.setRowCount(0)

        try:
            os.mkdir("tmp")
        except Exception as e:
            print e
            pass

        self.load_blocks()
        self.avtiveEvents(False)
        self.stream = None
        self.bytes = ''
        self.pmlast = None
        self.cameraScene = QtGui.QGraphicsScene()
        self.ui.cameragraphicsView.setScene(self.cameraScene)
        self.timerCamera = QtCore.QTimer()
        self.timerCamera.timeout.connect(self.readCamera)
        self.connectCameraRobot()

        # Check change on git repository
        pathrepo = path[0:path.rfind("/")]
        self.pathrepo = pathrepo[0:pathrepo.rfind("/")]
        try:
            urllib2.urlopen('http://216.58.192.142', timeout=1)
            self.repo = git.Repo(self.pathrepo)
            local_commit = self.repo.commit()
            remote = self.repo.remote()
            info = remote.fetch()[0]
            remote_commit = info.commit
            if local_commit.committed_date < remote_commit.committed_date:
                self.ui.updatepushButton.setVisible(True)
                self.ui.updatepushButton.clicked.connect(self.updateLearnblock)
            else:
                self.ui.updatepushButton.setVisible(False)
        except urllib2.URLError as e:
            self.ui.updatepushButton.setVisible(False)
        except Exception as e:
            self.ui.updatepushButton.setVisible(False)


        # Execute the application
        r = self.app.exec_()

        for b in self.listButtons:
            b.removeTmpFile()

        shutil.rmtree("tmp")
        sys.exit(r)


            # self.ui.camerawidget.update()
    def connectCameraRobot(self):
        try:
            self.stream = urllib2.urlopen('http://192.168.16.1:8080/?action=stream',timeout=4)
            self.timerCamera.start(5)
        except urllib2.URLError as e:
            print "Error connect Streamer\n", e

    def readCamera(self):
        self.bytes += self.stream.read(5120)
        a = self.bytes.find('\xff\xd8')
        b = self.bytes.find('\xff\xd9')
        if a != -1 and b != -1:
            jpg = self.bytes[a:b + 2]
            self.bytes = self.bytes[b + 2:]
            img = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            image = toQImage(img)
            pm = QtGui.QPixmap(image)
            if self.pmlast is not None:
                self.cameraScene.removeItem(self.pmlast)
            self.pmlast = self.cameraScene.addPixmap(pm)
            self.cameraScene.update()
            
    def closeEvent(self, event):
        if self.scene.shouldSave is False:
            self.stopthread()
            event.accept()
        else:
            msgBox = QtGui.QMessageBox()
            msgBox.setText(self.trUtf8("The document has been modified."))
            msgBox.setInformativeText(self.trUtf8("Do you want to save your changes?"))
            msgBox.setStandardButtons(QtGui.QMessageBox.Save | QtGui.QMessageBox.Discard | QtGui.QMessageBox.Cancel)
            msgBox.setDefaultButton(QtGui.QMessageBox.Save)
            ret = msgBox.exec_()
            if ret == 2048:
                self.saveInstance()
                event.accept()
            elif ret == 8388608:
                self.scene.shouldSave = False
                event.accept()
            else:
                event.ignore()

    def updateLearnblock(self):
        remote = self.repo.remote()
        remote.pull()
        if os.system(self.pathrepo + "/setupLearnBlock install") != 0:
            gui = guiupdatedSuccessfully.Ui_Updated()
            self.updatedSuccessfullydialog = QtGui.QDialog()
            gui.setupUi(self.updatedSuccessfullydialog)
            self.updatedSuccessfullydialog.open()

    def blocksToText(self):
        text=""
        if len(self.listNameVars) > 0:
            for name in self.listNameVars:
                text += name + " = None\n"
        blocks = self.scene.getListInstructions()
        code = self.parserBlocks(blocks, self.toLBotPy)
        self.ui.textCode.clear()
        self.ui.textCode.appendPlainText(text + code)

    def checkConnectionToBot(self):
        r = os.system("ping -c 1 -W 1 " + configSSH["ip"])
        return r is 0

    def startRobot(self):
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.WarningPolicy)
        client.connect(configSSH["ip"], port=22, username=configSSH["user"], password=configSSH["pass"])
        stdin, stdout, stderr = client.exec_command(configSSH["start"])

    def startSimulatorRobot(self):
        subprocess.Popen(configSSH["start_simulator"], shell=True, stdout=subprocess.PIPE)

    def shutdownRobot(self):
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.WarningPolicy)
        client.connect(configSSH["ip"], port=22, username=configSSH["user"], password=configSSH["pass"])
        stdin, stdout, stderr = client.exec_command("sudo shutdown 0")

    def rebootRobot(self):
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.WarningPolicy)
        client.connect(configSSH["ip"], port=22, username=configSSH["user"], password=configSSH["pass"])
        stdin, stdout, stderr = client.exec_command("sudo reboot 0")

    def avtiveEvents(self, isChecked):
        self.scene.useEvents(isChecked)
        self.ui.addWhenpushButton.setEnabled(isChecked)
        if not self.scene.thereisMain():
            self.mainButton.setEnabled(not isChecked)
        for b in self.listButtonsWhen:
            b.setEnabled(isChecked)

    def searchUpdate(self, text):
        currentable = self.ui.tableSearch
        currentable.clear()
        currentable.setRowCount(0)
        currentable.setColumnCount(1)
        if len(text) is not 0:
            for button in self.listButtons:
                textButtom = button.getCurrentText()
                if text in textButtom:
                    currentable.insertRow(currentable.rowCount())
                    buttonCopy = button.getCopy(currentable)
                    currentable.setCellWidget(currentable.rowCount() - 1, 0, buttonCopy)

    def newProject(self):
        if self.scene.shouldSave is False:
            # delete all whens
            auxList = copy.deepcopy(self.listNameWhens)
            for x in auxList:
                self.delWhen(x[0])
            self.listNameWhens = []
            auxList = copy.deepcopy(self.listNameVars)
            for name in auxList:
                self.delVar(name)
            self.listNameVars = []
            auxList = copy.deepcopy(self.listNameUserFunctions)
            for name in auxList:
                self.delUserFunction(name)
            self.listNameUserFunctions = []

            self.listButtonsWhen = []
            self.scene.setBlockDict({})
            self.scene.startAllblocks()
            self.listNameUserFunctions = []
            self.listNameUserFunctions = []
            self.__fileProject = None
            self.ui.deleteWhenpushButton.setEnabled(False)
            self.ui.deleteVarPushButton.setEnabled(False)
            self.ui.deleteFuntionsPushButton.setEnabled(False)
            self.setWindowTitle("Learnblock2.0")
        else:
            msgBox = QtGui.QMessageBox()
            msgBox.setText(self.trUtf8("The document has been modified."))
            msgBox.setInformativeText(self.trUtf8("Do you want to save your changes?"))
            msgBox.setStandardButtons(QtGui.QMessageBox.Save | QtGui.QMessageBox.Discard | QtGui.QMessageBox.Cancel)
            msgBox.setDefaultButton(QtGui.QMessageBox.Save)
            ret = msgBox.exec_()
            if ret == 2048:
                self.saveInstance()
                self.newProject()
            elif ret == 8388608:
                self.scene.shouldSave = False
                self.newProject()

    def setZoom(self):
        self.view.setZoom(self.ui.zoompushButton.isChecked())

    def changeLanguage(self):
        l = ["ES", "EN"]
        changeLanguageTo(l[self.ui.language.currentIndex()])

        self.app.removeTranslator(self.currentTranslator[0])
        self.app.removeTranslator(self.currentTranslator[1])
        translator, qttranslator = self.translators[l[self.ui.language.currentIndex()]]
        self.app.installTranslator(translator)
        self.app.installTranslator(qttranslator)
        # self.app.installTranslator(self.translators[l[self.ui.language.currentIndex()]])
        self.currentTranslator = self.translators[l[self.ui.language.currentIndex()]]
        self.ui.retranslateUi(self)

    def load_blocks(self):
        functions = reload_functions()
        for f in functions:
            if f.name in self.listNameBlock:
                continue
            self.listNameBlock.append(f.name)
            variables = []
            if f.variables:
                for v in f.variables:
                    variables.append(Variable(v[0], v[1], v[2]))
            funtionType = None
            HUE = None
            if "control" == f.type[0]:
                funtionType = CONTROL
                HUE = HUE_CONTROL
            elif "motor" == f.type[0]:
                funtionType = FUNTION
                HUE = HUE_MOTOR
            elif "perceptual" == f.type[0]:
                funtionType = FUNTION
                HUE = HUE_PERCEPTUAL
            elif "proprioceptive" == f.type[0]:
                funtionType = FUNTION
                HUE = HUE_PROPIOPERCEPTIVE
            elif "operador" == f.type[0]:
                funtionType = OPERATOR
                HUE = HUE_OPERATOR
            elif "express" == f.type[0]:
                funtionType = FUNTION
                HUE = HUE_EXPRESS
            elif "others" == f.type[0]:
                funtionType = FUNTION
                HUE = HUE_OTHERS

            # blockType = None
            for img in f.img:
                blockType, connections = loadConfigBlock(img)
                table = self.dicTables[f.type[0]]
                table.insertRow(table.rowCount())
                dicTrans = {}
                for l in f.translations:
                    dicTrans[l.language] = l.translation
                dicToolTip = {}
                for l in f.tooltip:
                    dicToolTip[l.language] = l.translation
                button = Block_Button((self, f.name[0], dicTrans, HUE, self.view, self.scene, img + ".png", connections,
                                       variables, blockType, table, table.rowCount() - 1, funtionType, dicToolTip))
                if f.name[0] == "main":
                    self.mainButton = button
                self.listButtons.append(button)
                table.setCellWidget(table.rowCount() - 1, 0, button)

    def execTmp(self):
        try:
            execfile("main_tmp.py")
        except:
            self.ui.stopPushButton.setEnabled(False)
            self.ui.startPushButton.setEnabled(True)
            self.ui.startPRPushButton.setEnabled(True)

    def stopExecTmp(self):
        robot = ""
        try:
            if self.physicalRobot:
                sys.argv = [' ', path + '/etc/configPhysical']
                robot = "physical"
            else:
                sys.argv = [' ', path + '/etc/configSimulate']
                robot = "simulate"

            execfile("stop_main_tmp.py", globals())
        except Exception as e:
            print e
            msgBox = QtGui.QMessageBox()
            msgBox.setText(self.trUtf8("You should check connection the" + robot + " robot"))
            msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
            msgBox.setDefaultButton(QtGui.QMessageBox.Ok)
            msgBox.exec_()

    def saveInstance(self):
        if self.__fileProject is None:
            fileName = QtGui.QFileDialog.getSaveFileName(self, 'Save Project', '.',
                                                         'Block Project file (*.blockProject)')
            file = fileName[0]
            if "." in file:
                file = file.split(".")[0]
            file = file + ".blockProject"
            if file != "":
                self.__fileProject = file
                self.saveInstance()
        else:
            self.setWindowTitle("Learnblock2.0 " + self.__fileProject)
            with open(self.__fileProject, 'wb') as fichero:
                dic = copy.deepcopy(self.scene.dicBlockItem)
                for id in dic:
                    block = dic[id]
                    block.file = block.file.replace(pathImgBlocks, "")
                pickle.dump(
                    (dic, self.listNameWhens, self.listUserFunctions, self.listNameVars, self.listNameUserFunctions),
                    fichero, 0)
        self.scene.shouldSave = False

    def saveAs(self):
        fileName = QtGui.QFileDialog.getSaveFileName(self, 'Save Project', '.', 'Block Project file (*.blockProject)')
        if fileName[0] != "":
            file = fileName[0]
            if "." in file:
                file = file.split(".")[0]
            elif fileName[1] == "Block Project file (*.blockProject)":
                file = file + ".blockProject"
                self.__fileProject = file
                self.saveInstance()

    def openProyect(self):
        if self.scene.shouldSave is False:
            self.newProject()
            fileName = QtGui.QFileDialog.getOpenFileName(self, 'Open Project', '.',
                                                         'Block Project file (*.blockProject)')
            if fileName[0] != "":
                self.__fileProject = fileName[0]
                self.setWindowTitle("Learnblock2.0 " + self.__fileProject)
                with open(self.__fileProject, 'rb') as fichero:
                    d = pickle.load(fichero)

                    dictBlock = d[0]
                    for id in dictBlock:
                        block = dictBlock[id]
                        block.file = pathImgBlocks + block.file

                    # delete all whens
                    auxList = copy.deepcopy(self.listNameWhens)
                    for x in auxList:
                        self.delWhen(x[0])
                    self.listNameWhens = []

                    for x in d[1]:
                        self.addButtonsWhens(x[1], x[0])
                    self.listNameWhens = d[1]

                    auxList = copy.deepcopy(self.listNameVars)
                    for name in auxList:
                        self.delVar(name)
                    self.listNameVars = []

                    for name in d[3]:
                        self.addVariable(name)
                    self.listNameVars = d[3]

                    auxList = copy.deepcopy(self.listNameUserFunctions)
                    for name in auxList:
                        self.delUserFunction(name)
                    self.listNameUserFunctions = []

                    for name in d[4]:
                        self.addUserFunction(name)
                    self.listNameUserFunctions = d[4]

                    self.scene.setBlockDict(d[0])
                    self.scene.startAllblocks()
                    self.scene.useEvents(self.ui.useEventscheckBox.isChecked())
        else:
            msgBox = QtGui.QMessageBox()
            msgBox.setText(self.trUtf8("The document has been modified."))
            msgBox.setInformativeText(self.trUtf8("Do you want to save your changes?"))
            msgBox.setStandardButtons(QtGui.QMessageBox.Save | QtGui.QMessageBox.Discard | QtGui.QMessageBox.Cancel)
            msgBox.setDefaultButton(QtGui.QMessageBox.Save)
            ret = msgBox.exec_()
            if ret == 2048:
                self.saveInstance()
            elif ret == 8388608:
                self.scene.shouldSave = False
                self.openProyect()

    def showCreateBlock(self):
        self.createBlockGui = guiCreateBlock(self.load_blocks)
        # self.createBlockGui.ui.pushButtonOK.clicked.connect(self.load_blocks)
        self.createBlockGui.open()

    def showGuiAddNumberOrString(self, type):
        self.addNumberOrStringGui = guiAddNumberOrString(type)
        self.addNumberOrStringGui.ui.pushButtonOK.clicked.connect(self.addBlockNumberOrString)
        self.addNumberOrStringGui.open()

    def addBlockNumberOrString(self):
        text = self.addNumberOrStringGui.value
        imgPath = self.addNumberOrStringGui.imgName
        configImgPath = imgPath.replace(".png", "")
        blockType, connections = loadConfigBlock(configImgPath)
        block = AbstractBlock(0, 0, text, {}, imgPath, [], HUE_NUMBER, "", connections, blockType, VARIABLE)
        self.scene.addItem(block)

    def showGuiAddWhen(self):
        self.addWhenGui = guiAddWhen()
        self.addWhenGui.ui.pushButtonOK.clicked.connect(self.addBlockWhen)
        self.addWhenGui.open()

    def addBlockWhen(self):
        if self.addWhenGui.isOk:
            text = self.addWhenGui.value
            imgPath = self.addWhenGui.imgName
            configImgPath = imgPath.replace(".png", "")
            blockType, connections = loadConfigBlock(configImgPath)

            block = AbstractBlock(0, 0, text, {'ES': "Cuando ", 'EN': "When "}, imgPath, [], HUE_WHEN,
                                  self.addWhenGui.nameControl.replace(" ", "_"), connections, blockType, WHEN)
            self.scene.addItem(block)
            if self.addWhenGui.nameControl != "start":
                self.addButtonsWhens(configImgPath, self.addWhenGui.nameControl.replace(" ", "_"))

    def addButtonsWhens(self, configImgPath, name):
        if configImgPath.split('/')[-1] == 'block8':
            blockType, connections = loadConfigBlock(pathBlocks + "/block1")
            table = self.dicTables['control']

            table.insertRow(table.rowCount())
            button = Block_Button((self, "activate " + name, {'ES': "Activar " + name, 'EN': "Activate " + name}, HUE_WHEN,
                                   self.view, self.scene, pathBlocks + "/block1" + ".png", connections, [], blockType,
                                   table, table.rowCount() - 1, VARIABLE,
                                   {'ES': "Activa el evento " + name, 'EN': "Activate the event " + name}))
            self.listButtonsWhen.append(button)
            self.listButtons.append(button)
            table.setCellWidget(table.rowCount() - 1, 0, button)

            table.insertRow(table.rowCount())
            button = Block_Button((self, "deactivate " + name, {'ES': "Desactivar " + name, 'EN': "Deactivate " + name}, HUE_WHEN,
                                   self.view, self.scene, pathBlocks + "/block1" + ".png", connections, [], blockType,
                                   table, table.rowCount() - 1, VARIABLE,
                                   {'ES': "Desactiva el evento " + name, 'EN': "Deactivate the event " + name}))
            self.listButtonsWhen.append(button)
            self.listButtons.append(button)
            table.setCellWidget(table.rowCount() - 1, 0, button)

        table = self.dicTables['control']
        for x in ["/block2", "/block3", "/block4"]:
            blockType, connections = loadConfigBlock(pathBlocks + x)

            table.insertRow(table.rowCount())
            button = Block_Button((self, "time_" + name, {'ES': "Tiempo_" + name, 'EN': "Time_" + name}, HUE_WHEN, self.view,
                                   self.scene, pathBlocks + x + ".png", connections, [], blockType, table,
                                   table.rowCount() - 1, VARIABLE,
                                   {'ES': "Es el numero de segundos que lleva en ejecucion el evento " + name,
                                    'EN': " " + name}))
            self.listButtonsWhen.append(button)
            self.listButtons.append(button)
            table.setCellWidget(table.rowCount() - 1, 0, button)

        self.listNameWhens.append((name, configImgPath))
        self.ui.deleteWhenpushButton.setEnabled(True)

    def StartProgramSR(self):
        self.physicalRobot = False
        self.generateTmpFile()

    def StartProgramPR(self):
        if self.checkConnectionToBot():
            self.physicalRobot = True
            self.generateTmpFile()
        else:
            msgBox = QtGui.QMessageBox()
            msgBox.setText(self.trUtf8("You should check connection the physical robot"))
            msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
            msgBox.setDefaultButton(QtGui.QMessageBox.Ok)
            msgBox.exec_()

    def generateTmpFilefromText(self, simulated):
        self.physicalRobot = not simulated
        self.generateTmpFile(False)
        pass

    def generateTmpFile(self, fromBlocks = True):
        text = ""
        if fromBlocks:
            blocks = self.scene.getListInstructions()
            if len(self.listNameVars) > 0:
                for name in self.listNameVars:
                    text += name + " = None\n"
        robot = ""
        if self.physicalRobot:
            sys.argv = [' ', path + '/etc/configPhysical']
            robot = "physical"
        else:
            sys.argv = [' ', path + '/etc/configSimulate']
            robot = "simulate"


        if not fromBlocks or blocks is not None:
            if fromBlocks:
                code = self.parserBlocks(blocks, self.toLBotPy)
                self.ui.textCode.clear()
                self.ui.textCode.appendPlainText(text + code)
            else:
                code = self.ui.textCode.toPlainText()

            fh = open("main_tmp.lb", "wr")
            fh.writelines(text + code)
            fh.close()

            try:
                if not parserLearntBotCode("main_tmp.lb", "main_tmp.py", self.physicalRobot):
                    msgBox = QtGui.QMessageBox()
                    msgBox.setText(self.trUtf8("Your code is empty or is not correct"))
                    msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
                    msgBox.setDefaultButton(QtGui.QMessageBox.Ok)
                    msgBox.exec_()
            except Exception as e:
                msgBox = QtGui.QMessageBox()
                msgBox.setText(self.trUtf8("line: {}".format(e.line) + "\n    " + " " * e.col + "^"))
                msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
                msgBox.setDefaultButton(QtGui.QMessageBox.Ok)
                msgBox.exec_()
                return
            if compile("main_tmp.py"):
                try:
                    if not self.physicalRobot:
                        LearnBotClient.Client(sys.argv)
                    self.hilo = Process(target=self.execTmp)
                    self.hilo.start()
                    self.ui.stopPushButton.setEnabled(True)
                    self.ui.startPushButton.setEnabled(False)
                    self.ui.startPRPushButton.setEnabled(False)
                    self.ui.stoptextPushButton.setEnabled(True)
                    self.ui.startSRTextPushButton.setEnabled(False)
                    self.ui.startPRTextPushButton.setEnabled(False)
                except:
                    msgBox = QtGui.QMessageBox()
                    msgBox.setText(self.trUtf8("You should check connection the " + robot + " robot"))
                    msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
                    msgBox.setDefaultButton(QtGui.QMessageBox.Ok)
                    msgBox.exec_()

            else:
                msgBox = QtGui.QMessageBox()
                msgBox.setText(self.trUtf8("Your code has an error. Check it out again"))
                msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
                msgBox.setDefaultButton(QtGui.QMessageBox.Ok)
                msgBox.exec_()

    def generateStopTmpFile(self):
        if self.physicalRobot:
            text = HEADER.replace('<LearnBotClient>', 'LearnBotClient_PhysicalRobot')
            sys.argv = [' ', 'configPhysical']
        else:
            text = HEADER.replace('<LearnBotClient>', 'LearnBotClient')
            sys.argv = [' ', 'config']
        text += '\nfunctions.get("stop_bot")(lbot)'
        fh = open("stop_main_tmp.py", "wr")
        fh.writelines(text)
        fh.close()

    def stopthread(self):
        try:
            self.hilo.terminate()
            self.generateStopTmpFile()
            self.stopExecTmp()
            self.ui.stopPushButton.setEnabled(False)
            self.ui.startPushButton.setEnabled(True)
            self.ui.startPRPushButton.setEnabled(True)
            self.ui.stoptextPushButton.setEnabled(False)
            self.ui.startPRTextPushButton.setEnabled(True)
            self.ui.startSRTextPushButton.setEnabled(True)
        except Exception as e:

            pass

    def parserBlocks(self, blocks, function):  # TODO add parser for blocks when
        text = self.parserUserFuntions(blocks, function)
        text += "\n\n"
        if self.ui.useEventscheckBox.isChecked():
            text += self.parserWhenBlocks(blocks, function)
        else:
            text += self.parserOtherBlocks(blocks, function)
        return text

    def parserUserFuntions(self, blocks, function):
        text = ""
        for b in blocks:
            if b[1]["TYPE"] is USERFUNCTION:
                text += "def " + function(b, 1)
                text += "\nend\n\n"
        return text

    def parserWhenBlocks(self, blocks, function):
        text = ""
        for b in blocks:
            if b[0] == "when":
                text += "when " + b[1]['NAMECONTROL']
                if b[1]['RIGHT'] is not None:
                    text += " = " + function(b[1]['RIGHT'], 0)
                text += ":\n"

                if b[1]['BOTTOMIN'] is not None:
                    text += "\t" + function(b[1]['BOTTOMIN'], 2) + "\n"
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
                    text += "\t" + function(b[1]["BOTTOMIN"], 2)
                else:
                    text += "pass"
                text += "\nend\n\n"
        return text

    def toLBotPy(self, inst, ntab=1):
        text = inst[0]
        if inst[1]["TYPE"] is USERFUNCTION:
            text = inst[0] + "()"
        if inst[1]["TYPE"] is CONTROL:
            if inst[1]["VARIABLES"] is not None:
                text = inst[0] + "("
                for var in inst[1]["VARIABLES"]:
                    text += var + ", "
                text = text[0:-2] + ""
                text += ")"
        if inst[1]["TYPE"] is FUNTION:
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
        if inst[0] == "while":
            text += "\n\t" * (ntab - 1) + "end"
        if inst[0] == "else" or (inst[0] in ["if", "elif"] and (inst[1]["BOTTOM"] is None or (
                inst[1]["BOTTOM"] is not None and inst[1]["BOTTOM"][0] not in ["elif", "else"]))):
            text += "\n" + "\t" * (ntab - 1) + "end"
        if inst[1]["BOTTOM"] is not None:
            text += "\n" + "\t" * (ntab - 1) + self.toLBotPy(inst[1]["BOTTOM"], ntab)
        return text

    def newVariable(self):
        self.addVarGui = addVar.Ui_Dialog()
        self.addVarDialog = QtGui.QDialog()
        self.addVarGui.setupUi(self.addVarDialog)
        self.addVarDialog.open()
        self.addVarGui.cancelPushButton.clicked.connect(lambda: self.retaddVarGui(0))
        self.addVarGui.okPushButton.clicked.connect(lambda: self.retaddVarGui(1))

    def retaddVarGui(self, ret):
        if ret is 1:
            name = self.addVarGui.nameLineEdit.text()
            name = name.replace(" ", "_")
            if name in self.listNameVars:
                msgBox = QtGui.QMessageBox()
                msgBox.setText(self.trUtf8("This name alredy exist"))
                msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
                msgBox.setDefaultButton(QtGui.QMessageBox.Ok)
                ret = msgBox.exec_()
                return
            if len(name) != 0 and name[0].isdigit():
                msgBox = QtGui.QMessageBox()
                msgBox.setText(self.trUtf8("The name can't start by number"))
                msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
                msgBox.setDefaultButton(QtGui.QMessageBox.Ok)
                ret = msgBox.exec_()
                return
            if len(name) == 0:
                msgBox = QtGui.QMessageBox()
                msgBox.setText(self.trUtf8("Error Name is empty."))
                msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
                msgBox.setDefaultButton(QtGui.QMessageBox.Ok)
                ret = msgBox.exec_()
                return
            self.addVariable(name)

        self.addVarDialog.close()

    def addVariable(self, name):
        self.ui.deleteVarPushButton.setEnabled(True)
        imgs = ['block2', 'block3', 'block4']

        self.listNameVars.append(name)
        blockType, connections = loadConfigBlock(pathBlocks + "/block1")
        table = self.dicTables['variables']
        table.insertRow(table.rowCount())
        variables = []
        variables.append(Variable("float", "set to ", "0"))
        button = Block_Button((self, name, {}, HUE_WHEN, self.view, self.scene, pathBlocks + "/block1" + ".png", connections,
                               variables, blockType, table, table.rowCount() - 1, VARIABLE, {}))
        self.listButtons.append(button)
        table.setCellWidget(table.rowCount() - 1, 0, button)
        self.listVars.append(button.getAbstracBlockItem())
        for img in imgs:
            blockType, connections = loadConfigBlock(pathBlocks + "/" + img)
            table = self.dicTables['variables']
            table.insertRow(table.rowCount())
            button = Block_Button((self, name, {}, HUE_VARIABLE, self.view, self.scene, pathBlocks + "/" + img + ".png", connections,
                                   [], blockType, table, table.rowCount() - 1, VARIABLE, {}))
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
        self.delVarGui.cancelPushButton.clicked.connect(lambda: self.retdelVarGui(0))
        self.delVarGui.okPushButton.clicked.connect(lambda: self.retdelVarGui(1))

    def retdelVarGui(self, ret):
        if ret is 1:
            name = self.delVarGui.listVarcomboBox.currentText()
            self.delVar(name)
        self.delVarDialgo.close()
        if len(self.listNameVars) == 0:
            self.ui.deleteVarPushButton.setEnabled(False)

    def delVar(self, name):
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
        for x in self.listNameWhens:
            self.delWhenGui.listWhencomboBox.addItem(x[0])
        self.delWhenGui.cancelPushButton.clicked.connect(lambda: self.retdelWhenGui(0))
        self.delWhenGui.okPushButton.clicked.connect(lambda: self.retdelWhenGui(1))

    def retdelWhenGui(self, ret):
        if ret is 1:
            name = self.delWhenGui.listWhencomboBox.currentText()
            self.delWhen(name)
            self.scene.removeByNameControl(name)
        self.delWhenDialgo.close()
        if len(self.listNameWhens) == 0:
            self.ui.deleteWhenpushButton.setEnabled(False)

    def delWhen(self, name):
        table = self.dicTables['control']
        rango = reversed(range(0, table.rowCount()))
        for row in rango:
            item = table.cellWidget(row, 0)
            if item.getText() in ["activate " + name, "deactivate " + name, "time_" + name]:
                item.delete(row)
                item.removeTmpFile()
                self.listButtons.remove(item)
        for x in self.listNameWhens:
            if x[0] == name:
                self.listNameWhens.remove(x)
        self.scene.removeWhenByName(name)
        if len(self.listNameWhens) is 0:
            self.ui.deleteWhenpushButton.setEnabled(False)

    def newUserFunctions(self):
        self.userFunctionsGui = guiCreateFunctions.Ui_Dialog()
        self.userFunctionsDialgo = QtGui.QDialog()
        self.userFunctionsGui.setupUi(self.userFunctionsDialgo)
        self.userFunctionsDialgo.open()
        self.userFunctionsGui.cancelPushButton.clicked.connect(lambda: self.retUserFunctions(0))
        self.userFunctionsGui.okPushButton.clicked.connect(lambda: self.retUserFunctions(1))

    def retUserFunctions(self, ret):
        if ret is 1:
            name = self.userFunctionsGui.nameLineEdit.text()
            name = name.replace(" ", "_")
            if name in self.listNameUserFunctions:
                msgBox = QtGui.QMessageBox()
                msgBox.setText(self.trUtf8("This name alredy exist"))
                msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
                msgBox.setDefaultButton(QtGui.QMessageBox.Ok)
                ret = msgBox.exec_()
                return
            if len(name) != 0 and name[0].isdigit():
                msgBox = QtGui.QMessageBox()
                msgBox.setText(self.trUtf8("The name can't start by number"))
                msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
                msgBox.setDefaultButton(QtGui.QMessageBox.Ok)
                ret = msgBox.exec_()
                return
            if len(name) == 0:
                msgBox = QtGui.QMessageBox()
                msgBox.setText(self.trUtf8("Error Name is empty."))
                msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
                msgBox.setDefaultButton(QtGui.QMessageBox.Ok)
                ret = msgBox.exec_()
                return
            self.addUserFunction(name)

        self.userFunctionsDialgo.close()

    def addUserFunction(self, name):
        self.ui.deleteFuntionsPushButton.setEnabled(True)
        imgs = ['block8', 'block1']
        self.listNameUserFunctions.append(name)
        table = self.dicTables['funtions']
        i = 0
        for img in imgs:
            blockType, connections = loadConfigBlock(pathBlocks + "/" + img)
            table.insertRow(table.rowCount())
            button = Block_Button((self, name, {}, HUE_USERFUNCTION, self.view, self.scene, pathBlocks + "/" + img + ".png", connections,
                                   [], blockType, table, table.rowCount() - 1, USERFUNCTION, {}))
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

    def retdelUserFunctionsGui(self, ret):
        if ret is 1:
            name = self.delUserFunctionsGui.listVarcomboBox.currentText()
            self.delUserFunction(name)
        self.delUserFunctionsDialgo.close()
        if len(self.listNameUserFunctions) == 0:
            self.ui.deleteFuntionsPushButton.setEnabled(False)

    def delUserFunction(self, name):
        table = self.dicTables['funtions']
        rango = reversed(range(0, table.rowCount()))
        for row in rango:
            item = table.cellWidget(row, 0)
            if item.getText() == name:
                item.delete(row)
                item.removeTmpFile()
                self.listButtons.remove(item)
        self.listNameUserFunctions.remove(name)