from PySide import QtCore, QtGui
import copy

import threading
from math import *
import numpy as np
import cv2
from toQImage import *
import var

TOP = 0
BOTTOM = 1
BOTTOMIN = -1
RIGHT = 3
LEFT = 4

SIMPLEBLOCK = 1
COMPLEXBLOCK = 2

class VarGui(QtGui.QDialog,var.Ui_Dialog):
    def init(self):
        self.setupUi(self)

    def getTable(self):
        return self.table

    def setSlotToDeleteButton(self,fun):
        self.deleteButton.clicked.connect(fun)
        self.okButton.clicked.connect(self.close)

class connection:
    def __init__(self, point, parent, type,):
        self.__parent = parent
        self.__connect = None
        self.__point = point
        self.__item = None
        self.__type = type
    def setType(self,type):
        self.__type = type
    def getType(self):
        return self.__type
    def setItem(self,item):
        self.__item = item
    def getItem(self):
        return self.__item
    def setPoint(self,point):
        self.__point = point
    def getPosPoint(self):
        return self.__point + self.__parent.pos()
    def getPoint(self):
        return self.__point
    def getConnect(self):
        return self.__connect
    def setConnect(self,connect):
        self.__connect=connect
    def setParent(self,parent):
        self.__parent = parent
    def getParent(self):
        return self.__parent
    def __del__(self):
        del self.__parent
        del self.__connect
        del self.__point
        del self.__item
        del self.__type

def EuclideanDist(p1,p2):
    p = p1 - p2
    return sqrt(pow(p.x(), 2) + pow(p.y(), 2))

def generateBlock2(img, x, name, type, connections=None):
    left = img[0:img.shape[0], 0:73]
    right = img[0:img.shape[0], img.shape[1] - 10:img.shape[1]]
    line = img[0:img.shape[0], 72:73]
    im = np.ones((left.shape[0], left.shape[1] + right.shape[1] + (len(name) * 8) - 23, 4), dtype=np.uint8)
    im[0:left.shape[0], 0:left.shape[1]] = copy.copy(left)
    im[0:right.shape[0], im.shape[1] - right.shape[1]:im.shape[1]] = copy.copy(right)
    for i in range(left.shape[1], im.shape[1] - right.shape[1]):
        im[0:line.shape[0], i:i + 1] = copy.copy(line)
    if type is COMPLEXBLOCK:
        header = copy.copy(im[0:39, 0:149])
        foot = copy.copy(im[69:104, 0:149])
        line = copy.copy(im[50:51, 0:im.shape[1]])
        im = np.ones((header.shape[0] + foot.shape[0] + x - 4, header.shape[1], 4), dtype=np.uint8)
        im[0:header.shape[0], 0:header.shape[1]] = header
        im[im.shape[0] - foot.shape[0]:im.shape[0], 0:foot.shape[1]] = foot
        for i in range(39, im.shape[0] - foot.shape[0]):
            im[i:i + line.shape[0], 0:header.shape[1]] = copy.copy(line)

    cv2.putText(im, name, (10, 23), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (0, 0, 0, 255), 1)
    if connections is not None:
        for point, type in connections:
            if type is RIGHT:
                point.setX(im.shape[1]-5)
    return im

class BlockItem(QtGui.QGraphicsPixmapItem):
    def __init__(self,x, y, nameFuntion, file, vars, parent=None, scene=None, connections=None, type = SIMPLEBLOCK):
        self.__nameFuntion = nameFuntion
        QtGui.QGraphicsPixmapItem.__init__(self)
        self.cvImg = cv2.imread(file,cv2.IMREAD_UNCHANGED)
        self.cvImg = np.require(self.cvImg, np.uint8, 'C')
        img = generateBlock2(self.cvImg,34,nameFuntion,type)
        qImage = toQImage(img)
        try:
            self.header = copy.copy(self.cvImg[0:39,0:149])
            self.foot = copy.copy(self.cvImg[69:104,0:149])
        except:
            pass

        #image = QtGui.QImage(file)
        self.img =QtGui.QPixmap(qImage)
        self.__type = type
        self.setFlags(QtGui.QGraphicsItem.ItemIsMovable)
        self.setZValue(1)
        self.setPos(x,y)
        self.setPixmap(self.img)

        self.scene = scene
        self.timer = QtCore.QTimer()
        QtCore.QTimer.connect(self.timer, QtCore.SIGNAL("timeout()"), self.update)
        self.timer.start(5)
        self.timer2 = QtCore.QTimer()
        QtCore.QTimer.connect(self.timer2, QtCore.SIGNAL("timeout()"), self.updateConnections)
        self.timer2.start(5)
        self.connections = []
        self.posmouseinItem = None
        self.DialogVar = None
        if vars is None:
            vars=[]
        self.DialogVar = VarGui()
        self.DialogVar.init()
        self.DialogVar.setSlotToDeleteButton(self.delete)
        self.tabVar = self.DialogVar.getTable()
        self.tabVar.verticalHeader().setVisible(False)
        self.tabVar.horizontalHeader().setVisible(False)
        self.tabVar.setColumnCount(2)
        self.tabVar.setRowCount(len(vars))
        i = 0
        for var in vars:
            self.tabVar.setCellWidget(i,0,QtGui.QLabel(var[1]))
            widget = None
            if "float" in var[1]:
                pass
            elif "int" in var[1]:
                pass
            elif "string" in var[1]:
                pass
            edit = QtGui.QLineEdit()
            edit.setValidator(QtGui.QDoubleValidator())
            self.tabVar.setCellWidget(i, 1, edit)
            i+=1
        """
        self.tabVar.setFixedSize(self.tabVar.columnWidth(0)*2+2, self.tabVar.rowHeight(0)*self.tabVar.rowCount()+2)
        self.table = self.scene.addWidget(self.tabVar)
        self.table.setZValue(1);
        self.table.setPos(x,y)
        self.scene.setTable(self.table)
        self.table.setVisible(False)
        """


    def getNameFuntion(self):
        return self.__nameFuntion



    def delete(self):
        for c in self.connections:
            if c.getItem() is not None:
                if c.getType() in [BOTTOM,BOTTOMIN,RIGHT]:
                    c.getItem().delete()
                else:
                    c.getConnect().setConnect(None)
                    c.getConnect().setItem(None)
        self.DialogVar.close()
        self.scene.removeItem(self)
        del self.__nameFuntion
        del self.connections
        del self.cvImg
        del self.img
        del self.foot
        del self.header
        del self.timer
        del self.timer2
        del self.DialogVar
        del self


    def addConnection(self,point,type):
        self.connections.append(connection(point, self, type))

    def updateConnections(self):
        if self.__type is COMPLEXBLOCK:
            nSubBlock, size  = self.getNumSub()
            if size is 0:
                size = 34
            im = generateBlock2(self.cvImg,size,self.__nameFuntion, self.__type)
            qImage = toQImage(im)
            self.img = QtGui.QPixmap(qImage)
            self.setPixmap(self.img)
            for c in self.connections:
                if c.getType() is BOTTOM:
                    c.setPoint(QtCore.QPointF(c.getPoint().x(),im.shape[0] - 5))
                    if c.getItem() is not None:
                        c.getItem().moveToPos(self.pos() + QtCore.QPointF(0,self.img.height()-5))

        for c in self.connections:
            if c.getConnect() is not None:
                if EuclideanDist(c.getPosPoint(), c.getConnect().getPosPoint()) != 5:
                    c.getConnect().setItem(None)
                    c.getConnect().setConnect(None)
                    c.setItem(None)
                    c.setConnect(None)

    def moveToPos(self, pos, connect=False):
        if connect is False and self.posmouseinItem is not None:
            self.setPos(pos - self.posmouseinItem)
        else:
            self.setPos(pos)
        for c in self.connections:
            if c.getType() in (TOP,LEFT) and self is self.scene.getItemSelected() and connect is not True:
                if c.getItem() is not None:
                    c.getConnect().setItem(None)
                    c.getConnect().setConnect(None)
                    c.setItem(None)
                    c.setConnect(None)
            elif c.getType() is BOTTOM:
                if c.getItem() is not None:
                    c.getItem().moveToPos(self.pos() + QtCore.QPointF(0, self.img.height()-5), connect)
            elif c.getType() is BOTTOMIN:
                if c.getItem() is not None:
                    c.getItem().moveToPos(self.pos() + QtCore.QPointF(17, 33), connect)
            elif c.getType() is RIGHT:
                if c.getItem() is not None:
                    c.getItem().moveToPos(self.pos() + QtCore.QPointF(self.img.width() - 5, 0), connect)

    def getLastItem(self):
        for c in self.connections:
            if c.getType() is BOTTOM:
                if c.getConnect() is None:
                    return c
                else:
                    return c.getItem().getLastItem()

    def moveToFront(self):
        self.setZValue(1)
        for c in self.connections:
            if c.getType() is BOTTOM and c.getConnect() is not None:
                c.getItem().moveToFront()
                break

    def update(self):
        if(self.isUnderMouse() and self.scene.getItemSelected() is not None and self is not self.scene.getItemSelected()):
            pass
            #print "reescalar"

    def mouseMoveEvent(self,event):
        self.setPos(event.scenePos()-self.posmouseinItem)

    def mousePressEvent(self, event):
        if event.button() is QtCore.Qt.MouseButton.LeftButton:
            self.posmouseinItem = event.scenePos()-self.pos()
            self.scene.itemSelected(self)
            if self.DialogVar is not None:
                self.DialogVar.close()
        if event.button() is QtCore.Qt.MouseButton.RightButton:
            self.scene.itemSelected(None)
            if self.DialogVar is not None:
                self.DialogVar.open()
                self.scene.setTable(self.DialogVar)
                """
                self.setZValue(-1)
                self.table.setZValue(1);
                self.table.setPos(event.scenePos())
                self.scene.setTable(self.table)
                """
    def mouseReleaseEvent(self,event):
        if event.button() is QtCore.Qt.MouseButton.LeftButton:
            self.posmouseinItem = None
            self.scene.itemSelected(None)
        if event.button() is QtCore.Qt.MouseButton.RightButton:
            self.posmouseinItem = None
            self.scene.itemSelected(None)
            pass

    def getItemBottomConnect(self):
        for c in self.connections:
            if c.getType() is BOTTOM:
                return c.getItem()

    def getItemTopConnect(self):
        for c in self.connections:
            if c.getType() is TOP:
                return c.getItem()

    def getNumSubBottom(self,n=0,size=0):
        size += self.img.height()-5
        for c in self.connections:
            if c.getType() is BOTTOM:
                if c.getConnect() is None:
                    return n+1,size+1
                else:
                    return c.getItem().getNumSubBottom(n + 1,size)

    def getNumSub(self, n=0):
        for c in self.connections:
            if c.getType() is BOTTOMIN:
                if c.getConnect() is not None:
                    return c.getItem().getNumSubBottom()
                else:
                    return 0,0
        return 0,0

    def getInstructionsRIGHT(self,inst=[]):
        for c in self.connections:
            if c.getType() is RIGHT and c.getItem() is not None:
                inst=c.getItem().getInstructions()
        if len(inst) is 0:
            return None
        return inst
    def getInstructionsBOTTOM(self,inst=[]):
        for c in self.connections:
            if c.getType() is BOTTOM and c.getItem() is not None:
                inst=c.getItem().getInstructions()
        if len(inst) is 0:
            return None
        return inst
    def getInstructionsBOTTOMIN(self,inst=[]):
        for c in self.connections:
            if c.getType() is BOTTOMIN and c.getItem() is not None:
                inst = c.getItem().getInstructions()
        if len(inst) is 0:
            return None
        return inst

    def getInstructions(self,inst=[]):
        instRight = self.getInstructionsRIGHT()
        instBottom = self.getInstructionsBOTTOM()
        instBottomIn = self.getInstructionsBOTTOMIN()
        dic = {}
        #if instRight is not None:
        dic["RIGHT"]=instRight
        #if instBottom is not None:
        dic["BOTTOM"]=instBottom
        #if instBottomIn is not None:
        dic["BOTTOMIN"]=instBottomIn
        vars = []
        for cell in range(0,self.tabVar.rowCount()):
            #if self.tabVar.cellWidget(cell,1) is not None:
            vars.append(self.tabVar.cellWidget(cell,1).text())
        if len(vars) is 0:
            vars = None
        dic["VARIABLES"]=vars
        #inst.insert(0,[self.getNameFuntion(),dic])
        return self.getNameFuntion(),dic