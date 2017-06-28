from Scene import *
from VisualFuntion import *
from View import *
import gui,sys
import os
import cv2


def loadfile(file):
    fh = open(file, "r")
    code = fh.read()
    fh.close()
    return code

class MyButtom(QtGui.QPushButton):
    def __init__(self,text,view,scene,imgFile,connections, vars):
        QtGui.QPushButton.__init__(self,text)
        self.clicked.connect(self.clickedButton)
        self.view = view
        self.scene = scene
        self.file = imgFile
        self.connections = connections
        self.vars = vars
    def clickedButton(self):
        item = BlockItem(0, 0, self.text(),self.file, self.vars, self.view, self.scene)
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
        functions = {}
        for base, dirs, files in os.walk('learnbot-dsl/functions'):
            for file in files:
                functions[file.replace(".py", "")] = file, file.replace(".py", ""), loadfile(base + "/" + file)
        del functions["__init__"]

        tableControl = self.ui.tableControl
        tableControl.verticalHeader().setVisible(False)
        tableControl.horizontalHeader().setVisible(False)
        tableControl.setColumnCount(1)
        tableControl.setRowCount(len(functions))

        block = cv2.imread("/home/ivan/gsoc17/learnbotCode/blocks/block5.png", cv2.IMREAD_UNCHANGED)
        try:
            os.mkdir("tmp")
        except:
            pass
        i = 0
        for f in functions:

            button = MyButtom(f,self.view,self.scene,"tmp/" + f + ".png",[(QtCore.QPointF(75, 99), BOTTOM),(QtCore.QPointF(75, 5), TOP)],1)
            tableControl.setCellWidget(i,0,button)
            img = block.copy()
            cv2.putText(img, f, (10, 23), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (0, 0, 0, 255), 1)
            cv2.imwrite("tmp/" + f + ".png", img, (cv2.IMWRITE_PNG_COMPRESSION, 9))
            i+=1

        tableControl.insertRow(tableControl.rowCount())
        button = MyButtom("Init_Program", self.view, self.scene, "initProgram.png",[(QtCore.QPointF(75, 33), BOTTOM)],None)
        tableControl.setCellWidget(i, 0, button)

        self.timer = QtCore.QTimer()
        # QtCore.QTimer.connect(self.timer, QtCore.SIGNAL("timeout()"), self.scene.update())
        self.timer.start(1000)

        r = app.exec_()

        for f in functions:
            os.remove("tmp/" + f + ".png")
        os.rmdir("tmp")
        sys.exit(r)


    def printProgram(self):
        listPrograms = self.scene.getListInstructions()
        for listInst in listPrograms:
            for inst in listInst:
                self.ui.plainTextEdit_2.appendPlainText(inst + "(vars)")
            self.ui.plainTextEdit_2.appendPlainText("\n\n")