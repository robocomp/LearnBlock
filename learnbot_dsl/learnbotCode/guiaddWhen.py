import os

import guis.addWhen as addWhen
from VisualBlock import *
from blocksConfig import pathBlocks
from blocksConfig.blocks import *
listBlock = []
listNameBlocks = []
import cv2

for base, dirs, files in os.walk(pathBlocks):
    for f in files:
        archivo, extension = os.path.splitext(base + "/" + f)
        if extension == ".png" and "block" in f and "azul" not in f:
            if "block8" in f or "block10" in f:
                listBlock.append(base + "/" + f)
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


class guiAddWhen(QtGui.QDialog):

    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.blockType = None
        self.nameControl = ""
        self.FuntionType = None
        self.img = None
        self.imgName = []
        self.ui = addWhen.Ui_Dialog()
        self.value = None
        self.ui.setupUi(self)
        self.hue = HUE_WHEN
        self.__updateBlockType(0)
        self.__updateImage(0)
        self.isOk = False
        for name in listNameBlocks:
            self.ui.comboBoxBlockImage.addItem(name)
        self.ui.comboBoxBlockImage.currentIndexChanged.connect(self.__updateImage)

        self.ui.pushButtonOK.clicked.connect(lambda: self.__buttons(1))
        self.ui.pushButtonCancel.clicked.connect(lambda: self.__buttons(0))
        self.ui.lineEditName.textChanged.connect(lambda: self.__updateImage(self.ui.comboBoxBlockImage.currentIndex()))
        self.ui.Run_start.stateChanged.connect(self.__changeRunStart)

    def __changeRunStart(self):
        if self.ui.Run_start.isChecked():
            self.ui.lineEditName.setEnabled(False)
            self.ui.comboBoxBlockImage.setCurrentIndex(1)
            self.ui.comboBoxBlockImage.setEnabled(False)
            self.ui.lineEditName.setText("start")
            self.__updateImage(self.ui.comboBoxBlockImage.currentIndex())
        else:
            self.ui.lineEditName.setText("")
            self.ui.lineEditName.setEnabled(True)
            self.ui.comboBoxBlockImage.setEnabled(True)
            self.__updateImage(self.ui.comboBoxBlockImage.currentIndex())
    def __updateImage(self, index):

        self.value = "when"
        self.nameControl = self.ui.lineEditName.text()
        self.img = listNameBlocks[index]
        self.imgName = listBlock[index]
        img = cv2.imread(listBlock[index], cv2.IMREAD_UNCHANGED)
        archivo, extension = os.path.splitext(listBlock[index])
        blockType, connections = self.__loadConfigBlock(archivo)
        img = generateBlock(img, 34, self.value, blockType, None, None, None, self.nameControl)
        r, g, b, a = cv2.split(img)
        rgb = cv2.merge((r, g, b))
        hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
        h, s, v = cv2.split(hsv)
        h = h + self.hue
        s = s + 130
        hsv = cv2.merge((h, s, v))
        im = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
        r, g, b = cv2.split(im)
        img = cv2.merge((r, g, b, a))
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

    def __clear(self):
        self.ui.lineEditFile.clear()
        self.ui.lineEditName.clear()
        self.ui.comboBoxFuntionType.setCurrentIndex(0)
        self.ui.comboBoxBlockImage.setCurrentIndex(0)

    def __buttons(self, ret):
        if ret is 1:
            ret = None
            if self.ui.Run_start.isChecked() is False and self.ui.lineEditName.text() == "start":
                msgBox = QtGui.QMessageBox()
                msgBox.setText(self.trUtf8("Error the name can not be 'start'"))
                msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
                msgBox.setDefaultButton(QtGui.QMessageBox.Ok)
                ret = msgBox.exec_()
            if self.ui.lineEditName.text() == "":
                msgBox = QtGui.QMessageBox()
                msgBox.setText(self.trUtf8("Error Name is empty."))
                msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
                msgBox.setDefaultButton(QtGui.QMessageBox.Ok)
                ret = msgBox.exec_()
            if ret is not None:
                return
        self.isOk = True
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
