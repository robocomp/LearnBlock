import guis.createBlock as createBlock
from VisualFuntion import *

listBlock = ["blocks/block0.png",
             "blocks/block1.png",
             "blocks/block2.png",
             "blocks/block3.png",
             "blocks/block4.png",
             "blocks/block5.png",
             "blocks/block6.png",
             "blocks/block7.png",
             "blocks/block8.png",
             "blocks/block9.png"]

listTypeFuntion = [CONTROL,FUNTION,OPERATOR]
listTypeBlock = ["control",
                 "motor",
                 "perceptive",
                 "propioperceptive",
                 "operator"]


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
        self.__updateFuntionType(0)
        self.__updateImage(0)
        self.ui.comboBoxBlockImage.currentIndexChanged.connect(self.__updateImage)
        self.ui.comboBoxFuntionType.currentIndexChanged.connect(self.__updateFuntionType)
        self.ui.pushButtonSelectFile.clicked.connect(self.__clickedSelectFile)
        self.ui.pushButtonAddVar.clicked.connect(self.__addVar)
        self.ui.pushButtonRemoveVar.clicked.connect(self.__delVar)
        self.ui.pushButtonAddBlockImage.clicked.connect(self.__addImage)
        self.ui.pushButtonRemoveBlockImage.clicked.connect(self.__removeImage)


        self.ui.comboBoxFuntionType.currentIndexChanged.connect(self.__updateBlockType)

    def __clickedSelectFile(self):
        file = QtGui.QFileDialog.getOpenFileName(self, "Open File",
                                                "/home","Python Files (*.py)")
        self.ui.lineEditFile.setText(file[0])

    def __updateImage(self,index):
        self.img=listBlock[index]
        self.ui.BlockImage.setPixmap(QtGui.QPixmap(listBlock[index]))

    def __updateFuntionType(self,index):
        self.FuntionType = listTypeFuntion[index]

    def __updateBlockType(self, index):
        self.blockType = listTypeBlock[index]

    def __addVar(self):
        row = self.ui.tableWidgetVars.rowCount()
        self.ui.tableWidgetVars.insertRow(row)
        self.ui.tableWidgetVars.setCellWidget(row,0,QtGui.QLabel("Float"))
        self.ui.tableWidgetVars.setCellWidget(row, 1, QtGui.QLineEdit())
        edit = QtGui.QLineEdit()
        edit.setValidator(QtGui.QDoubleValidator())
        self.ui.tableWidgetVars.setCellWidget(row, 2, edit)

    def __delVar(self):
        self.ui.tableWidgetVars.removeRow(self.ui.tableWidgetVars.currentRow())

    def __clear(self):
        self.ui.lineEditFile.clear()
        self.ui.lineEditName.clear()
        self.ui.comboBoxFuntionType.setCurrentIndex(0)
        self.ui.comboBoxBlockImage.setCurrentIndex(0)

    def __addImage(self):
        if self.img not in self.listImg:
            self.ui.listWidgetBlockImage.addItem(QtGui.QListWidgetItem(self.img))
            self.listImg.append(self.img)

    def __removeImage(self):
        index = self.ui.listWidgetBlockImage.currentRow()
        self.listImg.pop(index)
        self.ui.listWidgetBlockImage.takeItem(index)