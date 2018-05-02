from PySide import QtCore, QtGui
from VisualBlock import *
from math import *
import sys
from blocksConfig import pathImgBlocks


class MyScene(QtGui.QGraphicsScene):

    def __init__(self,view):
        self.shouldSave = False
        self.view = view
        QtGui.QGraphicsScene.__init__(self)
        self.setBackgroundBrush(QtCore.Qt.gray)
        self.idItemS = None
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(5)
        self.table = None
        self.posibleConnect = []
        self.imgPosibleConnectH = QtGui.QGraphicsPixmapItem(pathImgBlocks+"/ConnectH.png")
        super(MyScene, self).addItem(self.imgPosibleConnectH)
        self.imgPosibleConnectH.setVisible(False)
        self.imgPosibleConnectV = QtGui.QGraphicsPixmapItem(pathImgBlocks+"/ConnectV.png")
        super(MyScene, self).addItem(self.imgPosibleConnectV)
        self.imgPosibleConnectV.setVisible(False)
        self.dicBlockItem = {}
        self.dictVisualItem = {}
        self.nextIdItem = 0
        self.listNameVars = None

    def setlistNameVars(self,listNameVars):
        self.listNameVars = listNameVars

    def getVisualItem(self,id):
        if id in self.dictVisualItem:
            return self.dictVisualItem[id]
        return None

    def setIdItemSelected(self, id):
        self.idItemS = id

    def getItemSelected(self):
        if self.idItemS is not None:
            return self.dictVisualItem[self.idItemS]
        return None

    def setTable(self,table):
        self.table=table

    def addItem(self, blockItem):
        id = str(self.nextIdItem)
        #poner ide del bloque
        blockItem.setId(id)
        visualItem = VisualBlock(blockItem, self.view, self)
        visualItem.start()
        super(MyScene, self).addItem(visualItem)
        self.dicBlockItem[id] = blockItem
        self.dictVisualItem[id] = visualItem
        self.nextIdItem +=1

    def setBlockDict(self, dict):
        self.clean()
        for id in dict:
            blockItem = dict[id]
            visualItem = VisualBlock(blockItem, self.view, self)
            super(MyScene, self).addItem(visualItem)
            self.dicBlockItem[blockItem.id] = blockItem
            self.dictVisualItem[blockItem.id] = visualItem
            if self.nextIdItem <= int(id):
                self.nextIdItem = int(id)+1

        while self.shouldSave is True:
            self.shouldSave = False
            for id in self.dictVisualItem:
                block = self.dictVisualItem[id]
                block.update()

    def clean(self):
        while len(self.dictVisualItem)>0:
            id = self.dictVisualItem.keys()[0]
            self.dictVisualItem[id].delete()
        self.dictVisualItem={}
        self.dicBlockItem={}

    def startAllblocks(self):
        for id in self.dictVisualItem:
            block = self.dictVisualItem[id]
            block.start()

    def removeItem(self, id):
        visualItem = self.getVisualItem(id)
        super(MyScene, self).removeItem(visualItem)
        del self.dicBlockItem[id]
        del self.dictVisualItem[id]

    def removeByName(self, name):
        for id in self.dicBlockItem:
            visualItem = self.getVisualItem(id)
            if visualItem.parentBlock.name == name:
                visualItem.delete()
                return

    def removeWhenByName(self, name):
        for id in self.dicBlockItem:
            visualItem = self.getVisualItem(id)
            if visualItem.parentBlock.nameControl == name:
                visualItem.delete()
                return

    def removeByNameControl(self, name):
        for id in self.dicBlockItem:
            visualItem = self.getVisualItem(id)
            if visualItem.parentBlock.nameControl == name:
                visualItem.delete()
                return

    def getClosestItem(self):
        min_dist = None
        min_c = None
        min_cItS = None
        if self.idItemS is not None:
            itemS = self.getItemSelected()
            for id in self.dictVisualItem:
                if id is not self.idItemS:
                    item = self.dictVisualItem[id]
                    item.setZValue(-1)
                    for cItS in itemS.connections:
                        if cItS.getType() in (BOTTOM, BOTTOMIN, RIGHT) and cItS.getIdItem() is not None:
                            continue
                        for c in item.connections:
                            if c.getType() in (TOP, LEFT) and c.getIdItem() is not None:
                                continue
                            if abs(c.getType() - cItS.getType()) == 1 and (
                                    cItS.getConnect() is not c or cItS.getConnect() is None):
                                dist = EuclideanDist(cItS.getPosPoint(), c.getPosPoint())
                                if dist < min_dist or min_dist is None:
                                    min_c = c
                                    min_cItS = cItS
                                    min_dist = dist
            itemS.moveToFront()
        if min_dist is not None and min_dist < 30:
            return min_c, min_cItS
        return None, None

    def update(self):
        min_c, min_cItS = self.getClosestItem()
        self.posibleConnect = [min_c, min_cItS]

        if min_c is not None:
            if min_c.getType() is TOP:
                self.imgPosibleConnectH.setPos(min_c.getParent().pos)
                self.imgPosibleConnectH.setVisible(True)
                self.imgPosibleConnectH.setZValue(1)
            elif min_c.getType() is BOTTOM:
                self.imgPosibleConnectH.setPos(min_c.getParent().pos + QtCore.QPointF(0, self.getVisualItem(min_c.getParent().id).img.height() - 5))
                self.imgPosibleConnectH.setVisible(True)
                self.imgPosibleConnectH.setZValue(1)
            elif min_c.getType() is RIGHT:
                self.imgPosibleConnectV.setPos(min_c.getParent().pos + QtCore.QPointF(self.getVisualItem(min_c.getParent().id).img.width() - 5, 0)+QtCore.QPointF(0,5))
                self.imgPosibleConnectV.setVisible(True)
                self.imgPosibleConnectV.setZValue(1)
            elif min_c.getType() is LEFT:
                self.imgPosibleConnectV.setPos(min_c.getParent().pos+QtCore.QPointF(0,5))
                self.imgPosibleConnectV.setVisible(True)
                self.imgPosibleConnectV.setZValue(1)
            elif min_c.getType() is BOTTOMIN:
                self.imgPosibleConnectH.setPos(min_c.getParent().pos + QtCore.QPointF(16,38))
                self.imgPosibleConnectH.setVisible(True)
                self.imgPosibleConnectH.setZValue(1)
                pass


        else:
            self.imgPosibleConnectH.setVisible(False)
            self.imgPosibleConnectV.setVisible(False)

    def EuclideanDist(p1, p2):
        p = p1 - p2
        return sqrt(pow(p.x(), 2) + pow(p.y(), 2))

    def activeShouldSave(self):
        self.shouldSave = True

    def getListInstructions(self):
        list = []
        for id in self.dictVisualItem:
            item = self.getVisualItem(id)
            if item.isBlockDef():
                inst = item.getInstructions()
                list.append(inst)
        return list

    def mouseMoveEvent(self, event):
        itemS = self.getItemSelected()
        if isinstance(itemS, VisualBlock):
            itemS.moveToPos(event.scenePos())

    def mousePressEvent(self, event):
        item = self.itemAt(event.scenePos())
        if self.table is not None and item is not self.table:
            self.table.close()
            self.table = None
        if isinstance(item, VisualBlock):
            item.mousePressEvent(event)

    def mouseDoubleClickEvent(self,event):
        item = self.itemAt(event.scenePos())
        if self.table is not None and item is not self.table:
            self.table.close()
            self.table = None
        if isinstance(item, VisualBlock):
            item.mouseDoubleClickEvent(event)

    def mouseReleaseEvent(self, event):
        itemS = self.getItemSelected()
        self.idItemS = None
        pos = event.scenePos()
        item = self.itemAt(pos)
        if isinstance(item, VisualBlock):
            item.mouseReleaseEvent(event)

        if self.posibleConnect[0] is not None:
            c, cItS = self.posibleConnect
            if c.getIdItem() is not None:
                if c.getType() is TOP:
                    pass
                elif c.getType() in [BOTTOM,BOTTOMIN]:
                    cNext = c.getConnect()
                    cLastIt = self.getVisualItem(cItS.getParent().id).getLastItem()
                    if cLastIt is not None:
                        cLastIt.setItem(cNext.getParent().id)
                        cLastIt.setConnect(cNext)
                        cNext.setItem(cLastIt.getParent().id)
                        cNext.setConnect(cLastIt)
                elif c.getType() is RIGHT:
                    cNext = c.getConnect()
                    cLastIt = self.getVisualItem(cItS.getParent().id).getLastRightItem()
                    if cLastIt is not None:
                        cLastIt.setItem(cNext.getParent().id)
                        cLastIt.setConnect(cNext)
                        cNext.setItem(cLastIt.getParent().id)
                        cNext.setConnect(cLastIt)
            c.setItem(cItS.getParent().id)
            c.setConnect(cItS)
            cItS.setItem(c.getParent().id)
            cItS.setConnect(c)


            if c.getType() is TOP:
                itemS.moveToPos(c.getParent().pos + QtCore.QPointF(0, -itemS.img.height()+5), True)
            elif c.getType() is BOTTOM:
                itemS.moveToPos(c.getParent().pos + QtCore.QPointF(0, self.getVisualItem(c.getParent().id).img.height()-5), True)
            elif c.getType() is RIGHT:
                itemS.moveToPos(c.getParent().pos + QtCore.QPointF(self.getVisualItem(c.getParent().id).img.width()-5, 0), True)
            elif c.getType() is LEFT:
                itemS.moveToPos(c.getParent().pos + QtCore.QPointF(-self.getVisualItem(itemS.id).img.width()+5, 0), True)
            elif c.getType() is BOTTOMIN:
                itemS.moveToPos(c.getParent().pos + QtCore.QPointF(17, 33), True)
