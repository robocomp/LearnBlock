from Scene import *
from VisualFuntion import *
from View import *
import gui,sys,os,cv2
from parserConfigBlock import *

def loadfile(file):
    fh = open(file, "r")
    code = fh.read()
    fh.close()
    return code


class MyButtom(QtGui.QPushButton):
    def __init__(self,text,view,scene,imgFile,connections, vars, blockType,table,row):
        self.__text=text
        self.tmpFile = "tmp/"+text+str(row)+".png"
        QtGui.QPushButton.__init__(self)
        im = cv2.imread(imgFile,cv2.IMREAD_UNCHANGED)
        table.setRowHeight(row-1,im.shape[0])
        img = generateBlock2(im,34,text,blockType,connections)
        cv2.imwrite(self.tmpFile, img, (cv2.IMWRITE_PNG_COMPRESSION, 9))
        self.setIcon(QtGui.QIcon(self.tmpFile))
        self.setIconSize(QtCore.QSize(100,100))
        self.setFixedSize(QtCore.QSize(150, im.shape[0]))
        self.clicked.connect(self.clickedButton)
        self.__view = view
        self.__scene = scene
        self.__file = imgFile
        self.__connections = connections
        self.__vars = vars
        self.__blockType = blockType
    def removeTmpFile(self):
        os.remove(self.tmpFile)
    def clickedButton(self):
        item = BlockItem(0, 0, self.__text, self.__file, self.__vars, self.__view, self.__scene, None, self.__blockType)
        for point, type in self.__connections:
            item.addConnection(point, type)
        self.__scene.addItem(item)

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

        listButtons = []
        try:
            os.mkdir("tmp")
        except:
            pass
        i = 0
        for f in functions:
            for img in f[1]["img"]:
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
                button = MyButtom(f[1]["name"][0], self.view, self.scene, img, connections, variable, blockType,tableControl,tableControl.rowCount())
                listButtons.append(button)
                tableControl.setCellWidget(i, 0, button)
                i+=1

        self.timer = QtCore.QTimer()
        self.timer.start(1000)

        r = app.exec_()

        for b in listButtons:
            b.removeTmpFile()
        os.rmdir("tmp")
        sys.exit(r)

    def printProgram(self):
        inst = self.scene.getListInstructions()
        self.ui.plainTextEdit_2.clear()
        self.ui.plainTextEdit_2.appendPlainText(self.printInst(inst))

    def printInst(self,inst,ntab=0):
        text = inst[0]
        if inst[1]["VARIABLES"] is not None:
            text += "("
            for var in inst[1]["VARIABLES"]:
                text += var+","
            text = text[0:-1]+")"

        if inst[1]["RIGHT"] is not None:
            text += " " + self.printInst(inst[1]["RIGHT"])
        if inst[1]["BOTTOMIN"] is not None:
            ntab+=1
            text += "\n"+"\t"*ntab + self.printInst(inst[1]["BOTTOMIN"],ntab)
        if inst[1]["BOTTOM"] is not None:
            ntab-=1
            text += "\n"+"\t"*ntab + self.printInst(inst[1]["BOTTOM"],ntab)
        return text
