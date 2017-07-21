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


def generateBlock2(img, x, name, typeBlock, connections=None, vars=None, type=None):
    im = None
    sizeleter = 12
    varText = ""
    if type is FUNTION:
        varText = "("
        if vars is not None:
            for var in vars:
                varText += var + ","
            varText = varText[:-1] + ")"
        else:
            varText = "()"
    elif type is VARIABLE:
        if vars is not None:
            for var in vars:
                varText =  " poner a " + var
    if typeBlock is COMPLEXBLOCK:
        if vars is None:
            varText = ""
        left = img[0:img.shape[0], 0:73]
        right = img[0:img.shape[0], img.shape[1] - 10:img.shape[1]]
        line = img[0:img.shape[0], 72:73]
        im = np.ones((left.shape[0], left.shape[1] + right.shape[1] + ((len(name)+len(varText)) * sizeleter) - 23, 4), dtype=np.uint8)
        im[0:left.shape[0], 0:left.shape[1]] = copy.copy(left)
        im[0:right.shape[0], im.shape[1] - right.shape[1]:im.shape[1]] = copy.copy(right)
        for i in range(left.shape[1], im.shape[1] - right.shape[1]):
            im[0:line.shape[0], i:i + 1] = copy.copy(line)
        header = copy.copy(im[0:39, 0:149])
        foot = copy.copy(im[69:104, 0:149])
        line = copy.copy(im[50:51, 0:im.shape[1]])
        im = np.ones((header.shape[0] + foot.shape[0] + x - 4, header.shape[1], 4), dtype=np.uint8)
        im[0:header.shape[0], 0:header.shape[1]] = header
        im[im.shape[0] - foot.shape[0]:im.shape[0], 0:foot.shape[1]] = foot
        for i in range(39, im.shape[0] - foot.shape[0]):
            im[i:i + line.shape[0], 0:header.shape[1]] = copy.copy(line)
    else:
        left = img[0:img.shape[0], 0:43]
        right = img[0:img.shape[0], img.shape[1] - 10:img.shape[1]]
        line = img[0:img.shape[0], 43:44]
        im = np.ones((left.shape[0], left.shape[1] + right.shape[1] + ((len(name)+len(varText)) * sizeleter) , 4), dtype=np.uint8)
        im[0:left.shape[0], 0:left.shape[1]] = copy.copy(left)
        im[0:right.shape[0], im.shape[1] - right.shape[1]:im.shape[1]] = copy.copy(right)
        for i in range(left.shape[1], im.shape[1] - right.shape[1]):
            im[0:line.shape[0], i:i + 1] = copy.copy(line)
    cv2.putText(im, name+varText, (10, 27), cv2.FONT_HERSHEY_TRIPLEX, 0.75, (0, 0, 0, 255), 1,25)
    if connections is not None and len(connections) > 0:
        if not isinstance(connections[0],Connection):
            for point, t in connections:
                if t is RIGHT:
                    point.setX(im.shape[1]-5)
        else:
            for c in connections:
                if c.getType() is RIGHT:
                    c.getPoint().setX(im.shape[1] - 5)
    return im


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
        img = generateBlock2(img, 34, self.ui.lineEditName.text(), blockType, None,
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