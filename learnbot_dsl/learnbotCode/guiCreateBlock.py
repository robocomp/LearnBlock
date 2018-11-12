from __future__ import print_function, absolute_import
import os, tempfile, json
from PySide import QtGui
import learnbot_dsl.guis.CreateBlock as CreateBlock
from learnbot_dsl.blocksConfig.blocks import pathBlocks
from learnbot_dsl.blocksConfig.parserConfigBlock import pathConfig
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
            listBlock.append(os.path.join(base,f))
            archivo, extension = os.path.splitext(f)
            listNameBlocks.append(archivo)

listTypeBlock = ["control",
                 "motor",
                 "perceptual",
                 "proprioceptive",
                 "operator",
                 "express",
                 "others"]

pythonCode = """from __future__ import print_function, absolute_import

def <name>(lbot, <args>):
    pass
"""


class guiCreateBlock(QtGui.QDialog):

    def __init__(self, load_block):
        QtGui.QDialog.__init__(self)
        self.load_blocks = load_block
        self.blockType = None
        self.FuntionType = None
        self.img = None
        self.listImg = []
        self.ui = CreateBlock.Ui_Dialog()

        self.ui.setupUi(self)
        self.__updateBlockType(0)
        self.__updateImage(0)
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
                args += self.ui.tableWidgetVars.cellWidget(row, 1).text() + "=" + self.ui.tableWidgetVars.cellWidget(row, 2).text() + ", "
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
        self.ui.tableWidgetToolTip.setCellWidget(row, 0, QtGui.QLineEdit())
        self.ui.tableWidgetToolTip.setCellWidget(row, 1, QtGui.QLineEdit())
        self.ui.pushButtonRemoveTooltip.setEnabled(True)

    def __addlanguages(self):
        row = self.ui.tableWidgetlanguages.rowCount()
        self.ui.tableWidgetlanguages.insertRow(row)
        self.ui.tableWidgetlanguages.setCellWidget(row, 0, QtGui.QLineEdit())
        self.ui.tableWidgetlanguages.setCellWidget(row, 1, QtGui.QLineEdit())
        self.ui.pushButtonRemovelanguages.setEnabled(True)

    def __addVar(self):
        row = self.ui.tableWidgetVars.rowCount()
        self.ui.tableWidgetVars.insertRow(row)
        self.ui.tableWidgetVars.setCellWidget(row, 0, QtGui.QLabel("float"))
        edit = QtGui.QLineEdit()
        edit.textChanged.connect(lambda: self.__updateImage(self.ui.comboBoxBlockImage.currentIndex()))
        self.ui.tableWidgetVars.setCellWidget(row, 1, edit)
        edit = QtGui.QLineEdit()
        edit.textChanged.connect(lambda: self.__updateImage(self.ui.comboBoxBlockImage.currentIndex()))
        edit.setValidator(QtGui.QDoubleValidator())
        self.ui.tableWidgetVars.setCellWidget(row, 2, edit)
        self.ui.pushButtonRemoveVar.setEnabled(True)

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
            self.ui.listWidgetBlockImage.addItem(QtGui.QListWidgetItem(self.img))
            self.listImg.append(self.img)
            self.ui.pushButtonRemoveBlockImage.setEnabled(True)

    def __removeImage(self):

        index = self.ui.listWidgetBlockImage.currentRow()
        self.listImg.pop(index)
        self.ui.listWidgetBlockImage.takeItem(index)
        if len(self.listImg) == 0:
            self.ui.pushButtonRemoveBlockImage.setEnabled(False)

    def __buttons(self, ret):
        if ret is 1:
            ret = None
            name = self.ui.lineEditName.text().replace(" ", "_")
            if name == "":
                msgBox = QtGui.QMessageBox()
                msgBox.setWindowTitle(self.trUtf8("Warning"))
                msgBox.setIcon(QtGui.QMessageBox.Warning)
                msgBox.setText(self.trUtf8("Error Name is empty."))
                msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
                msgBox.setDefaultButton(QtGui.QMessageBox.Ok)
                ret = msgBox.exec_()
            if name not in functions.keys():
                msgBox = QtGui.QMessageBox()
                msgBox.setWindowTitle(self.trUtf8("Warning"))
                msgBox.setIcon(QtGui.QMessageBox.Warning)
                msgBox.setText(self.trUtf8("This name alredy exist"))
                msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
                msgBox.setDefaultButton(QtGui.QMessageBox.Ok)
                ret = msgBox.exec_()
            elif len(self.listImg) is 0:
                msgBox = QtGui.QMessageBox()
                msgBox.setWindowTitle(self.trUtf8("Warning"))
                msgBox.setIcon(QtGui.QMessageBox.Warning)
                msgBox.setText(self.trUtf8("Error Images of block is empty."))
                msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
                msgBox.setDefaultButton(QtGui.QMessageBox.Ok)
                ret = msgBox.exec_()
            elif self.__repitNameVar():
                msgBox = QtGui.QMessageBox()
                msgBox.setWindowTitle(self.trUtf8("Warning"))
                msgBox.setIcon(QtGui.QMessageBox.Warning)
                msgBox.setText(self.trUtf8("Error name of vars is repit, name is empty or default value is empty."))
                msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
                msgBox.setDefaultButton(QtGui.QMessageBox.Ok)
                ret = msgBox.exec_()
            if ret is not None:
                return

            dictBlock = {}
            dictBlock["type"] = self.blockType
            dictBlock["name"] = self.ui.lineEditName.text()
            if self.ui.tableWidgetVars.rowCount() is not 0:
                listVariables = []
                for row in range(0, self.ui.tableWidgetVars.rowCount()):
                    v = {}
                    v["type"] = self.ui.tableWidgetVars.cellWidget(row, 0).text()
                    v["name"] = self.ui.tableWidgetVars.cellWidget(row, 1).text()
                    v["default"] = self.ui.tableWidgetVars.cellWidget(row, 2).text()
                    listVariables.append(v)
                dictBlock["variables"] = listVariables
            listImgs = []
            for img in self.listImg:
                listImgs.append(img)
            dictBlock["img"] = listImgs
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

            msgBox = QtGui.QMessageBox()
            msgBox.setWindowTitle(self.trUtf8("Warning"))
            msgBox.setIcon(QtGui.QMessageBox.Warning)
            msgBox.setText(self.trUtf8("Are you sure you want to add this function?"))
            msgBox.setInformativeText(str(dictBlock))
            msgBox.setStandardButtons(QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
            msgBox.setDefaultButton(QtGui.QMessageBox.Cancel)
            ret = msgBox.exec_()
            if ret == QtGui.QMessageBox.Ok:
                with open(os.path.join(tempfile.gettempdir(), "block", self.ui.lineEditName.text() + ".conf"), 'w') as file:
                    json.dump([dictBlock], file)
                with open(os.path.join(tempfile.gettempdir(), "functions", self.ui.lineEditName.text() + ".py"), 'w') as file:
                    code = self.ui.textEditPythonCode.toPlainText()
                    file.write(code)
            else:
                return
            self.load_blocks()
        self.close()

    def __repitNameVar(self):
        varlist = []
        if self.ui.tableWidgetVars.rowCount() is not 0:
            for row in range(0, self.ui.tableWidgetVars.rowCount()):
                if self.ui.tableWidgetVars.cellWidget(row, 1).text() in varlist or self.ui.tableWidgetVars.cellWidget(
                        row, 1).text() == "" \
                        or self.ui.tableWidgetVars.cellWidget(row, 2).text() == "":
                    return True
                varlist.append(self.ui.tableWidgetVars.cellWidget(row, 1).text())
        return False
