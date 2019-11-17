from __future__ import print_function, absolute_import
import os, tempfile, json
from PySide2 import QtGui, QtWidgets, QtCore
import learnbot_dsl.guis.CreateBlock as CreateBlock
from learnbot_dsl.blocksConfig.blocks import pathBlocks
from learnbot_dsl.blocksConfig.parserConfigBlock import pathConfig
from learnbot_dsl.blocksConfig.parserConfigBlock import getOrigNameBlock
from learnbot_dsl.learnbotCode.Block import *
from learnbot_dsl.learnbotCode.toQImage import *
from learnbot_dsl.functions import getFuntions
listBlock = []
listNameBlocks = []
functions = getFuntions()
for base, dirs, files in os.walk(pathBlocks):
    for f in files:
        archivo, extension = os.path.splitext(base + "/" + f)
        if extension == ".png" and "block" in f and "azul" not in f:
            archivo, extension = os.path.splitext(f)
            if archivo in ["block1", "block3", "block4"]:
                listBlock.append(os.path.join(base,f))
                listNameBlocks.append(getOrigNameBlock(archivo))

listTypeBlock = ["express",
                 "motor",
                 "perceptual",
                 "proprioceptive",
                 "others"]

pythonCode = """from __future__ import print_function, absolute_import

def <name>(lbot, <args>):
    pass
"""


class guiCreateBlock(QtWidgets.QDialog):

    def __init__(self, load_block):
        QtWidgets.QDialog.__init__(self)
        self.load_blocks = load_block
        self.blockType = None
        self.FuntionType = None
        self.img = None
        self.listImg = []
        self.ui = CreateBlock.Ui_Dialog()

        self.ui.setupUi(self)
        self.__updateBlockType(0)
        self.__updateImage(0)
        self.ui.tableWidgetToolTip.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.ui.tableWidgetVars.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        self.ui.tableWidgetlanguages.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        for name in listNameBlocks:
            self.ui.comboBoxBlockImage.addItem(name)
        self.ui.comboBoxBlockImage.currentIndexChanged.connect(self.__updateImage)
        self.ui.comboBoxBlockType.currentIndexChanged.connect(self.__updateBlockType)
        self.ui.pushButtonAddVar.clicked.connect(self.__addVar)
        self.ui.pushButtonRemoveVar.clicked.connect(lambda : self.__delVar(self.ui.tableWidgetVars, self.ui.pushButtonAddVar))
        self.ui.pushButtonAddlanguages.clicked.connect(self.__addlanguages)
        self.ui.pushButtonRemovelanguages.clicked.connect(lambda : self.__delVar(self.ui.tableWidgetVars, self.ui.pushButtonAddVar))
        self.ui.pushButtonAddTooltip.clicked.connect(self.__addTooltip)
        self.ui.pushButtonRemoveTooltip.clicked.connect(lambda : self.__delVar(self.ui.tableWidgetVars, self.ui.pushButtonAddVar))
        self.ui.pushButtonAddBlockImage.clicked.connect(self.__addImage)
        self.ui.pushButtonRemoveBlockImage.clicked.connect(self.__removeImage)
        self.ui.pushButtonRemoveVar.setEnabled(False)
        self.ui.pushButtonRemoveBlockImage.setEnabled(False)
        self.ui.pushButtonConfigFile.clicked.connect(self.__selectConfigFile)
        self.ui.pushButtonOK.clicked.connect(lambda: self.__buttons(1))
        self.ui.pushButtonCancel.clicked.connect(lambda: self.__buttons(0))
        self.ui.lineEditName.textChanged.connect(lambda: self.__updateImage(self.ui.comboBoxBlockImage.currentIndex()))

    def __updateImage(self, index):
        name = self.ui.lineEditName.text().replace(" ","_")
        code = pythonCode.replace("<name>", name)
        args = ""
        vars = None
        if self.ui.tableWidgetVars.rowCount() is not 0:
            vars = []
            args = ", "
            for row in range(0, self.ui.tableWidgetVars.rowCount()):
                args += self.ui.tableWidgetVars.cellWidget(row, 1).text() + "="
                if self.ui.tableWidgetVars.cellWidget(row, 0).currentText() == "string":
                    args += '"' + self.ui.tableWidgetVars.cellWidget(row, 2).text() + '", '
                else:
                    args += self.ui.tableWidgetVars.cellWidget(row, 2).text() + ', '

                vars.append(self.ui.tableWidgetVars.cellWidget(row, 1).text())
            args = args[:-2]
        code = code.replace(", <args>",args)
        self.ui.textEditPythonCode.setText(code)
        self.img = listNameBlocks[index]
        img = cv2.imread(listBlock[index], cv2.IMREAD_UNCHANGED)
        archivo, extension = os.path.splitext(listBlock[index])
        blockType, connections = loadConfigBlock(archivo)
        img = generateBlock(img, 34, name, blockType,vars_=vars,type_=FUNTION)
        qImage = toQImage(img)
        self.ui.BlockImage.setPixmap(QtGui.QPixmap(qImage))

    def __updateBlockType(self, index):
        self.blockType = listTypeBlock[index]

    def __addTooltip(self):
        row = self.ui.tableWidgetToolTip.rowCount()
        self.ui.tableWidgetToolTip.insertRow(row)
        self.ui.tableWidgetToolTip.setCellWidget(row, 0, QtWidgets.QLineEdit())
        self.ui.tableWidgetToolTip.setCellWidget(row, 1, QtWidgets.QLineEdit())
        self.ui.pushButtonRemoveTooltip.setEnabled(True)

    def __addlanguages(self):
        row = self.ui.tableWidgetlanguages.rowCount()
        self.ui.tableWidgetlanguages.insertRow(row)
        self.ui.tableWidgetlanguages.setCellWidget(row, 0, QtWidgets.QLineEdit())
        self.ui.tableWidgetlanguages.setCellWidget(row, 1, QtWidgets.QLineEdit())
        self.ui.pushButtonRemovelanguages.setEnabled(True)

    def __addVar(self):
        row = self.ui.tableWidgetVars.rowCount()
        self.ui.tableWidgetVars.insertRow(row)
        combobox = QtWidgets.QComboBox()
        combobox.addItem("float")
        combobox.addItem("string")
        combobox.addItem("int")
        combobox.addItem("boolean")
        combobox.currentIndexChanged.connect(lambda : self.setdefaultWidget(row))
        self.ui.tableWidgetVars.setCellWidget(row, 0, combobox)
        edit = QtWidgets.QLineEdit()
        edit.textChanged.connect(lambda: self.__updateImage(self.ui.comboBoxBlockImage.currentIndex()))
        self.ui.tableWidgetVars.setCellWidget(row, 1, edit)
        edit = QtWidgets.QLineEdit()
        edit.textChanged.connect(lambda: self.__updateImage(self.ui.comboBoxBlockImage.currentIndex()))
        edit.setValidator(QtGui.QDoubleValidator())
        self.ui.tableWidgetVars.setCellWidget(row, 2, edit)
        self.ui.pushButtonRemoveVar.setEnabled(True)

    def setdefaultWidget(self,row):
        type = self.ui.tableWidgetVars.cellWidget(row, 0).currentText()
        if type == "float":
            edit = QtWidgets.QLineEdit()
            edit.textChanged.connect(lambda: self.__updateImage(self.ui.comboBoxBlockImage.currentIndex()))
            edit.setValidator(QtGui.QDoubleValidator())
            self.ui.tableWidgetVars.setCellWidget(row, 2, edit)
        elif type == "string":
            edit = QtWidgets.QLineEdit()
            edit.textChanged.connect(lambda: self.__updateImage(self.ui.comboBoxBlockImage.currentIndex()))
            self.ui.tableWidgetVars.setCellWidget(row, 2, edit)
        elif type == "int":
            edit = QtWidgets.QLineEdit()
            edit.textChanged.connect(lambda: self.__updateImage(self.ui.comboBoxBlockImage.currentIndex()))
            edit.setValidator(QtGui.QIntValidator())
            self.ui.tableWidgetVars.setCellWidget(row, 2, edit)
        elif type == "boolean":
            combobox = QtWidgets.QComboBox()
            combobox.addItem("True")
            combobox.addItem("False")
            combobox.currentIndexChanged.connect(lambda: self.__updateImage(self.ui.comboBoxBlockImage.currentIndex()))
            self.ui.tableWidgetVars.setCellWidget(row, 2, combobox)


    def __delete(self,table, buton):
        table.removeRow(table.currentRow())
        if table.rowCount() == 0:
            buton.setEnabled(False)

    def __clear(self):
        self.ui.lineEditFile.clear()
        self.ui.lineEditName.clear()
        self.ui.comboBoxFuntionType.setCurrentIndex(0)
        self.ui.comboBoxBlockImage.setCurrentIndex(0)

    def __addImage(self):
        if self.img not in self.listImg:
            self.ui.listWidgetBlockImage.addItem(QtWidgets.QListWidgetItem(self.img))
            self.listImg.append(self.img)
            self.ui.pushButtonRemoveBlockImage.setEnabled(True)

    def __removeImage(self):

        index = self.ui.listWidgetBlockImage.currentRow()
        self.listImg.pop(index)
        self.ui.listWidgetBlockImage.takeItem(index)
        if len(self.listImg) == 0:
            self.ui.pushButtonRemoveBlockImage.setEnabled(False)

    def __selectConfigFile(self):
        configPath = self.ui.lineEditConfigFile.text()
        if self.ui.lineEditConfigFile.text() == "":
            initialConfigPath = pathConfig
        else:
            initialConfigPath = os.path.dirname(configPath)

        configFile, _ = QtWidgets.QFileDialog.getSaveFileName(self, self.tr("Select configuration file"), initialConfigPath, filter = "*.conf", options = QtWidgets.QFileDialog.DontConfirmOverwrite)
        if configFile != "" and (os.path.exists(configFile) or os.path.exists(os.path.dirname(configFile))):
            self.ui.lineEditConfigFile.setText(configFile)
        print("selection of config file", configFile)

    def __buttons(self, ret):
        if ret is 1:
            ret = None
            name = self.ui.lineEditName.text().replace(" ", "_")
            category = self.ui.lineEditCategory.text()
            configFile = self.ui.lineEditConfigFile.text()
            if name == "":
                msgBox = QtWidgets.QMessageBox()
                msgBox.setWindowTitle(self.tr("Error"))
                msgBox.setIcon(QtWidgets.QMessageBox.Warning)
                msgBox.setText(self.tr("Block name is empty"))
                msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                msgBox.setDefaultButton(QtWidgets.QMessageBox.Ok)
                ret = msgBox.exec_()
            if name in functions.keys():
                msgBox = QtWidgets.QMessageBox()
                msgBox.setWindowTitle(self.tr("Error"))
                msgBox.setIcon(QtWidgets.QMessageBox.Warning)
                msgBox.setText(self.tr("This name already exists"))
                msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                msgBox.setDefaultButton(QtWidgets.QMessageBox.Ok)
                ret = msgBox.exec_()
            elif len(self.listImg) is 0:
                msgBox = QtWidgets.QMessageBox()
                msgBox.setWindowTitle(self.tr("Error"))
                msgBox.setIcon(QtWidgets.QMessageBox.Warning)
                msgBox.setText(self.tr("Images of block is empty"))
                msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                msgBox.setDefaultButton(QtWidgets.QMessageBox.Ok)
                ret = msgBox.exec_()
            elif self.__repeatNameVar():
                msgBox = QtWidgets.QMessageBox()
                msgBox.setWindowTitle(self.tr("Error"))
                msgBox.setIcon(QtWidgets.QMessageBox.Warning)
                msgBox.setText(self.tr("Name of variable already exists, name is empty or default value is empty."))
                msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                msgBox.setDefaultButton(QtWidgets.QMessageBox.Ok)
                ret = msgBox.exec_()
            elif configFile == "":
                msgBox = QtWidgets.QMessageBox()
                msgBox.setWindowTitle(self.tr("Error"))
                msgBox.setIcon(QtWidgets.QMessageBox.Warning)
                msgBox.setText(self.tr("No valid configuration file was chosen"))
                msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                msgBox.setDefaultButton(QtWidgets.QMessageBox.Ok)
                ret = msgBox.exec_()
            elif category == "":
                msgBox = QtWidgets.QMessageBox()
                msgBox.setWindowTitle(self.tr("Error"))
                msgBox.setIcon(QtWidgets.QMessageBox.Warning)
                msgBox.setText(self.tr("Block category is empty"))
                msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                msgBox.setDefaultButton(QtWidgets.QMessageBox.Ok)
                ret = msgBox.exec_()


            if ret is not None:
                return

            dictBlock = {}
            dictBlock["type"] = self.blockType
            dictBlock["category"] = category
            dictBlock["name"] = self.ui.lineEditName.text()
            if self.ui.tableWidgetVars.rowCount() is not 0:
                listVariables = []
                for row in range(0, self.ui.tableWidgetVars.rowCount()):
                    v = {}
                    v["type"] = self.ui.tableWidgetVars.cellWidget(row, 0).currentText()
                    v["name"] = self.ui.tableWidgetVars.cellWidget(row, 1).text()
                    v["default"] = self.ui.tableWidgetVars.cellWidget(row, 2).text()
                    listVariables.append(v)
                dictBlock["variables"] = listVariables
            listImgs = []
            for img in self.listImg:
                listImgs.append(img)
            dictBlock["shape"] = listImgs
            
            if self.ui.tableWidgetlanguages.rowCount() is not 0:
                dictLanguages = {}
                for row in range(0, self.ui.tableWidgetlanguages.rowCount()):
                    dictLanguages[self.ui.tableWidgetlanguages.cellWidget(row, 0).text()] = self.ui.tableWidgetlanguages.cellWidget(row, 1).text()
                dictBlock["languages"] = dictLanguages
            if self.ui.tableWidgetToolTip.rowCount() is not 0:
                dictToolTip = {}
                for row in range(0, self.ui.tableWidgetToolTip.rowCount()):
                    dictToolTip[self.ui.tableWidgetToolTip.cellWidget(row, 0).text()] = self.ui.tableWidgetToolTip.cellWidget(row, 1).text()
                dictBlock["tooltip"] = dictToolTip

            if os.path.exists(configFile):
                with open(configFile, 'r') as file:
                    listOfBlocks = json.load(file)
            else:
                listOfBlocks = []
            listOfBlocks.append(dictBlock)
            with open(configFile, 'w') as file:
                json.dump(listOfBlocks, file, indent=4)
            with open(os.path.join(tempfile.gettempdir(), "functions", self.ui.lineEditName.text() + ".py"), 'w') as file:
                code = self.ui.textEditPythonCode.toPlainText()
                file.write(code)

            self.load_blocks(dictBlock)

            msgBox = QtWidgets.QMessageBox()
            msgBox.setWindowTitle(self.tr("Block created"))
            msgBox.setIcon(QtWidgets.QMessageBox.Information)
            msgBox.setText(self.tr("New Python file created at ")+ os.path.join(tempfile.gettempdir(), "functions"))
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msgBox.setDefaultButton(QtWidgets.QMessageBox.Ok)
            ret = msgBox.exec_()

        self.close()

    def __repeatNameVar(self):
        varlist = []
        if self.ui.tableWidgetVars.rowCount() is not 0:
            for row in range(0, self.ui.tableWidgetVars.rowCount()):
                if self.ui.tableWidgetVars.cellWidget(row, 1).text() in varlist or self.ui.tableWidgetVars.cellWidget(
                        row, 1).text() == "" \
                        or self.ui.tableWidgetVars.cellWidget(row, 2).text() == "":
                    return True
                varlist.append(self.ui.tableWidgetVars.cellWidget(row, 1).text())
        return False
