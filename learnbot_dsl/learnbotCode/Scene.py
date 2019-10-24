from __future__ import print_function, absolute_import
from math import *

from learnbot_dsl.learnbotCode.VisualBlock import *
from learnbot_dsl.blocksConfig import pathImgBlocks

class MyScene(QtWidgets.QGraphicsScene):

    def __init__(self, parent, view):
        self.parent = parent
        self.shouldSave = False
        self.view = view
        QtWidgets.QGraphicsScene.__init__(self, self.parent)
        self.setBackgroundBrush(QtCore.Qt.gray)
        self.idItemS = None
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(5)
        self.table = None
        self.posibleConnect = []
        self.imgPosibleConnectH = QtWidgets.QGraphicsPixmapItem(os.path.join(pathImgBlocks, "ConnectH.png"))
        super(MyScene, self).addItem(self.imgPosibleConnectH)
        self.imgPosibleConnectH.setVisible(False)
        self.imgPosibleConnectV = QtWidgets.QGraphicsPixmapItem(os.path.join(pathImgBlocks, "ConnectV.png"))
        super(MyScene, self).addItem(self.imgPosibleConnectV)
        self.imgPosibleConnectV.setVisible(False)
        self.dicBlockItem = {}
        self.dictVisualItem = {}
        self.nextIdItem = 0
        self.listNameVars = []
        self.lastItemSelect = None

    def duplicateBlock(self):
        if self.lastItemSelect is not None:
            self.lastItemSelect.on_clicked_menu_duplicate()

    def exportBlock(self):
        if self.lastItemSelect is not None:
            self.lastItemSelect.on_clicked_menu_export_block()

    def deleteBlock(self):
        if self.lastItemSelect is not None:
            self.lastItemSelect.on_clicked_menu_delete()
            self.lastItemSelect = None

    def editBlock(self):
        if self.lastItemSelect is not None:
            self.lastItemSelect.on_clicked_menu_edit()

    def setlistNameVars(self, listNameVars):
        self.listNameVars = listNameVars

    def getVisualItem(self, id):
        if id in self.dictVisualItem:
            return self.dictVisualItem[id]
        return None

    def setIdItemSelected(self, id):
        self.idItemS = id

    def getItemSelected(self):
        if self.idItemS is not None:
            if self.idItemS in self.dictVisualItem:
                return self.dictVisualItem[self.idItemS]
            else:
                self.idItemS = None
        return None

    def setTable(self, table):
        self.table = table

    def addItem(self, blockItem, shouldstart = True, saveTmp=True):
        id = str(self.nextIdItem)
        # poner ide del bloque
        blockItem.setId(id)
        visualItem = VisualBlock(blockItem, self.view, self)
        if shouldstart:
            visualItem.start()
        visualItem.activeUpdateConections()
        super(MyScene, self).addItem(visualItem)
        pos = self.view.mapToScene(self.view.viewport().rect().center())
        visualItem.setPos(pos)
        self.dicBlockItem[id] = blockItem
        self.dictVisualItem[id] = visualItem
        self.nextIdItem += 1
        if saveTmp:
            self.parent.savetmpProject()

    def setBlockDict(self, dict):
        self.clean()
        for id in dict:
            blockItem = dict[id]
            visualItem = VisualBlock(blockItem, self.view, self)
            super(MyScene, self).addItem(visualItem)
            self.dicBlockItem[blockItem.id] = blockItem
            self.dictVisualItem[blockItem.id] = visualItem
            if self.nextIdItem <= int(id):
                self.nextIdItem = int(id) + 1

        while self.shouldSave is True:
            self.shouldSave = False
            for id in self.dictVisualItem:
                block = self.dictVisualItem[id]
                block.update()
        for id in self.dictVisualItem:
            block = self.dictVisualItem[id]
            block.activeUpdateConections()

    def clean(self):
        while len(self.dictVisualItem) > 0:
            id = list(self.dictVisualItem.keys())[0]
            self.dictVisualItem[id].delete()
        self.dictVisualItem = {}
        self.dicBlockItem = {}
        self.view.viewport().update()

    def startAllblocks(self):
        for id in self.dictVisualItem:
            block = self.dictVisualItem[id]
            block.start()

    def stopAllblocks(self):
        for id in self.dictVisualItem:
            block = self.dictVisualItem[id]
            block.stop()

    def removeItem(self, id, savetmp=True):
        visualItem = self.getVisualItem(id)
        super(MyScene, self).removeItem(visualItem)
        del self.dicBlockItem[id]
        del self.dictVisualItem[id]
        if savetmp:
            self.parent.savetmpProject()

    def removeByName(self, name, saveTmp=True):
        for visualItem in [self.getVisualItem(id) for id in self.dicBlockItem if self.getVisualItem(id).parentBlock.name == name]:
            visualItem.delete(saveTmp)
            return

    def removeWhenByName(self, name):
        for visualItem in [self.getVisualItem(id) for id in self.dicBlockItem if
                           self.getVisualItem(id).parentBlock.name == name]:
            visualItem.delete()
            return

    def removeByNameControl(self, name):
        for visualItem in [self.getVisualItem(id) for id in self.dicBlockItem if self.getVisualItem(id).parentBlock.nameControl == name]:
            visualItem.delete()
            return

    def getClosestItem(self):
        min_dist = None
        min_c = None
        min_cItS = None
        if self.idItemS is not None:
            itemS = self.getItemSelected()
            for item in [self.dictVisualItem[id] for id in self.dictVisualItem if id is not self.idItemS and self.dictVisualItem[id].isEnabled()]:
                item.setZValue(-1)
                for cItS in [c for c in itemS.connections if not (c.getType() in (BOTTOM, BOTTOMIN, RIGHT) and c.getIdItem() is not None)]:
                    for c in [conn for conn in item.connections if not (conn.getType() in (TOP, LEFT) and conn.getIdItem() is not None)]:
                        if abs(c.getType() - cItS.getType()) == 1 and (cItS.getConnect() is not c or cItS.getConnect() is None):

                            dist = EuclideanDist(cItS.getPosPoint(), c.getPosPoint())
                            if min_dist is None or dist < min_dist :
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
                self.imgPosibleConnectH.setPos(min_c.getParent().pos + QtCore.QPointF(0, self.getVisualItem(
                    min_c.getParent().id).img.height() - 5))
                self.imgPosibleConnectH.setVisible(True)
                self.imgPosibleConnectH.setZValue(1)
            elif min_c.getType() is RIGHT:
                self.imgPosibleConnectV.setPos(
                    min_c.getParent().pos + QtCore.QPointF(self.getVisualItem(min_c.getParent().id).img.width() - 5,
                                                           0) + QtCore.QPointF(0, 5))
                self.imgPosibleConnectV.setVisible(True)
                self.imgPosibleConnectV.setZValue(1)
            elif min_c.getType() is LEFT:
                self.imgPosibleConnectV.setPos(min_c.getParent().pos + QtCore.QPointF(0, 5))
                self.imgPosibleConnectV.setVisible(True)
                self.imgPosibleConnectV.setZValue(1)
            elif min_c.getType() is BOTTOMIN:
                self.imgPosibleConnectH.setPos(min_c.getParent().pos + QtCore.QPointF(16, 38))
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
        for item in [self.getVisualItem(id) for id in self.dictVisualItem if self.getVisualItem(id).isBlockDef()]:
            inst = item.getInstructions()
            list.append(inst)
        return list

    def mouseMoveEvent(self, event):
        itemS = self.getItemSelected()
        if isinstance(itemS, VisualBlock):
            itemS.moveToPos(event.scenePos())

    def mousePressEvent(self, event):
        item = self.itemAt(event.scenePos(), self.view.transform())
        if self.table is not None and item is not self.table:
            self.table.close()
            self.table = None
        if isinstance(item, VisualBlock):
            item.mousePressEvent(event)

    def mouseDoubleClickEvent(self, event):
        item = self.itemAt(event.scenePos(), self.view.transform())
        if self.table is not None and item is not self.table:
            self.table.close()
            self.table = None
        if isinstance(item, VisualBlock):
            item.mouseDoubleClickEvent(event)

    def mouseReleaseEvent(self, event):
        itemS = self.getItemSelected()
        self.idItemS = None
        pos = event.scenePos()
        item = self.itemAt(pos, self.view.transform())
        if isinstance(item, VisualBlock):
            item.mouseReleaseEvent(event)

        if self.posibleConnect[0] is not None:
            c, cItS = self.posibleConnect
            if c.getIdItem() is not None:
                if c.getType() is TOP:
                    pass
                elif c.getType() in [BOTTOM, BOTTOMIN]:
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
                itemS.moveToPos(c.getParent().pos + QtCore.QPointF(0, -itemS.img.height() + 5), True)
            elif c.getType() is BOTTOM:
                itemS.moveToPos(
                    c.getParent().pos + QtCore.QPointF(0, self.getVisualItem(c.getParent().id).img.height() - 5), True)
            elif c.getType() is RIGHT:
                itemS.moveToPos(
                    c.getParent().pos + QtCore.QPointF(self.getVisualItem(c.getParent().id).img.width() - 5, 0), True)
            elif c.getType() is LEFT:
                itemS.moveToPos(c.getParent().pos + QtCore.QPointF(-self.getVisualItem(itemS.id).img.width() + 5, 0),
                                True)
            elif c.getType() is BOTTOMIN:
                itemS.moveToPos(c.getParent().pos + QtCore.QPointF(17, 33), True)
        self.parent.savetmpProject()
        self.lastItemSelect = itemS

    def useEvents(self, used):
        for VBlock in self.dictVisualItem.values():
            if VBlock.parentBlock.name == "when":
                VBlock.setEnabledDependentBlocks(used)
            elif VBlock.parentBlock.name == "main":
                VBlock.setEnabledDependentBlocks(not used)

    def thereisMain(self):
        if "main" in [v.parentBlock.name for v in self.dictVisualItem.values()]:
            return True
        else:
            return False
