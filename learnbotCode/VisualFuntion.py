from PySide import QtCore, QtGui
import copy

import threading
from math import *

TOP = 0
BOTTOM = 1
BOTTOMIN = -1
RIGHT = 3
LEFT = 4



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
    def getPoint(self):
        return self.__point + self.__parent.pos()
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
    def __init__(self,x, y, nameFuntion, file, vars, parent=None, scene=None, connections=None):
        self.nameFuntion = nameFuntion
        QtGui.QGraphicsPixmapItem.__init__(self)
        image = QtGui.QImage(file)
        self.img =QtGui.QPixmap(image)

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


        self.table = None
        if vars is not None:
            tabVar = QtGui.QTableWidget()
            tabVar.verticalHeader().setVisible(False)
            tabVar.horizontalHeader().setVisible(False)
            tabVar.setColumnCount(2)
            tabVar.setRowCount(4)
            tabVar.setFixedSize(tabVar.columnWidth(0)*2+2, tabVar.rowHeight(0)*4+2)
            self.table = self.scene.addWidget(tabVar)
            self.table.setZValue(1);
            self.table.setPos(x,y)
            self.scene.setTable(self.table)
            self.table.setVisible(False)


        self.connections = []
        self.posmouseinItem = None

    def addConnection(self,point,type):
        self.connections.append(connection(point, self, type))

    def updateConnections(self):
        for c in self.connections:
            if c.getConnect() is not None:
                if EuclideanDist(c.getPoint(),c.getConnect().getPoint()) != 5:
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
            elif c.getType() in (BOTTOM,BOTTOMIN,RIGHT):
                if c.getItem() is not None:
                    c.getItem().moveToPos(self.pos() + QtCore.QPointF(0, self.img.height()-5), connect)

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