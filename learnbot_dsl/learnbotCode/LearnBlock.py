#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import
import sys, os, pickle, tempfile, shutil, subprocess, io, socket, struct, numpy as np, cv2, paho.mqtt.client, time, requests, paramiko
from PIL import Image
from pyunpack import Archive

from multiprocessing import Process

from learnbot_dsl.learnbotCode.AbstractBlock import *
from learnbot_dsl.learnbotCode.Button import *
from learnbot_dsl.learnbotCode.Scene import *
from learnbot_dsl.learnbotCode.View import *
from learnbot_dsl.blocksConfig.parserConfigBlock import reload_functions
from learnbot_dsl.learnbotCode.checkFile import compile
from learnbot_dsl.learnbotCode.dialogAddNumberOrString import *
from learnbot_dsl.learnbotCode.guiCreateBlock import *
from learnbot_dsl.learnbotCode.guiaddWhen import *
import learnbot_dsl.guis.Learnblock as Learnblock
from learnbot_dsl.guis import pathGuis
import learnbot_dsl.guis.AddVar as AddVar
import learnbot_dsl.guis.DelWhen as DelWhen
import learnbot_dsl.guis.CreateFunctions as CreateFunctions
import learnbot_dsl.guis.DelVar as DelVar
from learnbot_dsl.learnbotCode.Language import changeLanguageTo
from learnbot_dsl.learnbotCode.parserConfig import configSSH
from learnbot_dsl.blocksConfig.blocks import *
from learnbot_dsl.learnbotCode.guiTabLibrary import Library
from learnbot_dsl.learnbotCode.Highlighter import *
from future.standard_library import install_aliases
install_aliases()
from urllib.request import urlopen
from urllib.error import URLError

path = os.path.dirname(os.path.realpath(__file__))

class DownloadThread(QtCore.QThread):
    def __init__(self, url, tmp_file_name, downloading_window):
        QtCore.QThread.__init__(self)
        self.url = url
        self.tmp_file_name = tmp_file_name
        self.downloading_window = downloading_window

    def run(self):
        u = urlopen(self.url)
        with open(self.tmp_file_name, 'wb') as f:
            downloaded_bytes = 0
            block_size = 1024 * 8
            while True:
                buffer = u.read(block_size)
                if not buffer:
                    break

                f.write(buffer)
                downloaded_bytes += block_size
        self.downloading_window.finish = True
        return

class DownloadingWindow(QtGui.QWidget):
    def __init__(self, parent, text, titel ):
        QtGui.QWidget.__init__(self)
        self.parent = parent
        vbox = QtGui.QVBoxLayout()
        self.setWindowTitle(titel)
        label = QtGui.QLabel(text)
        label.setAlignment(QtCore.Qt.AlignCenter)
        vbox.addWidget(label)

        self.progress_bar = QtGui.QProgressBar()
        self.progress_bar.setAlignment(QtCore.Qt.AlignCenter)
        vbox.addWidget(self.progress_bar)
        self.setLayout(vbox)
        self.setGeometry(300, 300, 300, 50)
        self.progress_bar.setRange(0,0)
        self.move(self.parent.pos() + self.parent.rect().center() - self.rect().center())
        self.finish = False
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.run)
        self.timer.start(100)

    def run(self):
        if self.finish:
            self.close()

def internet_on():
    try:
        urlopen('http://216.58.192.142', timeout=1)
        return True
    except URLError as err:
        return False

# Create de streamer
class MySignal(QtCore.QObject):
    signalUpdateStreamer = QtCore.Signal(QtGui.QImage)

signal = None
def on_message(client, userdata, message):
    global signal
    data = message.payload
    image_stream = io.BytesIO()
    image_stream.write(data)
    image = Image.open(image_stream)
    open_cv_image = np.array(image)
    image = toQImage(open_cv_image)
    try:
        signal.signalUpdateStreamer[QtGui.QImage].emit(image)
    except:
        pass
type2Values = {"control": (CONTROL,HUE_CONTROL),
                 "motor": (FUNTION, HUE_MOTOR),
                 "perceptual": (FUNTION, HUE_PERCEPTUAL),
                 "proprioceptive": (FUNTION, HUE_PROPIOPERCEPTIVE),
                 "operador": (OPERATOR, HUE_OPERATOR),
                 "express": (FUNTION, HUE_EXPRESS),
                 "others": (FUNTION, HUE_OTHERS)
                 }
class LearnBlock(QtGui.QMainWindow):

    def __init__(self):
        global signal
        self.signal = MySignal()
        self.signal.signalUpdateStreamer[QtGui.QImage].connect(self.readCamera)
        signal = self.signal
        self.listNameUserFunctions = []
        self.listNameVars = []
        self.listNameBlock = []
        self.listNameWhens = []
        self.listButtonsWhen = []
        self.listVars = []
        self.listUserFunctions = []
        self.listButtons = []
        self.listBlock = []
        self.listLibrary =[]
        self.listLibraryWidget = []
        self.listNameLibraryFunctions = []
        self.__fileProject = None
        self.hilo = None
        self.physicalRobot = False
        self.index = -1
        # Create the application
        self.app = QtGui.QApplication(sys.argv)

        # Load tranlators
        self.translators = {}
        pathLanguages = {'EN': "t_en.qm", "ES": "t_es.qm"}
        for k, v in iter(pathLanguages.items()):
            translator = QtCore.QTranslator()
            print('Localization loaded: ', os.path.join("languages", v), translator.load(v, os.path.join(path , "languages")))
            qttranslator = QtCore.QTranslator()
            qttranslator.load("q"+v,QtCore.QLibraryInfo.location( QtCore.QLibraryInfo.TranslationsPath))
            self.translators[k] = (translator, qttranslator)
        self.currentTranslator = self.translators[getLanguage()]

        # install translators
        translator, qttranslator = self.translators[getLanguage()]
        self.app.installTranslator(translator)
        self.app.installTranslator(qttranslator)

        self.app.setWindowIcon(QtGui.QIcon(os.path.join(path, 'Learnbot_ico.png')))

        self.Dialog = QtGui.QMainWindow()
        QtGui.QMainWindow.__init__(self)
        self.ui = Learnblock.Ui_MainWindow()
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
        self.ui.openpushButton.clicked.connect(self.openProject)
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
        self.ui.actionOpen_Project.triggered.connect(self.openProject)
        self.ui.actionStart_components.triggered.connect(self.startRobot)
        self.ui.actionStart_Simulator.triggered.connect(self.startSimulatorRobot)
        self.ui.actionReboot.triggered.connect(self.rebootRobot)
        self.ui.actionShutdown.triggered.connect(self.shutdownRobot)
        self.ui.actionNew_project.triggered.connect(self.newProject)
        self.ui.actionLoad_Library.triggered.connect(self.addLibrary)
        self.ui.actionDownload_xmls.triggered.connect(self.downloadXMLs)
        self.ui.actionDownload_examples.triggered.connect(self.downloadExamples)
        self.ui.actionDownload_libraries.triggered.connect(self.downloadLibraries)
        self.ui.actionExit.triggered.connect(self.close)
        self.ui.actionChange_Libraries_path.triggered.connect(self.changeLibraryPath)
        self.ui.actionChange_Workspace.triggered.connect(self.changeWorkSpace)
        self.ui.connectCameraRobotpushButton.clicked.connect(self.connectCameraRobot)
        self.ui.spinBoxLeterSize.valueChanged.connect(self.updateTextCodeStyle)
        self.ui.textCode.textChanged.connect(self.updateTextCodeStyle)
        self.ui.actionRedo.triggered.connect(self.redo)
        self.ui.actionUndo.triggered.connect(self.undo)
        self.ui.actionStart_simulated_robot.triggered.connect(self.StartProgramSR)
        self.ui.actionStart_physical_robot.triggered.connect(self.StartProgramPR)
        self.ui.actionStop.triggered.connect(self.stopthread)
        self.ui.actionBlocks_to_text.triggered.connect(self.blocksToText)

        # Load image buttons
        self.ui.savepushButton.setIcon(QtGui.QIcon(os.path.join(pathGuis,"save.png")))
        self.ui.openpushButton.setIcon(QtGui.QIcon(os.path.join(pathGuis,"open.png")))
        self.ui.openpushButton.setFixedSize(QtCore.QSize(24, 22))
        self.ui.savepushButton.setFixedSize(QtCore.QSize(24, 22))
        self.ui.openpushButton.setIconSize(QtCore.QSize(24, 22))
        self.ui.savepushButton.setIconSize(QtCore.QSize(24, 22))
        self.ui.zoompushButton.setIcon(QtGui.QIcon(os.path.join(pathGuis,"zoom.png")))
        self.ui.zoompushButton.setIconSize(QtCore.QSize(30, 30))
        self.ui.zoompushButton.setFixedSize(QtCore.QSize(30, 30))

        self.disablestartButtons(False)
        self.ui.functions.setFixedWidth(221)

        self.view = MyView(self, self.ui.frame)
        self.view.setObjectName("view")
        self.ui.verticalLayout_3.addWidget(self.view)
        self.scene = MyScene(self, self.view)
        self.view.setScene(self.scene)
        self.view.show()
        self.view.setZoom(False)
        self.ui.actionDuplicate.triggered.connect(self.scene.duplicateBlock)
        self.ui.actionEdit.triggered.connect(self.scene.editBlock)
        self.ui.actionDelete.triggered.connect(self.scene.deleteBlock)
        self.ui.actionExport_Block.triggered.connect(self.scene.exportBlock)

        self.ui.block2textpushButton.clicked.connect(self.blocksToText)
        self.dicTables = {'control': self.ui.tableControl, 'motor': self.ui.tableMotor,
                          'perceptual': self.ui.tablePerceptual,
                          'proprioceptive': self.ui.tablePropioperceptive, 'operador': self.ui.tableOperadores,
                          'variables': self.ui.tableVariables,
                          'funtions': self.ui.tableUserfunctions, 'express': self.ui.tableExpress,
                          'others': self.ui.tableOthers}

        self.highlighter = Highlighter(self.ui.textCode.document())
        self.updateTextCodeStyle()
        self.listBackUps = []
        for t in self.dicTables:
            table = self.dicTables[t]
            table.verticalHeader().setVisible(False)
            table.horizontalHeader().setVisible(False)
            table.setColumnCount(1)
            table.setRowCount(0)

        self.ui.updatepushButton.setVisible(False)

        self.lopenRecent = []

        tempfile.tempdir = os.path.join(os.getenv('HOME'), ".learnblock")
        if not os.path.exists(tempfile.gettempdir()):
            tempfile.tempdir = os.path.join(os.getenv('HOME'), ".learnblock")
            os.mkdir(tempfile.gettempdir())
            os.mkdir(os.path.join(tempfile.gettempdir(), "block"))
            os.mkdir(os.path.join(tempfile.gettempdir(), "functions"))
            with open(os.path.join(tempfile.gettempdir(), "__init__.py"), 'w') as f:
                f.write("")
        self.loadConfigFile()
        self.menuOpenRecent = QtGui.QMenu()
        self.ui.actionOpen_Recent.setMenu(self.menuOpenRecent)

        self.updateOpenRecent()

        self.load_blocks()
        self.avtiveEvents(False)
        self.pmlast = None
        self.cameraScene = QtGui.QGraphicsScene()
        self.ui.cameragraphicsView.setScene(self.cameraScene)

        self.connectCameraRobot()

        self.client=None
        self.isOpen = True
        self.savetmpProject()
        # Execute the application
        subprocess.Popen("aprilTag.py", shell=True, stdout=subprocess.PIPE)
        subprocess.Popen("emotionrecognition2.py", shell=True, stdout=subprocess.PIPE)
        r = self.app.exec_()

        sys.exit(r)

    def disablestartButtons(self, disabled):
        self.ui.stopPushButton.setEnabled(disabled)
        self.ui.startPushButton.setEnabled(not disabled)
        self.ui.startPRPushButton.setEnabled(not disabled)
        self.ui.stoptextPushButton.setEnabled(disabled)
        self.ui.startSRTextPushButton.setEnabled(not disabled)
        self.ui.startPRTextPushButton.setEnabled(not disabled)
        self.ui.actionStart_simulated_robot.setEnabled(not disabled)
        self.ui.actionStart_physical_robot.setEnabled(not disabled)
        self.ui.actionStop.setEnabled(disabled)

    def redo(self):
        self.isOpen = False
        self.scene.shouldSave = False
        if self.index<len(self.listBackUps)-1:
            self.index += 1
            self.openProject(self.listBackUps[self.index], False)
        self.isOpen = True

    def undo(self):
        self.isOpen = False
        self.scene.shouldSave = False
        if self.index is not 0:
            self.index -= 1
            self.openProject(self.listBackUps[self.index], False)
        self.isOpen = True

    def savetmpProject(self):
        if self.isOpen:
            aux = tempfile.gettempdir()
            tempfile.tempdir = tempfile._get_default_tempdir()
            if self.index + 1 != len(self.listBackUps):
                for f in self.listBackUps[self.index+1:]:
                    os.remove(f)
                    self.listBackUps = self.listBackUps[:self.index+1]
                self.savetmpProject()
            elif len(self.listBackUps) < 30:
                with tempfile.NamedTemporaryFile(delete=False, suffix="lb.bk") as f:
                    dic = copy.deepcopy(self.scene.dicBlockItem)
                    for id in dic:
                        block = dic[id]
                        block.file = os.path.basename(block.file)
                    pickle.dump(
                        (dic, self.listNameWhens, self.listUserFunctions, self.listNameVars, self.listNameUserFunctions,
                         [x[0] for x in self.listLibrary]),
                        f, protocol=0)
                    self.listBackUps.append(f.name)
                    self.index = self.listBackUps.index(f.name)
            else:
                os.remove(self.listBackUps[0])
                self.listBackUps = self.listBackUps[1:]
                self.index -= 1
                self.savetmpProject()
            tempfile.tempdir = aux

    def updateOpenRecent(self):
        if self.__fileProject is not None:
            if self.__fileProject not in self.lopenRecent:
                self.lopenRecent.insert(0, self.__fileProject)
            else:
                self.lopenRecent.insert(0, self.lopenRecent.pop(self.lopenRecent.index(self.__fileProject)))
        self.menuOpenRecent.clear()
        lqA = []
        self.lopenRecent = [p for p in self.lopenRecent if os.path.exists(p)]
        for f,i in zip(self.lopenRecent, range(len(self.lopenRecent))):
            if i == 9:
                break
            name, ext = os.path.splitext(f)
            name = os.path.basename(name)
            qA =(QtGui.QAction(name, self.ui.actionOpen_Recent))
            qA.setShortcut("Ctrl+Shift+"+str(i+1))
            qA.triggered.connect(lambda f=f: self.openProject(f))
            self.menuOpenRecent.addAction(qA)

    def updateTextCodeStyle(self):
        font = QtGui.QFont()
        font.setFamily('Courier')
        font.setFixedPitch(True)
        font.setPointSize(self.ui.spinBoxLeterSize.value())
        self.ui.textCode.setFont(font)
        self.ui.textCode.setTextColor(QtCore.Qt.white)
        self.ui.textCode.setCursorWidth(2)
        p = self.ui.textCode.palette()
        p.setColor(self.ui.textCode.viewport().backgroundRole(), QtGui.QColor(101, 101, 101, 255))
        self.ui.textCode.setPalette(p)

    def loadConfigFile(self):
        self.confFile = os.path.join(tempfile.gettempdir(), ".learnblock.conf")
        if not os.path.exists(self.confFile):
            with open(self.confFile,'wb') as confFile:
                while True:
                    self.workSpace = QtGui.QFileDialog.getExistingDirectory(self, self.trUtf8('Choose workspace directory'), os.environ.get('HOME'),
                                                                  QtGui.QFileDialog.ShowDirsOnly)
                    if self.workSpace is "":
                        msgBox = QtGui.QMessageBox()
                        msgBox.setWindowTitle(self.trUtf8("Warning"))
                        msgBox.setIcon(QtGui.QMessageBox.Warning)
                        msgBox.setText(self.trUtf8("Workspace is empty"))
                        msgBox.setInformativeText(self.trUtf8("The working directory will be created in") + os.path.join(os.environ.get('HOME'), "learnbotWorkSpace"))
                        msgBox.setStandardButtons(QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
                        msgBox.setDefaultButton(QtGui.QMessageBox.Cancel)
                        ret = msgBox.exec_()
                        if ret == QtGui.QMessageBox.Ok:
                            self.workSpace = os.path.join(os.environ.get('HOME'), "learnbotWorkSpace")
                            os.mkdir(self.workSpace)
                            break
                    else:
                        self.workSpace = os.path.join(self.workSpace)
                        break
                while True:
                    self.libraryPath = QtGui.QFileDialog.getExistingDirectory(self, self.trUtf8('Choose the libraries directory'), os.environ.get('HOME'),
                                                                  QtGui.QFileDialog.ShowDirsOnly)
                    if self.libraryPath is "":
                        msgBox = QtGui.QMessageBox()
                        msgBox.setWindowTitle(self.trUtf8("Warning"))
                        msgBox.setIcon(QtGui.QMessageBox.Warning)
                        msgBox.setText(self.trUtf8("Workspace is empty"))
                        msgBox.setInformativeText(self.trUtf8("The libraries directory will be ") + os.environ.get('HOME'))
                        msgBox.setStandardButtons(QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
                        msgBox.setDefaultButton(QtGui.QMessageBox.Cancel)
                        ret = msgBox.exec_()
                        if ret == QtGui.QMessageBox.Ok:
                            self.libraryPath = os.environ.get('HOME')
                            break
                    else:
                        break
                pickle.dump((self.workSpace, self.ui.language.currentIndex(), self.libraryPath, self.lopenRecent), confFile, protocol=0)

        else:
            with open(self.confFile, 'rb') as fichero:
                d = pickle.load(fichero)
                self.workSpace = d[0]
                self.ui.language.setCurrentIndex(d[1])
                self.libraryPath = d[2]
                try:
                    self.lopenRecent = d[3]
                except Exception as e:
                    pass

    def changeWorkSpace(self):
        newworkSpace = QtGui.QFileDialog.getExistingDirectory(self, self.trUtf8('Choose workspace directory'),
                                                                self.workSpace,
                                                                QtGui.QFileDialog.ShowDirsOnly)
        if newworkSpace is "":
            return
        self.workSpace = newworkSpace

    def changeLibraryPath(self):
        newlibraryPath = QtGui.QFileDialog.getExistingDirectory(self, self.trUtf8('Choose the libraries directory'),
                                                                  self.libraryPath,
                                                                  QtGui.QFileDialog.ShowDirsOnly)
        if newlibraryPath is "":
            return
        self.libraryPath = newlibraryPath

    def saveConfigFile(self):
        with open(self.confFile, 'wb') as fichero:
            pickle.dump((self.workSpace, self.ui.language.currentIndex(), self.libraryPath, self.lopenRecent), fichero, protocol=0)

    def downloadLibraries(self):
        if internet_on():
            tempLibraries = tempfile.mkdtemp("Libraries-ebo")
            pathzip = os.path.join(tempLibraries, "Libraries.zip")
            self.dw = DownloadingWindow(self, self.trUtf8("Donwloading Libraries files please wait"), self.trUtf8("Donwloading Libraries"))
            self.dw.show()
            self.dwTh = DownloadThread("https://github.com/robocomp/learnbot/archive/Libraries.zip", pathzip, self.dw)
            self.dwTh.start()
            self.dwTh.finished.connect(lambda : self.unzip(pathzip, tempLibraries, self.libraryPath))

        else:
            msgBox = QtGui.QMessageBox()
            msgBox.setWindowTitle(self.trUtf8("Warning"))
            msgBox.setIcon(QtGui.QMessageBox.Warning)
            msgBox.setText(self.trUtf8("Your computer does not have an internet connection."))
            msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
            msgBox.setDefaultButton(QtGui.QMessageBox.Ok)
            msgBox.exec_()

    def downloadExamples(self):
        if internet_on():
            tempExamples = tempfile.mkdtemp("examples-ebo")
            pathzip = os.path.join(tempExamples, "examples.zip")
            self.dw = DownloadingWindow(self, self.trUtf8("Donwloading Examples files please wait"), self.trUtf8("Donwloading Examples"))
            self.dw.show()
            self.dwTh = DownloadThread("https://github.com/robocomp/learnbot/archive/examples.zip", pathzip, self.dw)
            self.dwTh.start()
            self.dwTh.finished.connect(lambda : self.unzip(pathzip,tempExamples,self.workSpace))

        else:
            msgBox = QtGui.QMessageBox()
            msgBox.setWindowTitle(self.trUtf8("Warning"))
            msgBox.setIcon(QtGui.QMessageBox.Warning)
            msgBox.setText(self.trUtf8("Your computer does not have an internet connection."))
            msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
            msgBox.setDefaultButton(QtGui.QMessageBox.Ok)
            msgBox.exec_()

    def downloadXMLs(self):
        if internet_on():
            tempXMLs = tempfile.mkdtemp("xmls-ebo")
            pathzip = os.path.join(tempXMLs, "xmls.zip")
            self.dw = DownloadingWindow(self, self.trUtf8("Donwloading XML's files please wait"), self.trUtf8("Donwloading XML's"))
            self.dw.show()
            self.dwTh = DownloadThread("https://github.com/robocomp/learnbot/archive/xmls.zip", pathzip, self.dw)
            self.dwTh.start()
            self.dwTh.finished.connect(lambda : self.unzip(pathzip,tempXMLs,os.environ.get('HOME')))

        else:
            msgBox = QtGui.QMessageBox()
            msgBox.setWindowTitle(self.trUtf8("Warning"))
            msgBox.setIcon(QtGui.QMessageBox.Warning)
            msgBox.setText(self.trUtf8("Your computer does not have an internet connection."))
            msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
            msgBox.setDefaultButton(QtGui.QMessageBox.Ok)
            msgBox.exec_()

    def unzip(self, pathzip, tempXMLs, outputPath):
        del self.dwTh
        del self.dw
        Archive(pathzip).extractall(outputPath)
        for f in os.listdir(tempXMLs):
            os.remove(os.path.join(tempXMLs, f))
        os.removedirs(tempXMLs)

    def connectCameraRobot(self):
        if self.checkConnectionToBot():
            try:
                self.client = paho.mqtt.client.Client(client_id='pc', clean_session=False)
                self.client.on_message = on_message
                self.client.connect(host='192.168.16.1', port=50000)
                self.client.subscribe(topic='camara', qos=2)
                self.client.loop_start()
                self.count=0
                self.start = time.time()
                print("Connect Camera Successfully")
            except Exception as e:
                print("Error connect Streamer\n", e)
        else:
            self.client = None

    def readCamera(self,image):
        try:
            # global imageCamera
            pm = QtGui.QPixmap(image)
            if self.pmlast is not None:
                self.cameraScene.removeItem(self.pmlast)
            self.pmlast = self.cameraScene.addPixmap(pm)
            self.cameraScene.update()
        except Exception as e:
            print(e)

    def addLibrary(self):
        self.scene.stopAllblocks()
        path = QtGui.QFileDialog.getExistingDirectory(self, self.trUtf8('Load Library'), self.libraryPath, QtGui.QFileDialog.ShowDirsOnly)
        nameLibrary = os.path.basename(path)
        self.scene.startAllblocks()
        if path is "":
            return
        if path not in [l[0] for l in self.listLibrary]:
            self.listLibraryWidget.append(Library(self, path))
            self.listLibrary.append((path, self.ui.functions.addTab(self.listLibraryWidget[-1],nameLibrary)))
        else:
            msgBox = QtGui.QMessageBox()
            msgBox.setWindowTitle(self.trUtf8("Warning"))
            msgBox.setIcon(QtGui.QMessageBox.Warning)
            msgBox.setText(self.trUtf8("The library has already been imported."))
            msgBox.setInformativeText(self.trUtf8("Do you want select another library?"))
            msgBox.setStandardButtons(QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
            msgBox.setDefaultButton(QtGui.QMessageBox.Ok)
            ret = msgBox.exec_()
            if ret ==QtGui.QMessageBox.Ok:
                self.addLibrary()

    def closeEvent(self, event):
        self.saveConfigFile()
        if self.scene.shouldSave is False:
            self.stopthread()
            self.newProject()
            self.disconnectCamera()
            del self.client
            subprocess.Popen("killall -9 emotionrecognition2.py aprilTag.py", shell=True, stdout=subprocess.PIPE)
            event.accept()
        else:
            self.scene.stopAllblocks()
            msgBox = QtGui.QMessageBox()
            msgBox.setWindowTitle(self.trUtf8("Warning"))
            msgBox.setIcon(QtGui.QMessageBox.Warning)
            msgBox.setText(self.trUtf8("The document has been modified."))
            msgBox.setInformativeText(self.trUtf8("Do you want to save your changes?"))
            msgBox.setStandardButtons(QtGui.QMessageBox.Save | QtGui.QMessageBox.Discard | QtGui.QMessageBox.Cancel)
            msgBox.setDefaultButton(QtGui.QMessageBox.Save)
            ret = msgBox.exec_()
            if ret == QtGui.QMessageBox.Save:
                self.saveInstance()
                self.disconnectCamera()
                del self.client
                self.stopthread()
                subprocess.Popen("killall -9 emotionrecognition2.py aprilTag.py", shell=True, stdout=subprocess.PIPE)
                event.accept()
            elif ret == QtGui.QMessageBox.Discard:
                self.scene.shouldSave = False
                self.disconnectCamera()
                del self.client
                self.stopthread()
                subprocess.Popen("killall -9 emotionrecognition2.py aprilTag.py", shell=True, stdout=subprocess.PIPE)
                event.accept()
            else:
                self.scene.startAllblocks()
                event.ignore()

    def disconnectCamera(self):
        if self.client is not None:
            self.client.disconnect()

    def blocksToText(self):
        text=""
        for library in self.listLibrary:
            text = 'import "' + library[0] +'"\n'
        if len(self.listNameVars) > 0:
            for name in self.listNameVars:
                text += name + " = None\n"
        blocks = self.scene.getListInstructions()
        code = self.parserBlocks(blocks, self.toLBotPy)
        self.ui.textCode.clear()
        self.ui.textCode.setText(text + code)

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
        self.scene.stopAllblocks()
        path = os.environ.get('HOME')
        if os.path.exists(os.path.join(os.environ.get('HOME'), "learnbot-xmls")):
            path = os.path.join(os.environ.get('HOME'), "learnbot-xmls")
        fileName = QtGui.QFileDialog.getOpenFileName(self, self.trUtf8('Open xml'), path,
                                                     self.trUtf8('Rcis file (*.xml)'))
        self.scene.startAllblocks()
        if fileName[0] != "":
            # print(configSSH["start_simulator"] + " " + fileName[0])
            subprocess.Popen(configSSH["start_simulator"] + " " + fileName[0], shell=True, stdout=subprocess.PIPE)

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
            for button in [b for b in self.listButtons if text.lower() in b.getCurrentText().lower()]:
                currentable.insertRow(currentable.rowCount())
                buttonCopy = button.getCopy(currentable)
                currentable.setCellWidget(currentable.rowCount() - 1, 0, buttonCopy)

    def newProject(self, resetAll=True):
        if self.scene.shouldSave is False:
            # Delete all whens
            for x in copy.copy(self.listNameWhens):
                self.delWhen(x[0])
            # Delete all variables
            for name in copy.copy(self.listNameVars):
                self.delVar(name)
            # Delete all user functions
            for name in copy.copy(self.listNameUserFunctions):
                self.delUserFunction(name)
            # Delete all library
            for l in [self.listLibrary[i] for i in range(len(self.listLibrary)).__reversed__()]:
                self.ui.functions.removeTab(l[1])
                i = self.listLibrary.index(l)
                self.listLibrary.remove(l)
                self.listLibraryWidget[i].delete()
                del self.listLibraryWidget[i]
            self.listNameLibraryFunctions = []
            # self.listLibraryWidget = []

            self.scene.setBlockDict({})
            self.scene.startAllblocks()
            if resetAll:
                self.index = -1
                self.__fileProject = None
            self.ui.deleteWhenpushButton.setEnabled(False)
            self.ui.deleteVarPushButton.setEnabled(False)
            self.ui.deleteFuntionsPushButton.setEnabled(False)
            self.setWindowTitle("Learnblock2.0")
        else:
            msgBox = QtGui.QMessageBox()
            msgBox.setWindowTitle(self.trUtf8("Warning"))
            msgBox.setIcon(QtGui.QMessageBox.Warning)
            msgBox.setText(self.trUtf8("The document has been modified."))
            msgBox.setInformativeText(self.trUtf8("Do you want to save your changes?"))
            msgBox.setStandardButtons(QtGui.QMessageBox.Save | QtGui.QMessageBox.Discard | QtGui.QMessageBox.Cancel)
            msgBox.setDefaultButton(QtGui.QMessageBox.Save)
            ret = msgBox.exec_()
            if ret == QtGui.QMessageBox.Save:
                self.saveInstance()
                self.newProject()
            elif ret == QtGui.QMessageBox.Discard:
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
        self.currentTranslator = self.translators[l[self.ui.language.currentIndex()]]
        self.ui.retranslateUi(self)
        for b in self.listButtons:
            b.updateImg()
        if self.__fileProject is not None:
            self.setWindowTitle("Learnblock2.0 " + self.__fileProject)

    def load_blocks(self):
        blocks = reload_functions()
        for k, table in iter(self.dicTables.items()):
            table.clear()
            table.setRowCount(0)
        try:
            self.listNameBlock.clear()
            self.listButtons.clear()
        except:
            pass
        for b in blocks:
            if b["name"] in self.listNameBlock:
                continue
            self.listNameBlock.append(b["name"])
            variables = []
            if "variables" in b:
                for v in b["variables"]:
                    variables.append(Variable(dict=copy.copy(v)))
            funtionType, HUE = type2Values[b["type"]]
            for img in b["img"]:
                blockType, connections = loadConfigBlock(img)
                table = self.dicTables[b["type"]]
                table.insertRow(table.rowCount())
                tooltip = {}
                languages = {}
                if "languages" in b:
                    languages = b["languages"]
                if "tooltip" in b:
                    tooltip = b["tooltip"]
                button = Block_Button((self, b["name"], languages, HUE, self.view, self.scene, img + ".png", connections,
                                       variables, blockType, table, table.rowCount() - 1, funtionType, tooltip))
                if b["name"] == "main":
                    self.mainButton = button
                self.listButtons.append(button)
                table.setCellWidget(table.rowCount() - 1, 0, button)

    def execTmp(self):
        sys.path.insert(0, tempfile.gettempdir())
        try:
            import main_tmp
        except Exception as e:
            print(e)
        finally:
            self.disablestartButtons(False)

    def stopExecTmp(self):
        robot = ""
        try:
            if self.physicalRobot:
                sys.argv = [' ', os.path.join(path,"etc", "configPhysical")]
                robot = "physical"
            else:
                sys.argv = [' ', os.path.join(path,"etc", "configSimulate")]
                robot = "simulate"

            sys.path.insert(0, tempfile.gettempdir())
            try:
                import stop_main_tmp
            except Exception as e:
                print(e)
            finally:
                self.disablestartButtons(False)
        except Exception as e:
            print(e)
            raise e

    def saveInstance(self):
        if self.__fileProject is None:
            self.scene.stopAllblocks()
            fileName = QtGui.QFileDialog.getSaveFileName(self, self.trUtf8('Save Project'), self.workSpace,
                                                         self.trUtf8('Block Project file (*.blockProject)'))
            self.scene.startAllblocks()
            if fileName[0] != "":
                file = fileName[0]
                if "." in file:
                    file = file.split(".")[0]
                file = file + ".blockProject"
                self.__fileProject = file
                self.saveInstance()
        else:
            self.setWindowTitle("Learnblock2.0 " + self.__fileProject)
            with open(self.__fileProject, 'wb') as fichero:
                dic = copy.deepcopy(self.scene.dicBlockItem)
                for id in dic:
                    block = dic[id]
                    block.file = os.path.basename(block.file)
                pickle.dump(
                    (dic, self.listNameWhens, self.listUserFunctions, self.listNameVars, self.listNameUserFunctions, [x[0] for x in self.listLibrary]),
                    fichero, protocol=0)
            self.updateOpenRecent()
        self.scene.shouldSave = False

    def saveAs(self):
        self.scene.stopAllblocks()
        fileName = QtGui.QFileDialog.getSaveFileName(self, self.trUtf8('Save Project'), self.workSpace, self.trUtf8('Block Project file (*.blockProject)'))
        self.scene.startAllblocks()
        if fileName[0] != "" and fileName[1] == self.trUtf8("Block Project file (*.blockProject)"):
            file = fileName[0]
            if os.path.splitext(file)[-1] != ".blockProject":
                file = file + ".blockProject"
            self.__fileProject = file
            self.saveInstance()

    def openProject(self, file=None, changeFileName=True):
        if self.scene.shouldSave is False:
            if file is None:
                self.scene.stopAllblocks()
                fileName = QtGui.QFileDialog.getOpenFileName(self, self.trUtf8('Open Project'), self.workSpace,
                                                         self.trUtf8('Block Project file (*.blockProject)'))
                self.scene.startAllblocks()
            if file is not None or fileName[0] != "":
                self.newProject(resetAll=False)
                if file is None:
                    file = fileName[0]
                if changeFileName:
                    self.__fileProject = file
                    for f in self.listBackUps:
                        os.remove(f)
                    self.listBackUps = []
                    self.index = -1
                if self.__fileProject is not None:
                    self.setWindowTitle("Learnblock2.0 " + self.__fileProject)
                with open(file, 'rb') as fichero:
                    d = pickle.load(fichero)
                    # Load Libraries
                    try:
                        for path in d[5]:
                            nameLibrary = os.path.basename(path)
                            l = Library(self, path)
                            if l.pathLibrary is not None:
                                self.listLibraryWidget.append(l)
                                self.listLibrary.append((l.pathLibrary, self.ui.functions.addTab(self.listLibraryWidget[-1], nameLibrary)))
                    except Exception as e:
                        print(e)

                    dictBlock = d[0]
                    for id in dictBlock:
                        block = dictBlock[id]
                        block.file = os.path.join(pathImgBlocks, os.path.basename(block.file))
                    # Load Whens
                    for x in d[1]:
                        self.addButtonsWhens(x[1], x[0])
                    self.listNameWhens = d[1]
                    # Load Variable
                    for name in d[3]:
                        self.addVariable(name)
                    self.listNameVars = d[3]
                    # Load UserFunctions
                    for name in d[4]:
                        self.addUserFunction(name)
                    self.listNameUserFunctions = d[4]

                    self.scene.setBlockDict(d[0])
                    self.scene.startAllblocks()
                    self.scene.useEvents(self.ui.useEventscheckBox.isChecked())
                self.updateOpenRecent()
                if self.scene.thereisMain():
                    self.mainButton.setEnabled(False)
                self.savetmpProject()
        else:
            msgBox = QtGui.QMessageBox()
            msgBox.setWindowTitle(self.trUtf8("Warning"))
            msgBox.setIcon(QtGui.QMessageBox.Warning)
            msgBox.setText(self.trUtf8("The document has been modified."))
            msgBox.setInformativeText(self.trUtf8("Do you want to save your changes?"))
            msgBox.setStandardButtons(QtGui.QMessageBox.Save | QtGui.QMessageBox.Discard | QtGui.QMessageBox.Cancel)
            msgBox.setDefaultButton(QtGui.QMessageBox.Save)
            ret = msgBox.exec_()
            if ret == QtGui.QMessageBox.Save:
                self.saveInstance()
            elif ret == QtGui.QMessageBox.Discard:
                self.scene.shouldSave = False
                self.openProject(file)

    def showCreateBlock(self):
        self.createBlockGui = guiCreateBlock(self.load_blocks)
        self.createBlockGui.open()

    def showGuiAddNumberOrString(self, type):
        self.addNumberOrStringGui = guiAddNumberOrString(type)
        self.addNumberOrStringGui.ui.pushButtonOK.clicked.connect(self.addBlockNumberOrString)
        self.addNumberOrStringGui.open()

    def addBlockNumberOrString(self):
        text = self.addNumberOrStringGui.value
        imgPath = self.addNumberOrStringGui.imgName
        configImgPath = os.path.splitext(imgPath)[0]
        blockType, connections = loadConfigBlock(configImgPath)
        block = AbstractBlock(0, 0, text, {}, imgPath, [], HUE_NUMBER, "", connections, blockType, VARIABLE)
        self.scene.addItem(block)

    def showGuiAddWhen(self):
        self.addWhenGui = guiAddWhen()
        self.addWhenGui.ui.pushButtonOK.clicked.connect(lambda : self.addBlockWhen(isOK=True))
        self.addWhenGui.ui.pushButtonCancel.clicked.connect(lambda : self.addBlockWhen(isOK=False))
        self.addWhenGui.open()

    def addBlockWhen(self, isOK=True):
        if isOK:

            name = self.addWhenGui.nameControl.replace(" ", "_")
            if not self.addWhenGui.ui.Run_start.isChecked() and name == "start":
                msgBox = QtGui.QMessageBox()
                msgBox.setWindowTitle(self.trUtf8("Warning"))
                msgBox.setIcon(QtGui.QMessageBox.Warning)
                msgBox.setText(self.trUtf8("Error the name can not be 'start'"))
                msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
                msgBox.setDefaultButton(QtGui.QMessageBox.Ok)
                ret = msgBox.exec_()
                return
            if name == "":
                msgBox = QtGui.QMessageBox()
                msgBox.setWindowTitle(self.trUtf8("Warning"))
                msgBox.setIcon(QtGui.QMessageBox.Warning)
                msgBox.setText(self.trUtf8("Error Name is empty."))
                msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
                msgBox.setDefaultButton(QtGui.QMessageBox.Ok)
                ret = msgBox.exec_()
                return
            if name in self.listNameVars or name in [name for name, _ in self.listNameWhens] or name in self.listNameUserFunctions or name in self.listNameLibraryFunctions:
                msgBox = QtGui.QMessageBox()
                msgBox.setWindowTitle(self.trUtf8("Warning"))
                msgBox.setIcon(QtGui.QMessageBox.Warning)
                msgBox.setText(self.trUtf8("This name alredy exist"))
                msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
                msgBox.setDefaultButton(QtGui.QMessageBox.Ok)
                ret = msgBox.exec_()
                return
            text = self.addWhenGui.value
            imgPath = self.addWhenGui.imgName
            configImgPath = os.path.splitext(imgPath)[0]
            blockType, connections = loadConfigBlock(configImgPath)

            block = AbstractBlock(0, 0, text, {'ES': "Cuando ", 'EN': "When "}, imgPath, [], HUE_WHEN,
                                  self.addWhenGui.nameControl.replace(" ", "_"), connections, blockType, WHEN)
            if self.addWhenGui.nameControl != "start":
                self.addButtonsWhens(configImgPath, self.addWhenGui.nameControl.replace(" ", "_"))
            self.scene.addItem(block)
            self.addWhenGui.close()
        else:
            self.addWhenGui.close()

    def addButtonsWhens(self, configImgPath, name):
        if os.path.basename(configImgPath) == 'block8':
            blockType, connections = loadConfigBlock(os.path.join(pathBlocks, "block1"))
            table = self.dicTables['control']

            table.insertRow(table.rowCount())
            button = Block_Button((self, "activate " + name, {'ES': "Activar " + name, 'EN': "Activate " + name}, HUE_WHEN,
                                   self.view, self.scene, os.path.join(pathBlocks, "block1.png"), connections, [], blockType,
                                   table, table.rowCount() - 1, VARIABLE,
                                   {'ES': "Activa el evento " + name, 'EN': "Activate the event " + name}))
            self.listButtonsWhen.append(button)
            self.listButtons.append(button)
            table.setCellWidget(table.rowCount() - 1, 0, button)

            table.insertRow(table.rowCount())
            button = Block_Button((self, "deactivate " + name, {'ES': "Desactivar " + name, 'EN': "Deactivate " + name}, HUE_WHEN,
                                   self.view, self.scene, os.path.join(pathBlocks, "block1.png"), connections, [], blockType,
                                   table, table.rowCount() - 1, VARIABLE,
                                   {'ES': "Desactiva el evento " + name, 'EN': "Deactivate the event " + name}))
            self.listButtonsWhen.append(button)
            self.listButtons.append(button)
            table.setCellWidget(table.rowCount() - 1, 0, button)

        table = self.dicTables['control']
        for x in ["block2", "block3", "block4"]:
            blockType, connections = loadConfigBlock(os.path.join(pathBlocks, x))

            table.insertRow(table.rowCount())
            button = Block_Button((self, "time_" + name, {'ES': "Tiempo_" + name, 'EN': "Time_" + name}, HUE_WHEN, self.view,
                                   self.scene, os.path.join(pathBlocks, x + ".png"), connections, [], blockType, table,
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
            msgBox.setWindowTitle(self.trUtf8("Warning"))
            msgBox.setIcon(QtGui.QMessageBox.Warning)
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
        for library in self.listLibrary:
            text = 'import "' + library[0] +'"\n'
        if fromBlocks:
            blocks = self.scene.getListInstructions()
            if len(self.listNameVars) > 0:
                for name in self.listNameVars:
                    text += name + " = None\n"
        robot = ""
        if self.physicalRobot:
            sys.argv = [' ', os.path.join(path,"etc","configPhysical")]
            robot = "physical"
        else:
            sys.argv = [' ', os.path.join(path,"etc","configSimulate")]
            robot = "simulate"


        if not fromBlocks or blocks is not None:
            if fromBlocks:
                code = self.parserBlocks(blocks, self.toLBotPy)
                self.ui.textCode.clear()
                self.ui.textCode.setText(text + code)
            else:
                code = self.ui.textCode.toPlainText()

            with open(os.path.join(tempfile.gettempdir(), "main_tmp.lb"), "w+") as fh:
                fh.writelines(text + code)

            try:
                if not parserLearntBotCode(os.path.join(tempfile.gettempdir(), "main_tmp.lb"), os.path.join(tempfile.gettempdir(), "main_tmp.py"), self.physicalRobot):
                    msgBox = QtGui.QMessageBox()
                    msgBox.setWindowTitle(self.trUtf8("Warning"))
                    msgBox.setIcon(QtGui.QMessageBox.Warning)
                    msgBox.setText(self.trUtf8("Your code is empty or is not correct"))
                    msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
                    msgBox.setDefaultButton(QtGui.QMessageBox.Ok)
                    msgBox.exec_()
            except Exception as e:
                msgBox = QtGui.QMessageBox()
                msgBox.setWindowTitle(self.trUtf8("Warning"))
                msgBox.setIcon(QtGui.QMessageBox.Warning)
                msgBox.setText(self.trUtf8("line: {}".format(e.line) + "\n    " + " " * e.col + "^"))
                msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
                msgBox.setDefaultButton(QtGui.QMessageBox.Ok)
                msgBox.exec_()
                return
            if compile(os.path.join(tempfile.gettempdir(), "main_tmp.py")):
                try:
                    if self.hilo is not None:
                        self.hilo.terminate()
                    self.hilo = Process(target=self.execTmp)
                    self.hilo.start()
                    self.disablestartButtons(True)
                except:
                    self.disablestartButtons(False)
                    msgBox = QtGui.QMessageBox()
                    msgBox.setWindowTitle(self.trUtf8("Warning"))
                    msgBox.setIcon(QtGui.QMessageBox.Warning)
                    msgBox.setText(self.trUtf8("You should check connection the " + robot + " robot"))
                    msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
                    msgBox.setDefaultButton(QtGui.QMessageBox.Ok)
                    msgBox.exec_()

            else:
                msgBox = QtGui.QMessageBox()
                msgBox.setWindowTitle(self.trUtf8("Warning"))
                msgBox.setIcon(QtGui.QMessageBox.Warning)
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
        with open(os.path.join(tempfile.gettempdir(), "stop_main_tmp.py"), "w+") as fh:
            fh.writelines(text)

    def stopthread(self):
        if self.hilo is not None:
            try:
                self.hilo.terminate()
                self.generateStopTmpFile()
                self.hilo = Process(target=self.stopExecTmp)
                try:
                    self.hilo.start()
                except:
                    msgBox = QtGui.QMessageBox()
                    msgBox.setWindowTitle(self.trUtf8("Warning"))
                    msgBox.setIcon(QtGui.QMessageBox.Warning)
                    msgBox.setText(self.trUtf8("You should check connection to the robot"))
                    msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
                    msgBox.setDefaultButton(QtGui.QMessageBox.Ok)
                    msgBox.exec_()
            except Exception as e:
                print(e)
                pass
            finally:
                self.disablestartButtons(False)

    def parserBlocks(self, blocks, function):
        text = self.parserUserFuntions(blocks, function)
        text += "\n\n"
        if self.ui.useEventscheckBox.isChecked():
            text += self.parserWhenBlocks(blocks, function)
        else:
            text += self.parserOtherBlocks(blocks, function)
        return text

    def parserUserFuntions(self, blocks, function):
        text = ""
        for b in [block for block in blocks if block[1]["TYPE"] is USERFUNCTION]:
            text += "def " + function(b, 1)
            text += "\nend\n\n"
        return text

    def parserWhenBlocks(self, blocks, function):
        text = ""
        for b in [block for block in blocks if block[0] == "when"]:
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
        for b in [block for block in blocks if "main" == block[0]]:
            text += b[0] + ":\n"
            if b[1]["BOTTOMIN"] is not None:
                text += "\t" + function(b[1]["BOTTOMIN"], 2)
            else:
                text += "pass"
            text += "\nend\n\n"
        return text

    def toLBotPy(self, inst, ntab=1):
        text = inst[0]
        if inst[1]["TYPE"] in [USERFUNCTION, LIBRARY]:
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
        self.addVarGui = AddVar.Ui_Dialog()
        self.addVarDialog = QtGui.QDialog()
        self.addVarGui.setupUi(self.addVarDialog)
        self.addVarDialog.open()
        self.addVarGui.cancelPushButton.clicked.connect(lambda: self.retaddVarGui(0))
        self.addVarGui.okPushButton.clicked.connect(lambda: self.retaddVarGui(1))

    def retaddVarGui(self, ret):
        if ret is 1:
            name = self.addVarGui.nameLineEdit.text()
            name = name.replace(" ", "_")
            if name == 'start':
                msgBox = QtGui.QMessageBox()
                msgBox.setWindowTitle(self.trUtf8("Warning"))
                msgBox.setIcon(QtGui.QMessageBox.Warning)
                msgBox.setText(self.trUtf8("Error the name can not be 'start'"))
                msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
                msgBox.setDefaultButton(QtGui.QMessageBox.Ok)
                ret = msgBox.exec_()
                return
            if name in self.listNameVars or name in [name for name, _ in self.listNameWhens] or name in self.listNameUserFunctions or name in self.listNameLibraryFunctions:
                msgBox = QtGui.QMessageBox()
                msgBox.setWindowTitle(self.trUtf8("Warning"))
                msgBox.setIcon(QtGui.QMessageBox.Warning)
                msgBox.setText(self.trUtf8("This name alredy exist"))
                msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
                msgBox.setDefaultButton(QtGui.QMessageBox.Ok)
                ret = msgBox.exec_()
                return
            if len(name) != 0 and name[0].isdigit():
                msgBox = QtGui.QMessageBox()
                msgBox.setWindowTitle(self.trUtf8("Warning"))
                msgBox.setIcon(QtGui.QMessageBox.Warning)
                msgBox.setText(self.trUtf8("The name can't start by number"))
                msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
                msgBox.setDefaultButton(QtGui.QMessageBox.Ok)
                ret = msgBox.exec_()
                return
            if len(name) == 0:
                msgBox = QtGui.QMessageBox()
                msgBox.setWindowTitle(self.trUtf8("Warning"))
                msgBox.setIcon(QtGui.QMessageBox.Warning)
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
        blockType, connections = loadConfigBlock(os.path.join(pathBlocks, "block1"))
        table = self.dicTables['variables']
        table.insertRow(table.rowCount())
        variables = []
        variables.append(Variable("float", "set to ", "0"))
        button = Block_Button((self, name, {}, HUE_WHEN, self.view, self.scene, os.path.join(pathBlocks, "block1.png"), connections,
                               variables, blockType, table, table.rowCount() - 1, VARIABLE, {}))
        self.listButtons.append(button)
        table.setCellWidget(table.rowCount() - 1, 0, button)
        self.listVars.append(button.getAbstracBlockItem())
        for img in imgs:
            blockType, connections = loadConfigBlock(os.path.join(pathBlocks, img))
            table = self.dicTables['variables']
            table.insertRow(table.rowCount())
            button = Block_Button((self, name, {}, HUE_VARIABLE, self.view, self.scene, os.path.join(pathBlocks, img + ".png"), connections,
                                   [], blockType, table, table.rowCount() - 1, VARIABLE, {}))
            self.listButtons.append(button)
            table.setCellWidget(table.rowCount() - 1, 0, button)
            self.listVars.append(button.getAbstracBlockItem())
        self.savetmpProject()

    def deleteVar(self):
        self.delVarGui = DelVar.Ui_Dialog()
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
        for item, row in [(table.cellWidget(r, 0), r) for r in reversed(range(0, table.rowCount())) if table.cellWidget(r, 0).getText() == name]:
            item.delete(row)
            item.removeTmpFile()
            self.listButtons.remove(item)
        self.listNameVars.remove(name)
        self.savetmpProject()

    def deleteWhen(self):
        self.delWhenGui = DelWhen.Ui_Dialog()
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
        for item, row in [(table.cellWidget(r, 0), r) for r in rango if table.cellWidget(r, 0).getText() in ["activate " + name, "deactivate " + name, "time_" + name]]:
            item.delete(row)
            item.removeTmpFile()
            self.listButtons.remove(item)
            self.listButtonsWhen.remove(item)
        for n in [n for n in self.listNameWhens if n[0] == name]:
            self.listNameWhens.remove(n)
        self.scene.removeWhenByName(name)
        if len(self.listNameWhens) is 0:
            self.ui.deleteWhenpushButton.setEnabled(False)

    def newUserFunctions(self):
        self.userFunctionsGui = CreateFunctions.Ui_Dialog()
        self.userFunctionsDialgo = QtGui.QDialog()
        self.userFunctionsGui.setupUi(self.userFunctionsDialgo)
        self.userFunctionsDialgo.open()
        self.userFunctionsGui.cancelPushButton.clicked.connect(lambda: self.retUserFunctions(0))
        self.userFunctionsGui.okPushButton.clicked.connect(lambda: self.retUserFunctions(1))

    def retUserFunctions(self, ret):
        if ret is 1:
            name = self.userFunctionsGui.nameLineEdit.text()
            name = name.replace(" ", "_")
            if name == 'start':
                msgBox = QtGui.QMessageBox()
                msgBox.setWindowTitle(self.trUtf8("Warning"))
                msgBox.setIcon(QtGui.QMessageBox.Warning)
                msgBox.setText(self.trUtf8("Error the name can not be 'start'"))
                msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
                msgBox.setDefaultButton(QtGui.QMessageBox.Ok)
                ret = msgBox.exec_()
                return
            if name in self.listNameVars or name in [name for name, _ in self.listNameWhens] or name in self.listNameUserFunctions or name in self.listNameLibraryFunctions:
                msgBox = QtGui.QMessageBox()
                msgBox.setWindowTitle(self.trUtf8("Warning"))
                msgBox.setIcon(QtGui.QMessageBox.Warning)
                msgBox.setText(self.trUtf8("This name alredy exist"))
                msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
                msgBox.setDefaultButton(QtGui.QMessageBox.Ok)
                ret = msgBox.exec_()
                return
            if len(name) != 0 and name[0].isdigit():
                msgBox = QtGui.QMessageBox()
                msgBox.setWindowTitle(self.trUtf8("Warning"))
                msgBox.setIcon(QtGui.QMessageBox.Warning)
                msgBox.setText(self.trUtf8("The name can't start by number"))
                msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
                msgBox.setDefaultButton(QtGui.QMessageBox.Ok)
                ret = msgBox.exec_()
                return
            if len(name) == 0:
                msgBox = QtGui.QMessageBox()
                msgBox.setWindowTitle(self.trUtf8("Warning"))
                msgBox.setIcon(QtGui.QMessageBox.Warning)
                msgBox.setText(self.trUtf8("Error Name is empty."))
                msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
                msgBox.setDefaultButton(QtGui.QMessageBox.Ok)
                ret = msgBox.exec_()
                return
            self.addUserFunction(name)
            self.savetmpProject()

        self.userFunctionsDialgo.close()

    def addUserFunction(self, name):
        self.ui.deleteFuntionsPushButton.setEnabled(True)
        imgs = ['block8', 'block1']
        self.listNameUserFunctions.append(name)
        table = self.dicTables['funtions']
        i = 0
        for img in imgs:
            blockType, connections = loadConfigBlock(os.path.join(pathBlocks, img))
            table.insertRow(table.rowCount())
            button = Block_Button((self, name, {}, HUE_USERFUNCTION, self.view, self.scene, os.path.join(pathBlocks, img + ".png"), connections,
                                   [], blockType, table, table.rowCount() - 1, USERFUNCTION, {}))
            self.listButtons.append(button)
            table.setCellWidget(table.rowCount() - 1, 0, button)
            self.listUserFunctions.append(button.getAbstracBlockItem())
            i += 1

    def deleteUserFunctions(self):
        self.delUserFunctionsGui = DelVar.Ui_Dialog()
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
        for item,row in [(table.cellWidget(r,0),r) for r in rango if table.cellWidget(r,0).getText() == name]:
            item.delete(row)
            item.removeTmpFile()
            self.listButtons.remove(item)
        self.listNameUserFunctions.remove(name)
        self.savetmpProject()
