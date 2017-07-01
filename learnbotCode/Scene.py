from PySide import QtCore, QtGui
from VisualFuntion import *
from math import *



class MyScene(QtGui.QGraphicsScene):
    def __init__(self):
        QtGui.QGraphicsScene.__init__(self)
        self.setBackgroundBrush(QtCore.Qt.gray)
        self.listBlocks = []
        self.itemSelec = None
        self.listItem = []
        self.timer = QtCore.QTimer()
        QtCore.QTimer.connect(self.timer, QtCore.SIGNAL("timeout()"), self.update)
        self.timer.start(5)
        self.table = None
        self.posibleConnect = []
        self.imgPosibleConnectH = QtGui.QGraphicsPixmapItem("blocks/ConnectH.png")
        super(MyScene, self).addItem(self.imgPosibleConnectH)
        self.imgPosibleConnectH.setVisible(False)
        self.imgPosibleConnectV = QtGui.QGraphicsPixmapItem("blocks/ConnectV.png")
        super(MyScene, self).addItem(self.imgPosibleConnectV)
        self.imgPosibleConnectV.setVisible(False)

    def itemSelected(self, item):
        self.itemSelec = item

    def getItemSelected(self):
        return self.itemSelec

    def setTable(self,table):
        self.table=table

    def addItem(self, item=None, nameFunction=None, params=None, type=None):
        self.listBlocks.append({"name":nameFunction,"params":params,"type":type})
        self.listItem.append(item)
        super(MyScene, self).addItem(item)

    def removeItem(self,item):
        self.listItem.remove(item)
        super(MyScene, self).removeItem(item)

    def update(self):
        min_c, min_cItS = self.getClosestItem()
        self.posibleConnect = [min_c, min_cItS]

        if min_c is not None:
            if min_c.getType() is TOP:
                self.imgPosibleConnectH.setPos(min_c.getParent().pos())
                self.imgPosibleConnectH.setVisible(True)
                self.imgPosibleConnectH.setZValue(1)
            elif min_c.getType() is BOTTOM:
                self.imgPosibleConnectH.setPos(min_c.getParent().pos() + QtCore.QPointF(0, min_c.getParent().img.height() - 5))
                self.imgPosibleConnectH.setVisible(True)
                self.imgPosibleConnectH.setZValue(1)
            elif min_c.getType() is RIGHT:
                self.imgPosibleConnectV.setPos(min_c.getParent().pos() + QtCore.QPointF(min_c.getParent().img.width() - 5, 0)+QtCore.QPointF(0,5))
                self.imgPosibleConnectV.setVisible(True)
                self.imgPosibleConnectV.setZValue(1)
            elif min_c.getType() is LEFT:
                self.imgPosibleConnectV.setPos(min_c.getParent().pos()+QtCore.QPointF(0,5))
                self.imgPosibleConnectV.setVisible(True)
                self.imgPosibleConnectV.setZValue(1)
            elif min_c.getType() is BOTTOMIN:
                self.imgPosibleConnectH.setPos(min_c.getParent().pos() + QtCore.QPointF(16,38))
                self.imgPosibleConnectH.setVisible(True)
                self.imgPosibleConnectH.setZValue(1)
                pass


        else:
            self.imgPosibleConnectH.setVisible(False)
            self.imgPosibleConnectV.setVisible(False)

    def EuclideanDist(p1, p2):
        p = p1 - p2
        return sqrt(pow(p.x(), 2) + pow(p.y(), 2))

    def getClosestItem(self):
        min_dist = None
        min_c = None
        min_cItS = None
        if self.itemSelec is not None:
            for item in self.listItem:
                if item is not self.itemSelec:
                    item.setZValue(-1)
                    for cItS in self.itemSelec.connections:
                        if cItS.getType() in (BOTTOM, BOTTOMIN,RIGHT) and cItS.getItem() is not None:
                            continue
                        for c in item.connections:
                            if c.getType() in  (TOP,LEFT) and c.getItem() is not None:
                                continue
                            if abs(c.getType()-cItS.getType()) == 1 and (cItS.getConnect() is not c or cItS.getConnect() is None):
                                dist = EuclideanDist(cItS.getPosPoint(), c.getPosPoint())
                                if dist < min_dist or min_dist is None:
                                    min_c = c
                                    min_cItS = cItS
                                    min_dist = dist
            self.itemSelec.moveToFront()
        if min_dist is not None and min_dist<30:
            return min_c, min_cItS
        return None, None

    def getListInstructions(self):
        listPrograms=[]
        for item in self.listItem:
            if "def" in item.getNameFuntion():
                inst = item.getInstructions()
                return inst

    def mouseMoveEvent(self, event):
        if isinstance(self.itemSelec, BlockItem):
            self.itemSelec.moveToPos(event.scenePos())

    def mousePressEvent(self, event):
        item = self.itemAt(event.scenePos())
        if self.table is not None and item is not self.table:
            self.table.close()
            self.table = None
        if isinstance(item, BlockItem):
            item.mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        itemS = self.itemSelec
        self.itemSelec = None
        pos = event.scenePos()
        item = self.itemAt(pos)
        if isinstance(item, BlockItem):
            item.mouseReleaseEvent(event)

        if self.posibleConnect[0] is not None:
            c, cItS = self.posibleConnect

            if c.getItem() is not None:
                if c.getType() is TOP:
                    pass
                elif c.getType() in [BOTTOM,BOTTOMIN]:
                    cNext = c.getConnect()
                    cLastIt = cItS.getParent().getLastItem()
                    cLastIt.setItem(cNext.getParent())
                    cLastIt.setConnect(cNext)
                    cNext.setItem(cLastIt.getParent())
                    cNext.setConnect(cLastIt)
            c.setItem(cItS.getParent())
            c.setConnect(cItS)
            cItS.setItem(c.getParent())
            cItS.setConnect(c)

            if c.getType() is TOP:
                itemS.moveToPos(c.getParent().pos() + QtCore.QPointF(0, -itemS.img.height()+5), True)
            elif c.getType() is BOTTOM:
                itemS.moveToPos(c.getParent().pos() + QtCore.QPointF(0, c.getParent().img.height()-5), True)
            elif c.getType() is RIGHT:
                itemS.moveToPos(c.getParent().pos() + QtCore.QPointF(c.getParent().img.width()-5, 0), True)
            elif c.getType() is LEFT:
                itemS.moveToPos(c.getParent().pos() + QtCore.QPointF(-itemS.img.width()+5, 0), True)
            elif c.getType() is BOTTOMIN:
                itemS.moveToPos(c.getParent().pos() + QtCore.QPointF(17, 33), True)

