from PySide import QtCore, QtGui
import copy

import threading
from math import *
import numpy as np
import cv2
from toQImage import *

TOP = 0
BOTTOM = 1
BOTTOMIN = -1
RIGHT = 3
LEFT = 4

SIMPLEBLOCK = 1
COMPLEXBLOCK = 2

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

def EuclideanDist(p1,p2):
    p = p1 - p2
    return sqrt(pow(p.x(), 2) + pow(p.y(), 2))


class BlockItem(QtGui.QGraphicsPixmapItem):
    def __init__(self,x, y, nameFuntion, file, vars, parent=None, scene=None, connections=None, type = SIMPLEBLOCK):
        self.nameFuntion = nameFuntion
        QtGui.QGraphicsPixmapItem.__init__(self)
        self.cvImg = cv2.imread(file,cv2.IMREAD_UNCHANGED)
        self.cvImg = np.require(self.cvImg, np.uint8, 'C')
        qImage = toQImage(self.cvImg)
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
        self.table = None
        if vars is not None:
            tabVar = QtGui.QTableWidget()
            tabVar.verticalHeader().setVisible(False)
            tabVar.horizontalHeader().setVisible(False)
            tabVar.setColumnCount(2)
            tabVar.setRowCount(len(vars)+1)
            i = 0
            for var in vars:
                tabVar.setCellWidget(i,0,QtGui.QLabel(var[1]))
                widget = None
                if "float" in var[1]:
                    pass
                elif "int" in var[1]:
                    pass
                elif "string" in var[1]:
                    pass
                edit = QtGui.QLineEdit()
                edit.setValidator(QtGui.QDoubleValidator())
                tabVar.setCellWidget(i, 1, edit)
                i+=1

            tabVar.setFixedSize(tabVar.columnWidth(0)*2+2, tabVar.rowHeight(0)*tabVar.rowCount()+2)
            self.table = self.scene.addWidget(tabVar)
            self.table.setZValue(1);
            self.table.setPos(x,y)
            self.scene.setTable(self.table)
            self.table.setVisible(False)

    def delete(self):
        self.scene.removeItem(self)

    def addConnection(self,point,type):
        self.connections.append(connection(point, self, type))

    def generateBlock(self,n,size):
        line = self.cvImg[50:51, 0:149]
        im = np.ones((self.header.shape[0]+self.foot.shape[0]+size-4, 149, 4), dtype=np.uint8)

        im[0:self.header.shape[0],0:149]=self.header
        im[im.shape[0]-self.foot.shape[0]:im.shape[0],0:149] = self.foot
        for i in range(39,im.shape[0]-self.foot.shape[0]):
            im[i:i+line.shape[0],0:149] = copy.copy(line)


        return im

    def updateConnections(self):
        if self.__type is COMPLEXBLOCK:
            nSubBlock, size  = self.getNumSub()
            if size is 0:
                size = 34
            im = self.generateBlock(nSubBlock,size)
            self.cvImg = np.require(im, np.uint8, 'C')
            qImage = toQImage(self.cvImg)
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
            if self.table is not None:
                self.table.setVisible(False)
        if event.button() is QtCore.Qt.MouseButton.RightButton:
            self.scene.itemSelected(None)
            if self.table is not None:
                self.table.setVisible(True)
                self.setZValue(-1)
                self.table.setZValue(1);
                self.table.setPos(event.scenePos())
                self.scene.setTable(self.table)

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
        size += self.cvImg.shape[0]-5
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

    def getInstructions(self,inst=[]):

        for c in self.connections:
            if c.getType() is RIGHT:
                if c.getItem() is not None:
                    if len(inst) is 0:
                        inst.append(c.getItem().getInstructions())
                    else:
                        inst.append(c.getItem().getInstructions())
            elif c.getType() is BOTTOMIN:
                if c.getItem() is not None:
                    inst.append(c.getItem().getInstructions(inst))
            elif c.getType() is BOTTOM:
                if c.getItem() is not None:
                    inst.append(c.getItem().getInstructions(inst))

        inst.append(self.nameFuntion)
        return inst