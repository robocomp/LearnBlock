from Scene import *
from VisualFuntion import *
from View import *
import gui,sys
import os
import cv2
from parserConfigBlock import *

def loadfile(file):
    fh = open(file, "r")
    code = fh.read()
    fh.close()
    return code

class MyButtom(QtGui.QPushButton):
    def __init__(self,text,view,scene,imgFile,connections, vars, blockType,table,row):
        QtGui.QPushButton.__init__(self)
        im = cv2.imread(imgFile)
        table.setRowHeight(row-1,im.shape[0])
        self.setIcon(QtGui.QIcon(imgFile))
        self.setIconSize(QtCore.QSize(100,100))
        self.setFixedSize(QtCore.QSize(150, im.shape[0]))
        self.clicked.connect(self.clickedButton)
        self.view = view
        self.scene = scene
        self.file = imgFile
        self.connections = connections
        self.vars = vars
        self.blockType = blockType
    def clickedButton(self):
        item = BlockItem(0, 0, self.text(),self.file, self.vars, self.view, self.scene,None,self.blockType)
        for point, type in self.connections:
            item.addConnection(point, type)
        self.scene.addItem(item)

class LearnBlock:
    def __init__(self):
        app = QtGui.QApplication(sys.argv)
        Dialog = QtGui.QMainWindow()
        self.ui = gui.Ui_MainWindow()
        self.ui.setupUi(Dialog)
        Dialog.showMaximized()
        self.ui.pushButton.clicked.connect(self.printProgram)

        self.view = MyView(self.ui.frame)
        self.view.setObjectName("view")
        self.ui.verticalLayout_3.addWidget(self.view)
        self.scene = MyScene()
        self.view.setScene(self.scene)
        self.view.show()
        tableControl = self.ui.tableControl
        tableControl.verticalHeader().setVisible(False)
        tableControl.horizontalHeader().setVisible(False)
        tableControl.setColumnCount(1)
        tableControl.setRowCount(0)
        #READ FUNTIONS
        functions = parserConfigBlock("config")

        listTmpFiles = []
        try:
            os.mkdir("tmp")
        except:
            pass
        i = 0
        for f in functions:
            for img in f[1]["img"]:
                block = cv2.imread(img, cv2.IMREAD_UNCHANGED)
                fileTmpImg = "tmp/" + f[1]["name"][0] + str(i) +".png"
                listTmpFiles.append(fileTmpImg)
                cv2.putText(block, f[1]["name"][0], (10, 23), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (0, 0, 0, 255), 1)
                cv2.imwrite(fileTmpImg, block, (cv2.IMWRITE_PNG_COMPRESSION, 9))
                fh = open(img.replace(".png",""), "r")
                text = fh.readlines()
                fh.close()
                connections = []
                for line in text:
                    line = line.replace("\n","")
                    line = line.replace(" ", "")
                    c = line.split(",")
                    type = None
                    if "TOP" in c[2] :
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
                variable = None
                if "variables" in f[1]:
                    variable = f[1]["variables"]
                blockType =  f[1]["blocktype"][0]
                if "simple" in blockType:
                    blockType = SIMPLEBLOCK
                elif "complex" in blockType:
                    blockType = COMPLEXBLOCK

                tableControl.insertRow(tableControl.rowCount())
                button = MyButtom(f[1]["name"][0], self.view, self.scene, fileTmpImg, connections, variable, blockType,tableControl,tableControl.rowCount())
                tableControl.setCellWidget(i, 0, button)
                i+=1

            #[(QtCore.QPointF(75, 33), BOTTOM), (QtCore.QPointF(75, 5), TOP)]
            """
            button = MyButtom(f,self.view,self.scene,"tmp/" + f + ".png",[(QtCore.QPointF(5, 15), LEFT),(QtCore.QPointF(94, 15), RIGHT)],1)
            tableControl.setCellWidget(i,0,button)
            img = block.copy()
            cv2.putText(img, f, (10, 23), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (0, 0, 0, 255), 1)
            cv2.imwrite("tmp/" + f + ".png", img, (cv2.IMWRITE_PNG_COMPRESSION, 9))
            """

        tableControl.insertRow(tableControl.rowCount())
        button = MyButtom("Init_Program", self.view, self.scene, "initProgram.png",[(QtCore.QPointF(75, 33), BOTTOM)],None,SIMPLEBLOCK,tableControl,tableControl.rowCount())
        tableControl.setCellWidget(i, 0, button)

        self.timer = QtCore.QTimer()
        # QtCore.QTimer.connect(self.timer, QtCore.SIGNAL("timeout()"), self.scene.update())
        self.timer.start(1000)

        r = app.exec_()

        for f in listTmpFiles:
            os.remove(f)
        os.rmdir("tmp")
        sys.exit(r)


    def printProgram(self):
        listPrograms = self.scene.getListInstructions()
        for listInst in listPrograms:
            for inst in listInst:
                self.ui.plainTextEdit_2.appendPlainText(inst + "(vars)")
            self.ui.plainTextEdit_2.appendPlainText("\n\n")