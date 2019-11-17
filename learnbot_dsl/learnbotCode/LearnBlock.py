# !/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import
import sys, os, pickle, tempfile, pathlib, shutil, subprocess, io, socket, struct, numpy as np, cv2, paho.mqtt.client, time, \
    requests, paramiko, traceback
from PIL import Image
from pyunpack import Archive
from pyparsing import ParseException
from multiprocessing import Process

from learnbot_dsl.learnbotCode.AbstractBlock import *
from learnbot_dsl.learnbotCode.Button import *
from learnbot_dsl.learnbotCode.Scene import *
from learnbot_dsl.learnbotCode.View import *
from learnbot_dsl.blocksConfig.parserConfigBlock import *
from learnbot_dsl.blocksConfig import pathConfig
from learnbot_dsl.learnbotCode.checkFile import compile
from learnbot_dsl.learnbotCode.dialogAddNumberOrString import *
from learnbot_dsl.learnbotCode.guiCreateBlock import *
from learnbot_dsl.learnbotCode.guiSelectBlocks import *
from learnbot_dsl.learnbotCode.guiJsonEditor import guiJsonEditor
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
from learnbot_dsl.learnbotCode.help import helper
from future.standard_library import install_aliases
from learnbot_dsl.learnbotCode.Parser import HEADER, parserLearntBotCodeFromCode, cleanCode
from learnbot_dsl import PATHCLIENT
from learnbot_dsl.learnbotCode.editDictionaryTags import EditDictionaryTags
import keyword

install_aliases()
from urllib.request import urlopen
from urllib.error import URLError
import qdarkstyle

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
            buffer = u.read()
            f.write(buffer)
        self.downloading_window.finish = True
        return


class DownloadingWindow(QtWidgets.QWidget):
    def __init__(self, parent, text, title):
        QtWidgets.QWidget.__init__(self)
        self.parent = parent
        vbox = QtWidgets.QVBoxLayout()
        self.setWindowTitle(title)
        label = QtWidgets.QLabel(text)
        label.setAlignment(QtCore.Qt.AlignCenter)
        vbox.addWidget(label)

        self.progress_bar = QtWidgets.QProgressBar()
        self.progress_bar.setAlignment(QtCore.Qt.AlignCenter)
        vbox.addWidget(self.progress_bar)
        self.setLayout(vbox)
        self.setGeometry(300, 300, 300, 50)
        self.progress_bar.setRange(0, 0)
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

languageCategories = ["control","operator","variables","functions"]

text4Categories = {"ES": {"motor": "Motor",
                "perceptual": "Percepción",
                "proprioceptive": "Propiocepción",
                "express": "Expresiones",
                "others": "Otros"},
              "EN": {"motor": "Motor",
                "perceptual": "Perceptual",
                "proprioceptive": "Proprioceptive",
                "express": "Expresions",
                "others": "Others"}
              }

type2Values = {"control": (CONTROL, HUE_CONTROL),
               "motor": (FUNTION, HUE_MOTOR),
               "perceptual": (FUNTION, HUE_PERCEPTUAL),
               "proprioceptive": (FUNTION, HUE_PROPIOPERCEPTIVE),
               "operator": (OPERATOR, HUE_OPERATOR),
               "express": (FUNTION, HUE_EXPRESS),
               "others": (FUNTION, HUE_OTHERS)
               }


class LearnBlock(QtWidgets.QMainWindow):
    listNameUserFunctions = []
    listNameVars = []
    listNameBlock = []
    listNameWhens = []
    listButtonsWhen = []
    listVars = []
    listUserFunctions = []
    listButtons = []
    listBlock = []
    listLibrary = []
    listLibraryWidget = []
    listNameLibraryFunctions = []
    __fileProject = None
    hilo = None
    rcisthread = None
    help = None
    index = -1
    pre_sizes = [0, 0]
    dicTables = {}

    def __init__(self):
        global signal
        self.signal = MySignal()
        self.signal.signalUpdateStreamer[QtGui.QImage].connect(self.readCamera)
        signal = self.signal

        # Create the application
        self.app = QtWidgets.QApplication(sys.argv)

        # Load tranlators
        self.translators = {}
        pathLanguages = {'EN': "t_en.qm", "ES": "t_es.qm"}
        for k, v in iter(pathLanguages.items()):
            translator = QtCore.QTranslator()
            print('Localization loaded: ', os.path.join(path, "languages", v),
                  translator.load(v, os.path.join(path, "languages")))
            qttranslator = QtCore.QTranslator()
            print('Localization loaded: ', os.path.join(QtCore.QLibraryInfo.location(QtCore.QLibraryInfo.TranslationsPath), "q" + v),
                  qttranslator.load("q" + v, QtCore.QLibraryInfo.location(QtCore.QLibraryInfo.TranslationsPath)))
            self.translators[k] = (translator, qttranslator)
        self.currentTranslator = self.translators[getLanguage()]

        # install translators
        translator, qttranslator = self.translators[getLanguage()]
        self.app.installTranslator(translator)
        self.app.installTranslator(qttranslator)

        self.app.setWindowIcon(QtGui.QIcon(os.path.join(path, 'Learnbot_ico.png')))

        self.Dialog = QtWidgets.QMainWindow()
        QtWidgets.QMainWindow.__init__(self)
        self.ui = Learnblock.Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("LearnBlock3.0")

        self.showMaximized()

        self.ui.stopPushButton.clicked.connect(self.stopthread)
        self.ui.stoptextPushButton.clicked.connect(self.stopthread)
        self.ui.stopPythonPushButton.clicked.connect(self.stopthread)

        self.ui.startpushButton.clicked.connect(lambda: self.startProgram(2))
        self.ui.starttextPushButton.clicked.connect(lambda: self.startProgram(1))
        self.ui.startPythonPushButton.clicked.connect(lambda: self.startProgram(0))

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
        self.ui.addClientPushButton.clicked.connect(self.addClient)
        self.ui.configRobotPushButton.clicked.connect(self.configureRobot)
        # Actions
        self.ui.actionCreate_New_block.triggered.connect(self.showCreateBlock)
        self.ui.actionSave.triggered.connect(self.saveInstance)
        self.ui.actionSave_As.triggered.connect(self.saveAs)
        self.ui.actionOpen_Project.triggered.connect(self.openProject)
        self.ui.actionLoad_Block_Text_Code.triggered.connect(self.loadBlockTextCode)
        self.ui.actionSave_Block_Text_Code.triggered.connect(self.saveBlockTextCode)
        self.ui.actionLoad_Python_Code.triggered.connect(self.loadPythonCode)
        self.ui.actionSave_Python_Code.triggered.connect(self.savePythonCode)
        self.ui.actionStart_components.triggered.connect(self.startRobot)
        self.ui.actionStart.triggered.connect(lambda: self.startProgram(self.ui.Tabwi.currentIndex()))
        self.ui.actionStart_Simulator.triggered.connect(self.startSimulatorRobot)
        self.ui.actionConfigure_Robot.triggered.connect(self.configureRobot)
        self.ui.actionReboot.triggered.connect(self.rebootRobot)
        self.ui.actionShutdown.triggered.connect(self.shutdownRobot)
        self.ui.actionNew_project.triggered.connect(self.newProject)
        self.ui.actionLoad_Library.triggered.connect(self.addLibrary)
        self.ui.actionLoad_Sets_of_Blocks.triggered.connect(self.loadSetsOfBlocks)
        self.ui.actionAdd_Set_of_Blocks.triggered.connect(self.addSetOfBlocks)
        self.ui.actionSelect_Visible_Blocks.triggered.connect(self.selectVisibleBlocks)
        self.ui.actionSave_Visible_Blocks.triggered.connect(self.saveVisibleBlocks)
        self.ui.actionDownload_xmls.triggered.connect(self.downloadXMLs)
        self.ui.actionDownload_examples.triggered.connect(self.downloadExamples)
        self.ui.actionDownload_libraries.triggered.connect(self.downloadLibraries)
        self.ui.actionExit.triggered.connect(self.close)
        self.ui.actionChange_Libraries_path.triggered.connect(self.changeLibraryPath)
        self.ui.actionChange_Workspace.triggered.connect(self.changeWorkSpace)
        self.ui.connectCameraRobotpushButton.clicked.connect(self.connectCameraRobot)
        self.ui.spinBoxLeterSize.valueChanged.connect(self.updateTextCodeStyle)
        self.ui.textCode.textChanged.connect(self.updateTextCodeStyle)
        self.ui.actionDark.changed.connect(self.enbleDarkTheme)

        self.ui.actionRedo.triggered.connect(self.redo)
        self.ui.actionUndo.triggered.connect(self.undo)
        self.ui.actionStop.triggered.connect(self.stopthread)
        self.ui.actionBlocks_to_text.triggered.connect(self.blocksToText)
        self.ui.actionHelp.triggered.connect(self.openHelp)

        # Load image buttons
        self.ui.savepushButton.setIcon(QtGui.QIcon(os.path.join(pathGuis, "save.png")))
        self.ui.openpushButton.setIcon(QtGui.QIcon(os.path.join(pathGuis, "open.png")))
        self.ui.openpushButton.setFixedSize(QtCore.QSize(24, 22))
        self.ui.savepushButton.setFixedSize(QtCore.QSize(24, 22))
        self.ui.openpushButton.setIconSize(QtCore.QSize(24, 22))
        self.ui.savepushButton.setIconSize(QtCore.QSize(24, 22))
        self.ui.zoompushButton.setIcon(QtGui.QIcon(os.path.join(pathGuis, "zoom.png")))
        self.ui.zoompushButton.setIconSize(QtCore.QSize(30, 30))
        self.ui.zoompushButton.setFixedSize(QtCore.QSize(30, 30))

        self.ui.spinBoxPythonSize.valueChanged.connect(self.updatePythonCodeStyle)
        self.ui.pythonCode.textChanged.connect(self.updatePythonCodeStyle)

        self.disablestartButtons(False)

        self.ui.splitter.splitterMoved.connect(self.resizeFunctionTab)
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
        self.ui.actionDictionary_Tags.triggered.connect(self.editDictTags)

        self.ui.block2textpushButton.clicked.connect(self.blocksToText)
        self.ui.bt2pythonpushButton.clicked.connect(self.btToPython)
        self.dicTables = {'control': self.ui.tableControl, 'operator': self.ui.tableOperadores,
                          'variables': self.ui.tableVariables,
                          'functions': self.ui.tableUserfunctions}

# Test code for including new tabs associated to new types of blocks
#        tableNew = QtWidgets.QTableWidget()
#        self.ui.functions.addTab(tableNew, "new")

        self.highlighter = Highlighter(self.ui.textCode.document())
        self.updateTextCodeStyle()

        self.highlighter2 = Highlighter(self.ui.pythonCode.document())
        self.updatePythonCodeStyle()

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
            os.mkdir(os.path.join(tempfile.gettempdir(), "clients"))
            shutil.copyfile(os.path.join(PATHCLIENT, "EBO.py"),
                            os.path.join(os.getenv('HOME'), ".learnblock", "clients", "EBO.py"))
            os.mkdir(os.path.join(tempfile.gettempdir(), "functions"))
            with open(os.path.join(tempfile.gettempdir(), "__init__.py"), 'w') as f:
                f.write("")

        self.confBlocksPath = None
        self.loadConfigFile()
        self.menuOpenRecent = QtWidgets.QMenu()
        self.ui.actionOpen_Recent.setMenu(self.menuOpenRecent)

        self.updateOpenRecent()
        self.updateClients()
        self.load_blockConfigurations(self.confBlocksPath)
        self.avtiveEvents(False)
        self.pmlast = None
        self.cameraScene = QtWidgets.QGraphicsScene()
        self.ui.cameragraphicsView.setScene(self.cameraScene)

        self.connectCameraRobot()

        self.client = None
        self.isOpen = True
        self.savetmpProject()

        new_sizes = self.ui.splitter.sizes()
        size = sum(new_sizes)
        self.ui.splitter.setSizes([233, size - 233])
        self.pre_sizes = self.ui.splitter.sizes()

        # Execute the application
        # subprocess.Popen("aprilTag.py", shell=True, stdout=subprocess.PIPE)
        # subprocess.Popen("emotionrecognition2.py", shell=True, stdout=subprocess.PIPE)

        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.checkProgramRunning)
        timer.start(200)

        r = self.app.exec_()
        sys.exit(r)

    def editDictTags(self):
        if not hasattr(self, "editDictionaryTagsUI"):
            self.editDictionaryTagsUI = EditDictionaryTags(self)
        self.editDictionaryTagsUI.show()

    def enbleDarkTheme(self):
        sender = self.sender()
        if sender.isChecked():
            self.app.setStyleSheet(qdarkstyle.load_stylesheet_pyside2())
        else:
            self.app.setStyleSheet(None)

    def resizeEvent(self, event):
        QtWidgets.QMainWindow.resizeEvent(self, event)
        new_sizes = self.ui.splitter.sizes()
        size = sum(new_sizes)
        self.pre_sizes[1] = size - self.pre_sizes[0]
        self.ui.splitter.setSizes(self.pre_sizes)
        self.resizeFunctionTab(None, None)

    def resizeFunctionTab(self, pos, event):
        # print(self.ui.splitter.sizes())
        self.pre_sizes = self.ui.splitter.sizes()
        width = self.ui.functions.width() - 51
        tables = [library.ui.tableLibrary for library in self.listLibraryWidget] + list(self.dicTables.values()) + [
            self.ui.tableSearch]
        for v in tables:
            v.setColumnWidth(0, width - 20)
            for item in [v.cellWidget(r, 0) for r in range(v.rowCount())]:
                item.updateIconSize(width - 20)

    def onClickedActionStart(self, simulated=False):
        currenTab = self.ui.Tabwi.currentIndex()
        if currenTab == 0:
            self.startFromPython(simulated)
        elif currenTab == 1:
            self.startFromText(simulated)
        elif currenTab == 2:
            self.startFromBlocks(simulated)

    def openHelp(self):
        if self.help is None:
            self.help = helper(getLanguage())
        if not self.help.empty:
            self.help.show()
        else:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setWindowTitle(self.tr("Not available"))
            msgBox.setIcon(QtWidgets.QMessageBox.Information)
            msgBox.setText(self.tr("The help is not available for the selected language. We apologize for the inconveniences."))
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msgBox.setDefaultButton(QtWidgets.QMessageBox.Ok)
            ret = msgBox.exec_()

            del self.help

    def disablestartButtons(self, disabled):
        self.ui.startpushButton.setEnabled(not disabled)
        self.ui.starttextPushButton.setEnabled(not disabled)
        self.ui.startPythonPushButton.setEnabled(not disabled)
        self.ui.actionStart.setEnabled(not disabled)

        self.ui.stopPushButton.setEnabled(disabled)
        self.ui.stoptextPushButton.setEnabled(disabled)
        self.ui.stopPythonPushButton.setEnabled(disabled)
        self.ui.actionStop.setEnabled(disabled)

    def redo(self):
        self.isOpen = False
        self.scene.shouldSave = False
        if self.index < len(self.listBackUps) - 1:
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
                for f in self.listBackUps[self.index + 1:]:
                    os.remove(f)
                    self.listBackUps = self.listBackUps[:self.index + 1]
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

    def addClient(self):
        file, ext = QtWidgets.QFileDialog.getOpenFileName(self, self.tr('Add Client'), PATHCLIENT,
                                                          self.tr('Python File(*.py)'))
        if file != "":
            shutil.copyfile(file, os.path.join(os.getenv('HOME'), ".learnblock", "clients", os.path.basename(file)))
            cfgFile = os.path.splitext(file)[0] + ".cfg"
            if os.path.isfile(cfgFile):
                shutil.copyfile(cfgFile, os.path.join(os.getenv('HOME'), ".learnblock", "clients", os.path.basename(cfgFile)))
            self.updateClients()

    def updateClients(self):
        self.ui.clientscomboBox.clear()
        for file in os.listdir(os.path.join(os.getenv('HOME'), ".learnblock", "clients")):
            if os.path.isfile(os.path.join(os.getenv('HOME'), ".learnblock", "clients", file)) and \
                    os.path.splitext(file)[-1].lower() == ".py":
                self.ui.clientscomboBox.addItem(os.path.splitext(file)[0])

    def configureRobot(self):
        client = self.ui.clientscomboBox.currentText()
        cfgFile = os.path.join(os.getenv('HOME'), ".learnblock", "clients", client+".cfg")
        if os.path.isfile(cfgFile):
            with open(cfgFile, "rb") as f:
                text = f.read()
            document = json.loads(text)
            self.dialogConfigRobot = guiJsonEditor(document, self.saveRobotConfiguration)
            self.dialogConfigRobot.show()

    def saveRobotConfiguration(self):
        client = self.ui.clientscomboBox.currentText()
        cfgFile = os.path.join(os.getenv('HOME'), ".learnblock", "clients", client+".cfg")
        with open(cfgFile, "w") as file:
            json.dump(self.dialogConfigRobot.model.json(), file, indent=4)                  
        self.dialogConfigRobot.close()

    def updateOpenRecent(self):  # TODO Fixed line lambda
        if self.__fileProject is not None:
            if self.__fileProject not in self.lopenRecent:
                self.lopenRecent.insert(0, self.__fileProject)
            else:
                self.lopenRecent.insert(0, self.lopenRecent.pop(self.lopenRecent.index(self.__fileProject)))
        self.menuOpenRecent.clear()
        self.lopenRecent = [p for p in self.lopenRecent if os.path.exists(p)]
        for f, i in zip(self.lopenRecent, range(len(self.lopenRecent))):
            if i == 9:
                break
            name, _ = os.path.splitext(f)
            name = os.path.basename(name)
            qA = (QtWidgets.QAction(name, self.ui.actionOpen_Recent))
            qA.setShortcut("Ctrl+Shift+" + str(i + 1))
            qA.setData(f)
            qA.triggered.connect(self.openProject)
            self.menuOpenRecent.addAction(qA)

    def updatePythonCodeStyle(self):
        font = QtGui.QFont()
        font.setFamily('Courier')
        font.setFixedPitch(True)
        font.setPointSize(self.ui.spinBoxPythonSize.value())
        self.ui.pythonCode.setFont(font)
        self.ui.pythonCode.setTextColor(QtCore.Qt.white)
        self.ui.pythonCode.setCursorWidth(2)
        p = self.ui.pythonCode.palette()
        p.setColor(self.ui.pythonCode.viewport().backgroundRole(), QtGui.QColor(51, 51, 51, 255))
        self.ui.pythonCode.setPalette(p)

    def updateTextCodeStyle(self):
        font = QtGui.QFont()
        font.setFamily('Courier')
        font.setFixedPitch(True)
        font.setPointSize(self.ui.spinBoxLeterSize.value())
        self.ui.textCode.setFont(font)
        self.ui.textCode.setTextColor(QtCore.Qt.white)
        self.ui.textCode.setCursorWidth(2)
        p = self.ui.textCode.palette()
        p.setColor(self.ui.textCode.viewport().backgroundRole(), QtGui.QColor(51, 51, 51, 255))
        self.ui.textCode.setPalette(p)

    def loadConfigFile(self):
        self.confFile = os.path.join(tempfile.gettempdir(), ".learnblock.conf")
        if not os.path.exists(self.confFile):
            with open(self.confFile, 'wb') as confFile:
                while True:
                    self.workSpace = QtWidgets.QFileDialog.getExistingDirectory(self,
                                                                                self.tr('Choose workspace directory'),
                                                                                os.environ.get('HOME'),
                                                                                QtWidgets.QFileDialog.ShowDirsOnly)
                    if self.workSpace is "":
                        msgBox = QtWidgets.QMessageBox()
                        msgBox.setWindowTitle(self.tr("Warning"))
                        msgBox.setIcon(QtWidgets.QMessageBox.Warning)
                        msgBox.setText(self.tr("Workspace is empty"))
                        msgBox.setInformativeText(
                            self.tr("The working directory will be created in") + os.path.join(os.environ.get('HOME'),
                                                                                               "learnbotWorkSpace"))
                        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
                        msgBox.setDefaultButton(QtWidgets.QMessageBox.Cancel)
                        ret = msgBox.exec_()
                        if ret == QtWidgets.QMessageBox.Ok:
                            self.workSpace = os.path.join(os.environ.get('HOME'), "learnbotWorkSpace")
                            os.mkdir(self.workSpace)
                            break
                    else:
                        self.workSpace = os.path.join(self.workSpace)
                        break
                while True:
                    self.libraryPath = QtWidgets.QFileDialog.getExistingDirectory(self, self.tr(
                        'Choose the libraries directory'), os.environ.get('HOME'),
                                                                                  QtWidgets.QFileDialog.ShowDirsOnly)
                    if self.libraryPath is "":
                        msgBox = QtWidgets.QMessageBox()
                        msgBox.setWindowTitle(self.tr("Warning"))
                        msgBox.setIcon(QtWidgets.QMessageBox.Warning)
                        msgBox.setText(self.tr("Workspace is empty"))
                        msgBox.setInformativeText(self.tr("The libraries directory will be ") + os.environ.get('HOME'))
                        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
                        msgBox.setDefaultButton(QtWidgets.QMessageBox.Cancel)
                        ret = msgBox.exec_()
                        if ret == QtWidgets.QMessageBox.Ok:
                            self.libraryPath = os.environ.get('HOME')
                            break
                    else:
                        break
                self.saveConfigFile()

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
                try:
                    self.ui.actionDark.setChecked(d[4])
                except:
                    pass
                try:
                    self.confBlocksPath = d[5]
                    if not os.path.exists(self.confBlocksPath):
                        self.confBlocksPath = None
                except:
                    pass


    def changeWorkSpace(self):
        newworkSpace = QtWidgets.QFileDialog.getExistingDirectory(self, self.tr('Choose workspace directory'),
                                                                  self.workSpace,
                                                                  QtWidgets.QFileDialog.ShowDirsOnly)
        if newworkSpace is "":
            return
        self.workSpace = newworkSpace

    def changeLibraryPath(self):
        newlibraryPath = QtWidgets.QFileDialog.getExistingDirectory(self, self.tr('Choose the libraries directory'),
                                                                    self.libraryPath,
                                                                    QtWidgets.QFileDialog.ShowDirsOnly)
        if newlibraryPath is "":
            return
        self.libraryPath = newlibraryPath

    def saveConfigFile(self):
        with open(self.confFile, 'wb') as fichero:
            pickle.dump((self.workSpace, self.ui.language.currentIndex(), self.libraryPath, self.lopenRecent, self.ui.actionDark.isChecked(), self.confBlocksPath), fichero, protocol=0)

    def downloadLibraries(self):
        if internet_on():
            tempLibraries = tempfile.mkdtemp("Libraries-ebo")
            pathzip = os.path.join(tempLibraries, "Libraries.zip")
            self.dw = DownloadingWindow(self, self.tr("Donwloading Libraries files please wait"),
                                        self.tr("Donwloading Libraries"))
            self.dw.show()
            self.dwTh = DownloadThread("https://github.com/robocomp/learnbot/archive/Libraries.zip", pathzip, self.dw)
            self.dwTh.start()
            self.dwTh.finished.connect(lambda: self.unzip(pathzip, tempLibraries, self.libraryPath))

        else:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setWindowTitle(self.tr("Warning"))
            msgBox.setIcon(QtWidgets.QMessageBox.Warning)
            msgBox.setText(self.tr("Your computer does not have an internet connection."))
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msgBox.setDefaultButton(QtWidgets.QMessageBox.Ok)
            msgBox.exec_()

    def downloadExamples(self):
        if internet_on():
            tempExamples = tempfile.mkdtemp("examples-ebo")
            pathzip = os.path.join(tempExamples, "examples.zip")
            self.dw = DownloadingWindow(self, self.tr("Donwloading Examples files please wait"),
                                        self.tr("Donwloading Examples"))
            self.dw.show()
            self.dwTh = DownloadThread("https://github.com/robocomp/learnbot/archive/examples.zip", pathzip, self.dw)
            self.dwTh.start()
            self.dwTh.finished.connect(lambda: self.unzip(pathzip, tempExamples, self.workSpace))

        else:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setWindowTitle(self.tr("Warning"))
            msgBox.setIcon(QtWidgets.QMessageBox.Warning)
            msgBox.setText(self.tr("Your computer does not have an internet connection."))
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msgBox.setDefaultButton(QtWidgets.QMessageBox.Ok)
            msgBox.exec_()

    def downloadXMLs(self):
        if internet_on():
            tempXMLs = tempfile.mkdtemp("xmls-ebo")
            pathzip = os.path.join(tempXMLs, "xmls.zip")
            self.dw = DownloadingWindow(self, self.tr("Donwloading XML's files please wait"),
                                        self.tr("Donwloading XML's"))
            self.dw.show()
            self.dwTh = DownloadThread("https://github.com/robocomp/learnbot/archive/xmls.zip", pathzip, self.dw)
            self.dwTh.start()
            self.dwTh.finished.connect(lambda: self.unzip(pathzip, tempXMLs, os.environ.get('HOME')))

        else:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setWindowTitle(self.tr("Warning"))
            msgBox.setIcon(QtWidgets.QMessageBox.Warning)
            msgBox.setText(self.tr("Your computer does not have an internet connection."))
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msgBox.setDefaultButton(QtWidgets.QMessageBox.Ok)
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
                # self.client = paho.mqtt.client.Client(client_id='pc', clean_session=False)
                self.client = paho.mqtt.client.Client()
                self.client.on_message = on_message
                self.client.connect(host='192.168.16.1', port=50000)
                self.client.subscribe(topic='camara', qos=2)
                self.client.loop_start()
                self.count = 0
                self.start = time.time()
                print("Connect Camera Successfully")
            except Exception as e:
                print("Error connect Streamer\n", e)
        else:
            self.client = None

    def readCamera(self, image):
        try:
            # global imageCamera
            pm = QtGui.QPixmap(image)
            if self.pmlast is not None:
                self.cameraScene.removeItem(self.pmlast)
            self.pmlast = self.cameraScene.addPixmap(pm)
            self.cameraScene.update()
        except Exception as e:
            traceback.print_exc()
            print(e)

    def addLibrary(self):
        self.scene.stopAllblocks()
        path = QtWidgets.QFileDialog.getExistingDirectory(self, self.tr('Load Library'), self.libraryPath,
                                                          QtWidgets.QFileDialog.ShowDirsOnly)
        nameLibrary = os.path.basename(path)
        self.scene.startAllblocks()
        if path is "":
            return
        if path not in [l[0] for l in self.listLibrary]:
            self.listLibraryWidget.append(Library(self, path))
            self.listLibrary.append((path, self.ui.functions.addTab(self.listLibraryWidget[-1], nameLibrary)))
        else:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setWindowTitle(self.tr("Warning"))
            msgBox.setIcon(QtWidgets.QMessageBox.Warning)
            msgBox.setText(self.tr("The library has already been imported."))
            msgBox.setInformativeText(self.tr("Do you want select another library?"))
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
            msgBox.setDefaultButton(QtWidgets.QMessageBox.Ok)
            ret = msgBox.exec_()
            if ret == QtWidgets.QMessageBox.Ok:
                self.addLibrary()

    def closeEvent(self, event):
        self.saveConfigFile()
        if self.scene.shouldSave is False:
            self.stopthread()
            self.newProject()
            self.disconnectCamera()
            del self.client
            if self.rcisthread is not None:
                self.rcisthread.terminate()
#            subprocess.Popen("killall -9 emotionrecognition2.py aprilTag.py", shell=True, stdout=subprocess.PIPE)
            subprocess.Popen("pkill -f emotionrecognition2.py", shell=True, stdout=subprocess.PIPE)
            subprocess.Popen("pkill -f aprilTag.py", shell=True, stdout=subprocess.PIPE)
            event.accept()
        else:
            self.scene.stopAllblocks()
            msgBox = QtWidgets.QMessageBox()
            msgBox.setWindowTitle(self.tr("Warning"))
            msgBox.setIcon(QtWidgets.QMessageBox.Warning)
            msgBox.setText(self.tr("The document has been modified."))
            msgBox.setInformativeText(self.tr("Do you want to save your changes?"))
            msgBox.setStandardButtons(
                QtWidgets.QMessageBox.Save | QtWidgets.QMessageBox.Discard | QtWidgets.QMessageBox.Cancel)
            msgBox.setDefaultButton(QtWidgets.QMessageBox.Save)
            ret = msgBox.exec_()
            if ret == QtWidgets.QMessageBox.Save:
                self.saveInstance()
                self.disconnectCamera()
                del self.client
                self.stopthread()
                if self.rcisthread is not None:
                    self.rcisthread.terminate()
#                subprocess.Popen("killall -9 emotionrecognition2.py aprilTag.py", shell=True, stdout=subprocess.PIPE)
                subprocess.Popen("pkill -f emotionrecognition2.py", shell=True, stdout=subprocess.PIPE)
                subprocess.Popen("pkill -f aprilTag.py", shell=True, stdout=subprocess.PIPE)
                event.accept()
            elif ret == QtWidgets.QMessageBox.Discard:
                self.scene.shouldSave = False
                self.disconnectCamera()
                del self.client
                self.stopthread()
                if self.rcisthread is not None:
                    self.rcisthread.terminate()
 #               subprocess.Popen("killall -9 emotionrecognition2.py aprilTag.py", shell=True, stdout=subprocess.PIPE)
                subprocess.Popen("pkill -f emotionrecognition2.py", shell=True, stdout=subprocess.PIPE)
                subprocess.Popen("pkill -f aprilTag.py", shell=True, stdout=subprocess.PIPE)
                event.accept()
            else:
                self.scene.startAllblocks()
                event.ignore()

    def disconnectCamera(self):
        if self.client is not None:
            self.client.disconnect()

    def blocksToText(self):
        name_Client = self.ui.clientscomboBox.currentText()
        self.blocksToTextCode()
        self.textCodeToPython(name_Client)

    def btToPython(self):
        name_Client = self.ui.clientscomboBox.currentText()
        self.textCodeToPython(name_Client)

    def blocksToTextCode(self):
        text = ""
        for library in self.listLibrary:
            text = 'import "' + library[0] + '"\n'
        if len(self.listNameVars) > 0:
            for name in self.listNameVars:
                text += name + " = None\n"
        blocks = self.scene.getListInstructions()
        code = self.parserBlocks(blocks, self.toLBotPy)
        self.ui.textCode.clear()
        self.ui.textCode.setText(text + code)

    def checkConnectionToBot(self, showWarning=False):
        r = os.system("ping -c 1 -W 1 " + configSSH["ip"])
        if showWarning and r is not 0:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setWindowTitle(self.tr("Warning"))
            msgBox.setIcon(QtWidgets.QMessageBox.Warning)
            msgBox.setText(self.tr("You should check connection the physical robot"))
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msgBox.setDefaultButton(QtWidgets.QMessageBox.Ok)
            msgBox.exec_()
        return r is 0

    def startRobot(self):
        if self.checkConnectionToBot():
            client = paramiko.SSHClient()
            client.load_system_host_keys()
            client.set_missing_host_key_policy(paramiko.WarningPolicy)
            print(configSSH["ip"], configSSH["user"], configSSH["pass"])
            client.connect(hostname=configSSH["ip"], port=22, username=configSSH["user"], password=configSSH["pass"])
            _, stdout, _ = client.exec_command(configSSH["start"])

    def startProgram(self, _from=2):
        selected_Client = self.ui.clientscomboBox.currentIndex()
        name_Client = self.ui.clientscomboBox.currentText()
        if _from == 2:  # from blocks
            self.blocksToTextCode()
        if _from >= 1:  # from textCode
            self.textCodeToPython(name_Client)

        with open(os.path.join(tempfile.gettempdir(), "main_tmp.py"), "w+") as fh:
            fh.writelines(self.ui.pythonCode.toPlainText())
        if compile(os.path.join(tempfile.gettempdir(), "main_tmp.py")):
            try:
                if self.hilo is not None:
                    try:
                        self.hilo.terminate()
                    except Exception as e:
                        print(e.with_traceback())
                self.hilo = subprocess.Popen(
                    ["python" + sys.version[0], os.path.join(tempfile.gettempdir(), "main_tmp.py")],
                    stdout=subprocess.PIPE)
                # self.hilo = Process(target=self.execTmp)
                # self.hilo.start()
                self.disablestartButtons(True)
            except Exception as e:
                print(e.with_traceback())
                self.disablestartButtons(False)
                msgBox = QtWidgets.QMessageBox()
                msgBox.setWindowTitle(self.tr("Warning"))
                msgBox.setIcon(QtWidgets.QMessageBox.Warning)
                msgBox.setText(self.tr("You should check the connection to " + name_Client))
                msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                msgBox.setDefaultButton(QtWidgets.QMessageBox.Ok)
                msgBox.exec_()

        else:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setWindowTitle(self.tr("Warning"))
            msgBox.setIcon(QtWidgets.QMessageBox.Warning)
            msgBox.setText(self.tr("Your code has an error. Check it out again"))
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msgBox.setDefaultButton(QtWidgets.QMessageBox.Ok)
            msgBox.exec_()

    def checkProgramRunning(self):
        if self.hilo is not None:
            p = self.hilo.poll()
            if p is not None:
                self.disablestartButtons(False)
                self.hilo = None
                print("returned value", p)
                if p!=0:
                    subprocess.Popen("pkill -f emotionrecognition2.py", shell=True, stdout=subprocess.PIPE)
                    subprocess.Popen("pkill -f aprilTag.py", shell=True, stdout=subprocess.PIPE)
                    name_Client = self.ui.clientscomboBox.currentText()
                    msgBox = QtWidgets.QMessageBox()
                    msgBox.setWindowTitle(self.tr("Warning"))
                    msgBox.setIcon(QtWidgets.QMessageBox.Warning)
                    msgBox.setText(self.tr("You should check the connection to " + name_Client))
                    msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    msgBox.setDefaultButton(QtWidgets.QMessageBox.Ok)
                    msgBox.exec_()



    def textCodeToPython(self, name_Client):
        textCode = self.ui.textCode.toPlainText()
        try:
            code = parserLearntBotCodeFromCode(textCode, name_Client)
            if not code:
                msgBox = QtWidgets.QMessageBox()
                msgBox.setWindowTitle(self.tr("Warning"))
                msgBox.setIcon(QtWidgets.QMessageBox.Warning)
                msgBox.setText(self.tr("Your code is empty or is not correct"))
                msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                msgBox.setDefaultButton(QtWidgets.QMessageBox.Ok)
                msgBox.exec_()
            self.ui.pythonCode.clear()
            self.ui.pythonCode.setText(code)
            return code
        except ParseException as e:
            traceback.print_exc()
            msgBox = QtWidgets.QMessageBox()
            msgBox.setWindowTitle(self.tr("Warning"))
            msgBox.setIcon(QtWidgets.QMessageBox.Warning)
            msgBox.setText(self.tr("line: {}".format(e.line) + "\n    " + " " * e.col + "^"))
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msgBox.setDefaultButton(QtWidgets.QMessageBox.Ok)
            msgBox.exec_()
        except Exception as e:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setWindowTitle(self.tr("Warning"))
            msgBox.setIcon(QtWidgets.QMessageBox.Warning)
            msgBox.setText(e)
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msgBox.setDefaultButton(QtWidgets.QMessageBox.Ok)
            msgBox.exec_()
        return False

    def startSimulatorRobot(self):
        self.scene.stopAllblocks()
        path = os.environ.get('HOME')
        if os.path.exists(os.path.join(os.environ.get('HOME'), "learnbot-xmls")):
            path = os.path.join(os.environ.get('HOME'), "learnbot-xmls")
        fileName = QtWidgets.QFileDialog.getOpenFileName(self, self.tr('Open xml'), path,
                                                         self.tr('Rcis file (*.xml)'))
        self.scene.startAllblocks()
        if fileName[0] != "":
            if self.rcisthread is not None:
                self.rcisthread.terminate()
            self.rcisthread = Process(target=lambda: os.popen(
                "cd " + os.path.dirname(fileName[0]) + " && " + configSSH["start_simulator"] + " " + fileName[0]))
            self.rcisthread.start()

    def shutdownRobot(self):
        if self.checkConnectionToBot():
            client = paramiko.SSHClient()
            client.load_system_host_keys()
            client.set_missing_host_key_policy(paramiko.WarningPolicy)
            client.connect(configSSH["ip"], port=22, username=configSSH["user"], password=configSSH["pass"])
            stdin, stdout, stderr = client.exec_command("sudo shutdown -h now")

    def rebootRobot(self):
        if self.checkConnectionToBot():
            client = paramiko.SSHClient()
            client.load_system_host_keys()
            client.set_missing_host_key_policy(paramiko.WarningPolicy)
            client.connect(configSSH["ip"], port=22, username=configSSH["user"], password=configSSH["pass"])
            stdin, stdout, stderr = client.exec_command("sudo reboot 0")

    def avtiveEvents(self, isChecked):
        self.scene.useEvents(isChecked)
        self.ui.addWhenpushButton.setEnabled(isChecked)
        if not self.scene.thereisMain() and (self.mainButton is not None):
            self.mainButton.setEnabled(not isChecked)
        for b in self.listButtonsWhen:
            b.setEnabled(isChecked)

    def searchUpdate(self, text):
        text = text.replace(" ", "_")
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
            for name, _ in copy.copy(self.listNameWhens):
                self.delWhen(name)
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
            self.setWindowTitle("LearnBlock3.0")
        else:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setWindowTitle(self.tr("Warning"))
            msgBox.setIcon(QtWidgets.QMessageBox.Warning)
            msgBox.setText(self.tr("The document has been modified."))
            msgBox.setInformativeText(self.tr("Do you want to save your changes?"))
            msgBox.setStandardButtons(
                QtWidgets.QMessageBox.Save | QtWidgets.QMessageBox.Discard | QtWidgets.QMessageBox.Cancel)
            msgBox.setDefaultButton(QtWidgets.QMessageBox.Save)
            ret = msgBox.exec_()
            if ret == QtWidgets.QMessageBox.Save:
                self.saveInstance()
                self.newProject()
            elif ret == QtWidgets.QMessageBox.Discard:
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
        if isinstance(self.__fileProject, str):
            self.setWindowTitle("LearnBlock3.0 " + self.__fileProject)
        if self.help is not None:
            del self.help

    def load_blockConfigurations(self, config_path = None):
        blocks = reload_functions(config_path)
        self.blocksInCategories = {}
        for b in blocks:
            btype = str(b["category"])
            if not btype in self.blocksInCategories.keys():
                self.blocksInCategories[btype] = []
            self.blocksInCategories[btype].append((b,True))
        self.load_blocks()

    def selectVisibleBlocks(self):
        lang = getLanguage()
        self.visibleBlockLists = {}
        for cat in self.blocksInCategories.keys():
            if not cat in languageCategories:
                newList = []
                for b, visible in self.blocksInCategories[cat]:
                    if "languages" in b.keys():
                        if lang in b["languages"].keys():
                            newList.append((b["languages"][lang], visible))
                        else:
                            newList.append((b["name"], visible))
                    else:
                        newList.append((b["name"], visible))
                self.visibleBlockLists[cat] = newList
        self.dialogSelectBlocks = guiSelectBlocks(self.visibleBlockLists, self.setVisibleBlocks)
        self.dialogSelectBlocks.show()

    def setVisibleBlocks(self):
        keys = list(self.visibleBlockLists.keys())
        k = 0
        for l in self.dialogSelectBlocks.lists:
            cat = keys[k]
            for i in range(l.count()):
                item = l.item(i)
                if item.checkState() == QtCore.Qt.Checked:
                    self.blocksInCategories[cat][i] = (self.blocksInCategories[cat][i][0], True)
                else:
                    self.blocksInCategories[cat][i] = (self.blocksInCategories[cat][i][0], False)
            k+=1
        self.dialogSelectBlocks.close()
        self.load_blocks()

    def saveVisibleBlocks(self):
        blocks_path = QtWidgets.QFileDialog.getExistingDirectory(self, self.tr("Select Directory"), str(pathlib.Path.home()), QtWidgets.QFileDialog.ShowDirsOnly | QtWidgets.QFileDialog.DontResolveSymlinks)
        if blocks_path!="":
            for cat in self.blocksInCategories.keys():
                if not cat in languageCategories:
                    configFile = os.path.join(blocks_path, cat+".conf")
                    saveConfig = True
                    if os.path.isfile(configFile):
                        msgBox = QtWidgets.QMessageBox()
                        msgBox.setWindowTitle(self.tr("Warning"))
                        msgBox.setIcon(QtWidgets.QMessageBox.Warning)
                        msgBox.setText(self.tr("The config file ") + "\"" + cat + ".conf" + "\"" + self.tr(" already exists"))
                        msgBox.setInformativeText(self.tr("Do you want to overwrite it?"))
                        msgBox.setStandardButtons(QtWidgets.QMessageBox.Save |QtWidgets.QMessageBox.Cancel)
                        msgBox.setDefaultButton(QtWidgets.QMessageBox.Save)
                        ret = msgBox.exec_()
                        if ret == QtWidgets.QMessageBox.Save:
                            saveConfig = True
                        else:
                            saveConfig = False
                    if saveConfig:
                        listOfBlocks = []
                        for b in self.blocksInCategories[cat]:
                            if b[1]:
                                listOfBlocks.append(b[0])
                        with open(configFile, "w") as file:
                            json.dump(listOfBlocks, file, indent=4)                  


    def load_blocks(self):
        for k, table in iter(self.dicTables.items()):
            table.clear()
            table.setRowCount(0)
        kBlocks = list(self.dicTables.keys())
        for k in kBlocks:
            if not k in languageCategories:
                indTab = self.ui.functions.indexOf(self.dicTables[k])
                self.ui.functions.removeTab(indTab)
                del self.dicTables[k]

        try:
            self.listNameBlock.clear()
            self.listButtons.clear()
        except:
            pass

        self.mainButton = None
        for k, blocks in iter(self.blocksInCategories.items()):
            for b in blocks:
                if b[1]:
                    self.addBlock(b[0])

    def addBlock(self, b):
        if b["name"] in self.listNameBlock:
            return

        if not b["category"] in self.dicTables.keys():
            tableNew = QtWidgets.QTableWidget()
            tableNew.verticalHeader().setVisible(False)
            tableNew.horizontalHeader().setVisible(False)
            tableNew.setShowGrid(False)
            tableNew.setColumnCount(1)
            tableNew.setRowCount(0)
            self.ui.functions.addTab(tableNew, b["category"])
            self.dicTables[b["category"]] = tableNew


        self.listNameBlock.append(b["name"])
        variables = []
        if "variables" in b:
            for v in b["variables"]:
                variables.append(Variable(dict=copy.copy(v)))
        funtionType, HUE = type2Values[b["type"]]
        for img in b["shape"]:
            img = renameBlock(img)
            blockType, connections = loadConfigBlock(os.path.join(pathBlocks, img))
            table = self.dicTables[b["category"]]
            table.insertRow(table.rowCount())
            tooltip = {}
            languages = {}
            if "languages" in b:
                languages = b["languages"]
            if "tooltip" in b:
                tooltip = b["tooltip"]
            button = Block_Button(
                (self, b["name"], languages, HUE, self.view, self.scene, os.path.join(pathBlocks, img + ".png"), connections, variables, blockType, table, table.rowCount() - 1, funtionType, tooltip))
            if b["name"] == "main":
                self.mainButton = button
            self.listButtons.append(button)
            table.setCellWidget(table.rowCount() - 1, 0, button)


    def execTmp(self):
        sys.path.insert(0, tempfile.gettempdir())
        try:
            import main_tmp
        except Exception as e:
            traceback.print_exc()
        finally:
            self.disablestartButtons(False)

    def stopExecTmp(self):
        robot = ""
        try:
            sys.path.insert(0, tempfile.gettempdir())
            try:
                import stop_main_tmp
            except Exception as e:
                traceback.print_exc()
            finally:
                self.disablestartButtons(False)
        except Exception as e:
            traceback.print_exc()
            raise e

    def saveInstance(self):
        if self.__fileProject is None:
            self.scene.stopAllblocks()
            fileName = QtWidgets.QFileDialog.getSaveFileName(self, self.tr('Save Project'), self.workSpace,
                                                             self.tr('Block Project file (*.blockProject)'))
            self.scene.startAllblocks()
            if fileName[0] != "":
                file = fileName[0]
                if "." in file:
                    file = file.split(".")[0]
                file = file + ".blockProject"
                self.__fileProject = file
                self.saveInstance()
        else:
            self.setWindowTitle("LearnBlock3.0 " + self.__fileProject)
            with open(self.__fileProject, 'wb') as fichero:
                dic = copy.deepcopy(self.scene.dicBlockItem)
                for id in dic:
                    block = dic[id]
                    block.file = os.path.basename(block.file)
                pickle.dump(
                    (dic, self.listNameWhens, self.listUserFunctions, self.listNameVars, self.listNameUserFunctions,
                     [x[0] for x in self.listLibrary]),
                    fichero, protocol=0)
            self.updateOpenRecent()
        self.scene.shouldSave = False

    def saveAs(self):
        self.scene.stopAllblocks()
        fileName = QtWidgets.QFileDialog.getSaveFileName(self, self.tr('Save Project'), self.workSpace,
                                                         self.tr('Block Project file (*.blockProject)'))
        self.scene.startAllblocks()
        if fileName[0] != "" and fileName[1] == self.tr("Block Project file (*.blockProject)"):
            file = fileName[0]
            if os.path.splitext(file)[-1] != ".blockProject":
                file = file + ".blockProject"
            self.__fileProject = file
            self.saveInstance()

    def openProject(self, file=None, changeFileName=True):
        sender = self.sender()
        if hasattr(sender, "data"):
            data = sender.data()
            if data is not None:
                file = data
        if self.scene.shouldSave is False:
            if file is None:
                self.scene.stopAllblocks()
                fileName = QtWidgets.QFileDialog.getOpenFileName(self, self.tr('Open Project'), self.workSpace,
                                                                 self.tr('Block Project file (*.blockProject)'))
                self.scene.startAllblocks()
            if file is not None or fileName[0] != "":
                self.newProject()#(resetAll=False)
                if file is None:
                    file = fileName[0]
                if changeFileName:
                    self.__fileProject = file
                    for f in self.listBackUps:
                        os.remove(f)
                    self.listBackUps = []
                    self.index = -1
                if self.__fileProject is not None:
                    self.setWindowTitle("LearnBlock3.0 " + self.__fileProject)
                with open(file, 'rb') as fichero:
                    d = pickle.load(fichero)
                    # Load Libraries
                    try:
                        for path in d[5]:
                            nameLibrary = os.path.basename(path)
                            l = Library(self, path)
                            if l.pathLibrary is not None:
                                self.listLibraryWidget.append(l)
                                self.listLibrary.append(
                                    (l.pathLibrary, self.ui.functions.addTab(self.listLibraryWidget[-1], nameLibrary)))
                    except Exception as e:
                        traceback.print_exc()

                    dictBlock = d[0]
                    for block in dictBlock.values():
                        block.file = os.path.join(pathImgBlocks, os.path.basename(block.file))
                    # Load Whens
                    for name, configFile in d[1]:
                        self.addButtonsWhens(configFile, name)
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
                if self.scene.thereisMain() and (self.mainButton is not None):
                    self.mainButton.setEnabled(False)
                self.savetmpProject()

        else:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setWindowTitle(self.tr("Warning"))
            msgBox.setIcon(QtWidgets.QMessageBox.Warning)
            msgBox.setText(self.tr("The document has been modified."))
            msgBox.setInformativeText(self.tr("Do you want to save your changes?"))
            msgBox.setStandardButtons(
                QtWidgets.QMessageBox.Save | QtWidgets.QMessageBox.Discard | QtWidgets.QMessageBox.Cancel)
            msgBox.setDefaultButton(QtWidgets.QMessageBox.Save)
            ret = msgBox.exec_()
            if ret == QtWidgets.QMessageBox.Save:
                self.saveInstance()
            elif ret == QtWidgets.QMessageBox.Discard:
                self.scene.shouldSave = False
                self.openProject(file)

    def loadBlockTextCode(self):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, self.tr('Load Block-Text code'), self.workSpace, self.tr('Block-Text file (*.bt)'))
        if os.path.exists(fileName):
            f = open(fileName, "r")
            code = f.read()
            self.ui.textCode.clear()
            self.ui.textCode.setText(code)
            f.close()

    def saveBlockTextCode(self):
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self, self.tr('Save Block-Text code'), self.workSpace, self.tr('Block-Text file (*.bt)'))
        if fileName!="":
            name, extension = os.path.splitext(fileName)
            if extension == "":
                fileName += ".bt"
            f = open(fileName, "w")
            code = self.ui.textCode.toPlainText()
            f.write(code)
            f.close()

    def loadPythonCode(self):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, self.tr('Load Python code'), self.workSpace, self.tr('Python file (*.py)'))
        if os.path.exists(fileName):
            f = open(fileName, "r")
            code = f.read()
            self.ui.pythonCode.clear()
            self.ui.pythonCode.setText(code)
            f.close()


    def savePythonCode(self):
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self, self.tr('Save Python code'), self.workSpace, self.tr('Python file (*.py)'))
        if fileName!="":
            name, extension = os.path.splitext(fileName)
            if extension == "":
                fileName += ".py"
            f = open(fileName, "w")
            code = self.ui.pythonCode.toPlainText()
            f.write(code)
            f.close()


    def loadSetsOfBlocks(self):
        blocks_path = QtWidgets.QFileDialog.getExistingDirectory(self, self.tr("Select directory"), pathConfig, QtWidgets.QFileDialog.ShowDirsOnly | QtWidgets.QFileDialog.DontResolveSymlinks)
        if blocks_path!="":
            self.confBlocksPath = blocks_path
            self.load_blockConfigurations(blocks_path)

    def addSetOfBlocks(self):
        blocks_file, _ = QtWidgets.QFileDialog.getOpenFileName(self, self.tr("Select a block configuration file"), pathConfig, filter = "*.conf")
        if blocks_file!="":
            with open(blocks_file, "rb") as f:
                text = f.read()
            blocks = json.loads(text)
            for b in blocks:
                btype = str(b["category"])
                if not btype in self.blocksInCategories.keys():
                    self.blocksInCategories[btype] = []
                self.blocksInCategories[btype].append((b,True))
                self.addBlock(b)


    def showCreateBlock(self):
        self.createBlockGui = guiCreateBlock(self.addBlock)
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
        self.addWhenGui.ui.pushButtonOK.clicked.connect(lambda: self.addBlockWhen(isOK=True))
        self.addWhenGui.ui.pushButtonCancel.clicked.connect(lambda: self.addBlockWhen(isOK=False))
        self.addWhenGui.open()

    def addBlockWhen(self, isOK=True):
        if isOK:
            name = self.addWhenGui.nameControl.replace(" ", "_")
            if not self.addWhenGui.ui.Run_start.isChecked() and name == "start":
                msgBox = QtWidgets.QMessageBox()
                msgBox.setWindowTitle(self.tr("Warning"))
                msgBox.setIcon(QtWidgets.QMessageBox.Warning)
                msgBox.setText(self.tr("Error the name can not be 'start'"))
                msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                msgBox.setDefaultButton(QtWidgets.QMessageBox.Ok)
                ret = msgBox.exec_()
                return
            if name == "":
                msgBox = QtWidgets.QMessageBox()
                msgBox.setWindowTitle(self.tr("Warning"))
                msgBox.setIcon(QtWidgets.QMessageBox.Warning)
                msgBox.setText(self.tr("Error Name is empty."))
                msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                msgBox.setDefaultButton(QtWidgets.QMessageBox.Ok)
                ret = msgBox.exec_()
                return
            if name in keyword.kwlist:
                msgBox = QtWidgets.QMessageBox()
                msgBox.setWindowTitle(self.tr("Warning"))
                msgBox.setIcon(QtWidgets.QMessageBox.Warning)
                msgBox.setText(self.tr("This name is reserved"))
                msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                msgBox.setDefaultButton(QtWidgets.QMessageBox.Ok)
                ret = msgBox.exec_()
                return
            if name in self.listNameVars or name in [name for name, _ in
                                                     self.listNameWhens] or name in self.listNameUserFunctions or name in self.listNameLibraryFunctions:
                msgBox = QtWidgets.QMessageBox()
                msgBox.setWindowTitle(self.tr("Warning"))
                msgBox.setIcon(QtWidgets.QMessageBox.Warning)
                msgBox.setText(self.tr("This name already exists"))
                msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                msgBox.setDefaultButton(QtWidgets.QMessageBox.Ok)
                ret = msgBox.exec_()
                return
            text = self.addWhenGui.value
            imgPath = self.addWhenGui.imgName
            configImgPath = os.path.splitext(imgPath)[0]
            blockType, connections = loadConfigBlock(configImgPath)

            block = AbstractBlock(0, 0, "when", {'ES': "Cuando ", 'EN': "When "}, imgPath, [], HUE_WHEN,
                                  self.addWhenGui.nameControl.replace(" ", "_"), connections, blockType, WHEN)
            if self.addWhenGui.nameControl != "start":
                self.addButtonsWhens(configImgPath, self.addWhenGui.nameControl.replace(" ", "_"))
                self.listNameWhens.append((name, configImgPath))
            self.scene.addItem(block)
            self.addWhenGui.close()
        else:
            self.addWhenGui.close()

    def addButtonsWhens(self, configImgPath, name):
        if os.path.basename(configImgPath) == 'block8':
            blockType, connections = loadConfigBlock(os.path.join(pathBlocks, "block1"))
            table = self.dicTables['control']

            table.insertRow(table.rowCount())
            button = Block_Button(
                (self, "activate " + name, {'ES': "Activar " + name, 'EN': "Activate " + name}, HUE_WHEN,
                 self.view, self.scene, os.path.join(pathBlocks, "block1.png"), connections, [], blockType,
                 table, table.rowCount() - 1, VARIABLE,
                 {'ES': "Activa el evento " + name, 'EN': "Activate the event " + name}))
            self.listButtonsWhen.append(button)
            self.listButtons.append(button)
            table.setCellWidget(table.rowCount() - 1, 0, button)

            table.insertRow(table.rowCount())
            button = Block_Button(
                (self, "deactivate " + name, {'ES': "Desactivar " + name, 'EN': "Deactivate " + name}, HUE_WHEN,
                 self.view, self.scene, os.path.join(pathBlocks, "block1.png"), connections, [], blockType,
                 table, table.rowCount() - 1, VARIABLE,
                 {'ES': "Desactiva el evento " + name, 'EN': "Deactivate the event " + name}))
            self.listButtonsWhen.append(button)
            self.listButtons.append(button)
            table.setCellWidget(table.rowCount() - 1, 0, button)
            # table.insertRow(table.rowCount())

        table = self.dicTables['control']
        for img in ["block3", "block4"]:
            table.insertRow(table.rowCount())
            blockType, connections = loadConfigBlock(os.path.join(pathBlocks, img))
            button = Block_Button((self, "state_" + name, {'ES': "Estado_" + name, 'EN': "State_" + name}, HUE_WHEN,
                                   self.view, self.scene, os.path.join(pathBlocks, img + ".png"), connections, [],
                                   blockType,
                                   table, table.rowCount() - 1, VARIABLE,
                                   {'ES': "Variable que dice si el evento " + name + " esta activo", 'EN': ""}))
            self.listButtonsWhen.append(button)
            self.listButtons.append(button)
            table.setCellWidget(table.rowCount() - 1, 0, button)

        for x in ["block3", "block4"]:
            blockType, connections = loadConfigBlock(os.path.join(pathBlocks, x))

            table.insertRow(table.rowCount())
            button = Block_Button(
                (self, "time_" + name, {'ES': "Tiempo_" + name, 'EN': "Time_" + name}, HUE_WHEN, self.view,
                 self.scene, os.path.join(pathBlocks, x + ".png"), connections, [], blockType, table,
                 table.rowCount() - 1, VARIABLE,
                 {'ES': "Es el numero de segundos que lleva en ejecucion el evento " + name,
                  'EN': " " + name}))
            self.listButtonsWhen.append(button)
            self.listButtons.append(button)
            table.setCellWidget(table.rowCount() - 1, 0, button)

        self.ui.deleteWhenpushButton.setEnabled(True)

    def generateStopTmpFile(self):
        name_client = self.ui.clientscomboBox.currentText()
        text = HEADER.replace('<Client>', name_client)
        text += '\nrobot.stop_bot()'
        text = cleanCode(text)
        with open(os.path.join(tempfile.gettempdir(), "stop_main_tmp.py"), "w+") as fh:
            fh.writelines(text)

    def stopthread(self):
        if self.hilo is not None:
            try:
                self.hilo.terminate()
            except Exception as e:
                print(e.with_traceback())
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
        if inst[0] in ["while", "while True"]:
            text += "\n\t" * (ntab - 1) + "end"
        if inst[0] == "else" or (inst[0] in ["if", "elif"] and (inst[1]["BOTTOM"] is None or (
                inst[1]["BOTTOM"] is not None and inst[1]["BOTTOM"][0] not in ["elif", "else"]))):
            text += "\n" + "\t" * (ntab - 1) + "end"
        if inst[1]["BOTTOM"] is not None:
            text += "\n" + "\t" * (ntab - 1) + self.toLBotPy(inst[1]["BOTTOM"], ntab)
        return text

    def newVariable(self):
        self.addVarGui = AddVar.Ui_Dialog()
        self.addVarDialog = QtWidgets.QDialog()
        self.addVarGui.setupUi(self.addVarDialog)
        self.addVarDialog.open()
        self.addVarGui.cancelPushButton.clicked.connect(lambda: self.retaddVarGui(0))
        self.addVarGui.okPushButton.clicked.connect(lambda: self.retaddVarGui(1))

    def retaddVarGui(self, ret):
        if ret is 1:
            name = self.addVarGui.nameLineEdit.text().replace(" ", "_")
            if name == 'start':
                msgBox = QtWidgets.QMessageBox()
                msgBox.setWindowTitle(self.tr("Warning"))
                msgBox.setIcon(QtWidgets.QMessageBox.Warning)
                msgBox.setText(self.tr("Error the name can not be 'start'"))
                msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                msgBox.setDefaultButton(QtWidgets.QMessageBox.Ok)
                ret = msgBox.exec_()
                return
            if name in keyword.kwlist:
                msgBox = QtWidgets.QMessageBox()
                msgBox.setWindowTitle(self.tr("Warning"))
                msgBox.setIcon(QtWidgets.QMessageBox.Warning)
                msgBox.setText(self.tr("This name is reserved"))
                msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                msgBox.setDefaultButton(QtWidgets.QMessageBox.Ok)
                ret = msgBox.exec_()
                return
            if name in self.listNameVars or name in [name for name, _ in
                                                     self.listNameWhens] or name in self.listNameUserFunctions or name in self.listNameLibraryFunctions:
                msgBox = QtWidgets.QMessageBox()
                msgBox.setWindowTitle(self.tr("Warning"))
                msgBox.setIcon(QtWidgets.QMessageBox.Warning)
                msgBox.setText(self.tr("This name already exists"))
                msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                msgBox.setDefaultButton(QtWidgets.QMessageBox.Ok)
                ret = msgBox.exec_()
                return
            if len(name) != 0 and name[0].isdigit():
                msgBox = QtWidgets.QMessageBox()
                msgBox.setWindowTitle(self.tr("Warning"))
                msgBox.setIcon(QtWidgets.QMessageBox.Warning)
                msgBox.setText(self.tr("The name can't start by number"))
                msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                msgBox.setDefaultButton(QtWidgets.QMessageBox.Ok)
                ret = msgBox.exec_()
                return
            if len(name) == 0:
                msgBox = QtWidgets.QMessageBox()
                msgBox.setWindowTitle(self.tr("Warning"))
                msgBox.setIcon(QtWidgets.QMessageBox.Warning)
                msgBox.setText(self.tr("Error Name is empty."))
                msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                msgBox.setDefaultButton(QtWidgets.QMessageBox.Ok)
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
        variables.append(Variable("float", "set to ", "0", {"ES": " poner a ", "EN": " set to "}))
        button = Block_Button((self, name, {"ES": name + " poner a ", "EN": name + " set to "}, HUE_WHEN, self.view,
                               self.scene, os.path.join(pathBlocks, "block1.png"), connections,
                               variables, blockType, table, table.rowCount() - 1, VARIABLE, {}))
        self.listButtons.append(button)
        table.setCellWidget(table.rowCount() - 1, 0, button)
        self.listVars.append(button.getAbstracBlockItem())
        for img in imgs:
            blockType, connections = loadConfigBlock(os.path.join(pathBlocks, img))
            table = self.dicTables['variables']
            table.insertRow(table.rowCount())
            button = Block_Button((self, name, {}, HUE_VARIABLE, self.view, self.scene,
                                   os.path.join(pathBlocks, img + ".png"), connections,
                                   [], blockType, table, table.rowCount() - 1, VARIABLE, {}))
            self.listButtons.append(button)
            table.setCellWidget(table.rowCount() - 1, 0, button)
            self.listVars.append(button.getAbstracBlockItem())
        self.savetmpProject()

    def deleteVar(self):
        self.delVarGui = DelVar.Ui_Dialog()
        self.delVarDialgo = QtWidgets.QDialog()
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
        for item, row in [(table.cellWidget(r, 0), r) for r in reversed(range(0, table.rowCount())) if
                          table.cellWidget(r, 0).getText() == name]:
            item.delete(row)
            item.removeTmpFile()
            self.listButtons.remove(item)
        self.listNameVars.remove(name)
        self.savetmpProject()

    def deleteWhen(self):
        self.delWhenGui = DelWhen.Ui_Dialog()
        self.delWhenDialgo = QtWidgets.QDialog()
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
        for item, row in [(table.cellWidget(r, 0), r) for r in rango if
                          table.cellWidget(r, 0).getText() in [name, "activate " + name, "deactivate " + name,
                                                               "time_" + name, "state_" + name]]:
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
        self.userFunctionsDialgo = QtWidgets.QDialog()
        self.userFunctionsGui.setupUi(self.userFunctionsDialgo)
        self.userFunctionsDialgo.open()
        self.userFunctionsGui.cancelPushButton.clicked.connect(lambda: self.retUserFunctions(0))
        self.userFunctionsGui.okPushButton.clicked.connect(lambda: self.retUserFunctions(1))

    def retUserFunctions(self, ret):
        if ret is 1:
            name = self.userFunctionsGui.nameLineEdit.text()
            name = name.replace(" ", "_")
            if name == 'start':
                msgBox = QtWidgets.QMessageBox()
                msgBox.setWindowTitle(self.tr("Warning"))
                msgBox.setIcon(QtWidgets.QMessageBox.Warning)
                msgBox.setText(self.tr("Error the name can not be 'start'"))
                msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                msgBox.setDefaultButton(QtWidgets.QMessageBox.Ok)
                ret = msgBox.exec_()
                return
            if name in keyword.kwlist:
                msgBox = QtWidgets.QMessageBox()
                msgBox.setWindowTitle(self.tr("Warning"))
                msgBox.setIcon(QtWidgets.QMessageBox.Warning)
                msgBox.setText(self.tr("This name is reserved"))
                msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                msgBox.setDefaultButton(QtWidgets.QMessageBox.Ok)
                ret = msgBox.exec_()
                return
            if name in self.listNameVars or name in [name for name, _ in
                                                     self.listNameWhens] or name in self.listNameUserFunctions or name in self.listNameLibraryFunctions:
                msgBox = QtWidgets.QMessageBox()
                msgBox.setWindowTitle(self.tr("Warning"))
                msgBox.setIcon(QtWidgets.QMessageBox.Warning)
                msgBox.setText(self.tr("This name already exists"))
                msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                msgBox.setDefaultButton(QtWidgets.QMessageBox.Ok)
                ret = msgBox.exec_()
                return
            if len(name) != 0 and name[0].isdigit():
                msgBox = QtWidgets.QMessageBox()
                msgBox.setWindowTitle(self.tr("Warning"))
                msgBox.setIcon(QtWidgets.QMessageBox.Warning)
                msgBox.setText(self.tr("The name can't start by number"))
                msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                msgBox.setDefaultButton(QtWidgets.QMessageBox.Ok)
                ret = msgBox.exec_()
                return
            if len(name) == 0:
                msgBox = QtWidgets.QMessageBox()
                msgBox.setWindowTitle(self.tr("Warning"))
                msgBox.setIcon(QtWidgets.QMessageBox.Warning)
                msgBox.setText(self.tr("Error Name is empty."))
                msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                msgBox.setDefaultButton(QtWidgets.QMessageBox.Ok)
                ret = msgBox.exec_()
                return
            self.addUserFunction(name)
            self.savetmpProject()

        self.userFunctionsDialgo.close()

    def addUserFunction(self, name):
        self.ui.deleteFuntionsPushButton.setEnabled(True)
        imgs = ['block8', 'block1']
        self.listNameUserFunctions.append(name)
        table = self.dicTables['functions']
        i = 0
        for img in imgs:
            blockType, connections = loadConfigBlock(os.path.join(pathBlocks, img))
            table.insertRow(table.rowCount())
            button = Block_Button((self, name, {}, HUE_USERFUNCTION, self.view, self.scene,
                                   os.path.join(pathBlocks, img + ".png"), connections,
                                   [], blockType, table, table.rowCount() - 1, USERFUNCTION, {}))
            self.listButtons.append(button)
            table.setCellWidget(table.rowCount() - 1, 0, button)
            self.listUserFunctions.append(button.getAbstracBlockItem())
            i += 1

    def deleteUserFunctions(self):
        self.delUserFunctionsGui = DelVar.Ui_Dialog()
        self.delUserFunctionsDialgo = QtWidgets.QDialog()
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
        table = self.dicTables['functions']
        rango = reversed(range(0, table.rowCount()))
        for item, row in [(table.cellWidget(r, 0), r) for r in rango if table.cellWidget(r, 0).getText() == name]:
            item.delete(row)
            item.removeTmpFile()
            self.listButtons.remove(item)
        self.listNameUserFunctions.remove(name)
        self.savetmpProject()
