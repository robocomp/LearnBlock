from __future__ import print_function, absolute_import
import os, cv2

import learnbot_dsl.guis.AddNumberOrString as AddNumberOrString
from learnbot_dsl.learnbotCode.VisualBlock import *
from learnbot_dsl.blocksConfig import pathBlocks
from learnbot_dsl.blocksConfig.blocks import *
listBlock = []
listNameBlocks = []


for base, dirs, files in os.walk(pathBlocks):
    for f in files:
        archivo, extension = os.path.splitext(base + "/" + f)
        if extension == ".png" and "block" in f and "azul" not in f:
            if "block3" in f or "block4" in f:
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


class guiAddNumberOrString(QtWidgets.QDialog):

    def __init__(self, type):
        self.type = type
        QtWidgets.QDialog.__init__(self)
        self.blockType = None
        self.FuntionType = None
        self.img = None
        self.imgName = []
        self.ui = AddNumberOrString.Ui_Dialog()
        self.value = None
        self.hue = HUE_STRING
        if type is 1:
            self.hue = HUE_NUMBER
        self.ui.setupUi(self)
        self.__updateBlockType(0)
        self.__updateImage(0)
        for name in listNameBlocks:
            self.ui.comboBoxBlockImage.addItem(name)
        self.ui.comboBoxBlockImage.currentIndexChanged.connect(self.__updateImage)
        self.ui.pushButtonOK.clicked.connect(lambda: self.__buttons(1))
        self.ui.pushButtonCancel.clicked.connect(lambda: self.__buttons(0))
        self.ui.lineEditName.textChanged.connect(lambda: self.__updateImage(self.ui.comboBoxBlockImage.currentIndex()))
        if type is 1:
            self.ui.lineEditName.setValidator(QtGui.QDoubleValidator())

    def __updateImage(self, index):
        self.value = self.ui.lineEditName.text()
        if self.type is 2:
            self.value = '"' + self.value + '"'
        self.img = listNameBlocks[index]
        self.imgName = listBlock[index]
        img = cv2.imread(listBlock[index], cv2.IMREAD_UNCHANGED)
        archivo, extension = os.path.splitext(listBlock[index])
        blockType, connections = self.__loadConfigBlock(archivo)
        img = generateBlock(img, 34, self.ui.lineEditName.text(), blockType, None,
                            None)
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
            if self.ui.lineEditName.text() == "":
                msgBox = QtWidgets.QMessageBox()
                msgBox.setWindowTitle(self.tr("Warning"))
                msgBox.setIcon(QtWidgets.QMessageBox.Warning)
                msgBox.setText(self.tr("Error Name is empty."))
                msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                msgBox.setDefaultButton(QtWidgets.QMessageBox.Ok)
                ret = msgBox.exec_()
            if ret is not None:
                return
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
