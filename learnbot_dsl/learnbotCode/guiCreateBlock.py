import guis.createBlock as createBlock
from VisualFuntion import *
import os
from blocksConfig import pathBlocks, pathConfig
listBlock = []
listNameBlocks = []
import cv2

for base, dirs, files in os.walk(pathBlocks):
    for f in files:
        archivo, extension = os.path.splitext(base+"/"+f)
        if extension == ".png" and "block" in f and "azul" not in f:
            listBlock.append(base+"/"+f)
            archivo, extension = os.path.splitext(f)
            listNameBlocks.append(archivo)

listTypeBlock = ["control",
                 "motor",
                 "perceptive",
                 "propioperceptive",
                 "operator"]

listconfig = ["configControl",
              "configMotor",
              "configOperators",
              "configPerceptual"
              "configPropriopercetive"]

class guiCreateBlock(QtGui.QDialog):

    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.blockType = None
        self.FuntionType = None
        self.img = None
        self.listImg = []
        self.ui = createBlock.Ui_Dialog()

        self.ui.setupUi(self)
        self.__updateBlockType(0)
        self.__updateImage(0)
        for name in listNameBlocks:
            self.ui.comboBoxBlockImage.addItem(name)
        self.ui.comboBoxBlockImage.currentIndexChanged.connect(self.__updateImage)
        self.ui.pushButtonSelectFile.clicked.connect(self.__clickedSelectFile)
        self.ui.pushButtonAddVar.clicked.connect(self.__addVar)
        self.ui.pushButtonRemoveVar.clicked.connect(self.__delVar)
        self.ui.pushButtonAddBlockImage.clicked.connect(self.__addImage)
        self.ui.pushButtonRemoveBlockImage.clicked.connect(self.__removeImage)
        self.ui.pushButtonRemoveVar.setEnabled(False)
        self.ui.pushButtonRemoveBlockImage.setEnabled(False)
        self.ui.pushButtonOK.clicked.connect(lambda :self.__buttons(1))
        self.ui.pushButtonCancel.clicked.connect(lambda :self.__buttons(0))
        self.ui.lineEditName.textChanged.connect(lambda :self.__updateImage(self.ui.comboBoxBlockImage.currentIndex()))

    def __clickedSelectFile(self):
        file = QtGui.QFileDialog.getOpenFileName(self, "Open File",
                                                ".","Python Files (*.py)")
        self.ui.lineEditFile.setText(file[0])

    def __updateImage(self,index):
        self.img=listNameBlocks[index]
        img = cv2.imread(listBlock[index],cv2.IMREAD_UNCHANGED)
        archivo, extension = os.path.splitext(listBlock[index])
        blockType, connections = self.__loadConfigBlock(archivo)
        img = generateBlock(img, 34, self.ui.lineEditName.text(), blockType, None,
                             None)
        qImage = toQImage(img)
        self.ui.BlockImage.setPixmap(QtGui.QPixmap(qImage))

    def __loadConfigBlock(self, img):
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

    def __updateBlockType(self, index):
        self.blockType = listTypeBlock[index]
        self.config = listconfig[index]

    def __addVar(self):
        row = self.ui.tableWidgetVars.rowCount()
        self.ui.tableWidgetVars.insertRow(row)
        self.ui.tableWidgetVars.setCellWidget(row,0,QtGui.QLabel("Float"))
        self.ui.tableWidgetVars.setCellWidget(row, 1, QtGui.QLineEdit())
        edit = QtGui.QLineEdit()
        edit.setValidator(QtGui.QDoubleValidator())
        self.ui.tableWidgetVars.setCellWidget(row, 2, edit)
        self.ui.pushButtonRemoveVar.setEnabled(True)

    def __delVar(self):

        self.ui.tableWidgetVars.removeRow(self.ui.tableWidgetVars.currentRow())
        if self.ui.tableWidgetVars.rowCount() == 0:
            self.ui.pushButtonRemoveVar.setEnabled(False)

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
        if len(self.listImg)==0:
            self.ui.pushButtonRemoveBlockImage.setEnabled(False)

    def __buttons(self, ret):
        if ret is 1:
            ret =None
            if self.ui.lineEditName.text() == "":
                msgBox = QtGui.QMessageBox()
                msgBox.setText("Error Name is empty.")
                msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
                msgBox.setDefaultButton(QtGui.QMessageBox.Ok)
                ret = msgBox.exec_()
            elif len(self.listImg) is 0:
                msgBox = QtGui.QMessageBox()
                msgBox.setText("Error Images of block is empty.")
                msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
                msgBox.setDefaultButton(QtGui.QMessageBox.Ok)
                ret = msgBox.exec_()
            elif self.__repitNameVar():
                msgBox = QtGui.QMessageBox()
                msgBox.setText("Error name of vars is repit, name is empty or default value is empty.")
                msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
                msgBox.setDefaultButton(QtGui.QMessageBox.Ok)
                ret = msgBox.exec_()
            if ret is not None:
                return

            text = """
block{\n"""
            text += "\ttype " + self.blockType + "\n"
            text += "\tname " + self.ui.lineEditName.text() + "\n"
            file = self.ui.lineEditFile.text()
            if file == "":
                file = "None"
            text += "\tfile " + file + "\n"
            if self.ui.tableWidgetVars.rowCount() is not 0:
                text += "\tvariables{\n"
                for row in range(0,self.ui.tableWidgetVars.rowCount()):
                    text += "\t\t"+self.ui.tableWidgetVars.cellWidget(row,0).text() + " " + \
                            self.ui.tableWidgetVars.cellWidget(row,1).text() + " " + self.ui.tableWidgetVars.cellWidget(row,2).text() + "\n"
                text += "\t}\n"
            text += "\timg "
            for img in self.listImg:
                text += img + ", "
            text = text[:-2] + "\n}"
            msgBox = QtGui.QMessageBox()
            msgBox.setText("Are you sure you want to add this function?")
            msgBox.setInformativeText(text)
            msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
            msgBox.setDefaultButton(QtGui.QMessageBox.Ok)
            ret = msgBox.exec_()
            if ret == QtGui.QMessageBox.Ok:
                print "escribiendo", self.config
                with open(pathConfig+"/"+self.config, 'a') as file:
                    file.write(text)
            else:
                return

        self.close()

    def __repitNameVar(self):
        varlist=[]
        if self.ui.tableWidgetVars.rowCount() is not 0:
            for row in range(0, self.ui.tableWidgetVars.rowCount()):
                if self.ui.tableWidgetVars.cellWidget(row,1).text() in varlist or self.ui.tableWidgetVars.cellWidget(row,1).text() == ""\
                        or self.ui.tableWidgetVars.cellWidget(row,2).text() == "":
                    return True
                varlist.append(self.ui.tableWidgetVars.cellWidget(row, 1).text())
        return False