from PySide import QtGui,QtCore
from math import *

import guis.var as var
from Block import *
from Language import *
from toQImage import *

def EuclideanDist(p1, p2):
    p = p1 - p2
    return sqrt(pow(p.x(), 2) + pow(p.y(), 2))


class VarGui(QtGui.QDialog, var.Ui_Dialog):

    def init(self):
        self.setupUi(self)

    def getTable(self):
        return self.table

    def setSlotToDeleteButton(self, fun):
        self.deleteButton.clicked.connect(fun)
        self.okButton.clicked.connect(self.close)


class VisualBlock(QtGui.QGraphicsPixmapItem, QtGui.QWidget):

    def __init__(self, parentBlock, parent=None, scene=None):
        self.parentBlock = parentBlock
        self.__typeBlock = self.parentBlock.typeBlock
        self.__type = self.parentBlock.type
        self.id = self.parentBlock.id
        self.connections = self.parentBlock.connections

        for c in self.connections:
            c.setParent(self.parentBlock)
        self.dicTrans = parentBlock.dicTrans
        self.shouldUpdate = True
        if len(self.dicTrans) is 0:
            self.showtext = self.parentBlock.name
        else:
            self.showtext = self.dicTrans[getLanguage()]
        QtGui.QGraphicsPixmapItem.__init__(self)
        QtGui.QWidget.__init__(self)

        # Load Image of block
        im = cv2.imread(self.parentBlock.file, cv2.IMREAD_UNCHANGED)
        r, g, b, a = cv2.split(im)
        rgb = cv2.merge((r, g, b))
        hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
        h, s, v = cv2.split(hsv)
        h = h + self.parentBlock.hue
        s = s + 130
        hsv = cv2.merge((h, s, v))
        im = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
        r, g, b = cv2.split(im)
        self.cvImg = cv2.merge((r, g, b, a))
        self.cvImg = np.require(self.cvImg, np.uint8, 'C')
        img = generateBlock(self.cvImg, 34, self.showtext, self.parentBlock.typeBlock, None, self.parentBlock.type,
                            self.parentBlock.nameControl)
        qImage = toQImage(img)
        try:
            self.header = copy.copy(self.cvImg[0:39, 0:149])
            self.foot = copy.copy(self.cvImg[69:104, 0:149])
        except:
            pass

        self.img = QtGui.QPixmap(qImage)

        self.scene = scene

        self.setFlags(QtGui.QGraphicsItem.ItemIsMovable)
        self.setZValue(1)
        self.setPos(self.parentBlock.pos)
        self.scene.activeShouldSave()
        self.setPixmap(self.img)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.posmouseinItem = None

        vars = self.parentBlock.vars

        self.DialogVar = VarGui()
        self.DialogVar.init()
        self.DialogVar.setSlotToDeleteButton(self.delete)
        self.tabVar = self.DialogVar.getTable()
        self.tabVar.verticalHeader().setVisible(False)
        self.tabVar.horizontalHeader().setVisible(False)
        self.tabVar.setColumnCount(3)
        self.tabVar.setRowCount(len(vars))

        i = 0
        for var in vars:
            self.tabVar.setCellWidget(i, 0, QtGui.QLabel(var.name))
            edit = QtGui.QLineEdit()
            edit.setValidator(QtGui.QDoubleValidator())
            edit.setText(var.defaul)
            self.tabVar.setCellWidget(i, 1, edit)
            combobox = QtGui.QComboBox()
            combobox.addItem("None")
            self.tabVar.setCellWidget(i, 2, combobox)
            i += 1
        self.sizeIn = 0
        self.shouldUpdateConnections = False
        self.popMenu = QtGui.QMenu(self)
        if self.parentBlock.name not in ["main", "when"]:
            action0 = QtGui.QAction('Duplicate', self)
            action0.triggered.connect(self.on_clicked_menu_duplicate)
            self.popMenu.addAction(action0)
        action1 = QtGui.QAction('Edit', self)
        action1.triggered.connect(self.on_clicked_menu_edit)
        self.popMenu.addAction(action1)
        self.popMenu.addSeparator()
        action2 = QtGui.QAction('Delete', self)
        action2.triggered.connect(self.on_clicked_menu_delete)
        self.popMenu.addAction(action2)

    def on_clicked_menu_duplicate(self):
        self.duplicate()
        self.scene.startAllblocks()

    def duplicate(self, old_id=None, id=None, connection=None):
        blockDuplicate = self.parentBlock.copy()
        blockDuplicate.setPos(self.parentBlock.pos + QtCore.QPointF(50, 50))
        self.scene.addItem(blockDuplicate, False)
        id_new = blockDuplicate.id
        new_connection = None
        for c in blockDuplicate.connections:
            if id is None and c.getType() in [TOP, LEFT]:
                c.setItem(None)
                c.setConnect(None)
            elif old_id is not None and c.getIdItem() == old_id:
                new_connection = c
                c.setItem(id)
                c.setConnect(connection)
            elif c.getIdItem() is not None and c.getType() not in [TOP, LEFT]:
                c_new, id_new2 = self.scene.getVisualItem(c.getIdItem()).duplicate(self.id, id_new, c)
                c.setConnect(c_new)
                c.setItem(id_new2)
        return new_connection, id_new

    def on_clicked_menu_edit(self):
        self.scene.setIdItemSelected(None)
        if self.DialogVar is not None:
            self.DialogVar.open()
            self.scene.setTable(self.DialogVar)

    def on_clicked_menu_delete(self):
        self.delete()

    def start(self):
        # self.update()
        self.timer.start(5)

    def stop(self):
        self.timer.stop()

    def activeUpdateConections(self):
        self.shouldUpdateConnections = True

    def getNameFuntion(self):
        return self.parentBlock.name

    def getIdItemBottomConnect(self):
        for c in self.connections:
            if c.getType() is BOTTOM:
                return self.scene.getVisualItem(c.getIdItem())

    def getIdItemTopConnect(self):
        for c in self.connections:
            if c.getType() is TOP:
                return self.scene.getVisualItem(c.getIdItem())

    def getNumSubBottom(self, n=0, size=0):
        size += self.img.height() - 5
        for c in self.connections:
            if c.getType() is BOTTOM:
                if c.getConnect() is None:
                    return n + 1, size + 1
                else:
                    return self.scene.getVisualItem(c.getIdItem()).getNumSubBottom(n + 1, size)
        return n + 1, size + 1

    def getNumSub(self, n=0):
        for c in self.connections:
            if c.getType() is BOTTOMIN:
                if c.getConnect() is not None:
                    return self.scene.getVisualItem(c.getIdItem()).getNumSubBottom()
                else:
                    return 0, 0
        return 0, 0

    def getInstructionsRIGHT(self, inst=[]):
        for c in self.connections:
            if c.getType() is RIGHT and c.getIdItem() is not None:
                inst = self.scene.getVisualItem(c.getIdItem()).getInstructions()
        if len(inst) is 0:
            return None
        return inst

    def getInstructionsBOTTOM(self, inst=[]):
        for c in self.connections:
            if c.getType() is BOTTOM and c.getIdItem() is not None:
                inst = self.scene.getVisualItem(c.getIdItem()).getInstructions()
        if len(inst) is 0:
            return None
        return inst

    def getInstructionsBOTTOMIN(self, inst=[]):
        for c in self.connections:
            if c.getType() is BOTTOMIN and c.getIdItem() is not None:
                inst = self.scene.getVisualItem(c.getIdItem()).getInstructions()
        if len(inst) is 0:
            return None
        return inst

    def getVars(self):
        vars = []
        for cell in range(0, self.tabVar.rowCount()):
            if self.tabVar.cellWidget(cell, 2).currentText() == "None":
                vars.append(self.tabVar.cellWidget(cell, 1).text())
            else:
                vars.append(self.tabVar.cellWidget(cell, 2).currentText())
        if len(vars) is 0:
            vars = None
        return vars

    def getInstructions(self, inst=[]):
        instRight = self.getInstructionsRIGHT()
        instBottom = self.getInstructionsBOTTOM()
        instBottomIn = self.getInstructionsBOTTOMIN()
        nameControl = self.parentBlock.nameControl
        if nameControl is "":
            nameControl = None
        dic = {}
        dic["NAMECONTROL"] = nameControl
        dic["RIGHT"] = instRight
        dic["BOTTOM"] = instBottom
        dic["BOTTOMIN"] = instBottomIn
        dic["VARIABLES"] = self.getVars()
        dic["TYPE"] = self.__type
        return self.getNameFuntion(), dic

    def getId(self):
        return self.parentBlock.id

    def updateImg(self):
        if self.__typeBlock is COMPLEXBLOCK:
            nSubBlock, size = self.getNumSub()
        else:
            size = 34

        if size is 0:
            size = 34

        if self.sizeIn != size or self.shouldUpdate:
            self.sizeIn = size
            im = generateBlock(self.cvImg, size, self.showtext, self.__typeBlock, None, self.getVars(), self.__type,
                               self.parentBlock.nameControl)
            if not self.isEnabled():
                r, g, b, a = cv2.split(im)
                im = cv2.cvtColor(im, cv2.COLOR_RGBA2GRAY)
                im = cv2.cvtColor(im, cv2.COLOR_GRAY2RGB)
                r, g, b= cv2.split(im)
                im = cv2.merge((r, g, b, a))
            qImage = toQImage(im)
            self.img = QtGui.QPixmap(qImage)
            self.setPixmap(self.img)
            for c in self.connections:
                if c.getType() is BOTTOM:
                    c.setPoint(QtCore.QPointF(c.getPoint().x(), im.shape[0] - 5))
                    if c.getIdItem() is not None:
                        self.scene.getVisualItem(c.getIdItem()).moveToPos(
                            self.pos() + QtCore.QPointF(0, self.img.height() - 5))
                if c.getType() is RIGHT:
                    c.setPoint(QtCore.QPointF(im.shape[1] - 5, c.getPoint().y()))
                    if c.getIdItem() is not None:
                        self.scene.getVisualItem(c.getIdItem()).moveToPos(
                            self.pos() + QtCore.QPointF(self.img.width() - 5, 0))
        self.shouldUpdate = False

    def updateVarValues(self):
        vars = self.getVars()
        prev_vars = self.parentBlock.getVars()
        if vars is not None:
            for i in range(0, len(vars)):
                if vars[i] != prev_vars:
                    self.shouldUpdate = True
                    self.parentBlock.updateVars(vars)
                    break

    def updateConnections(self):
        for c in self.connections:
            if c.getConnect() is not None:
                if EuclideanDist(c.getPosPoint(), c.getConnect().getPosPoint()) > 7:
                    c.getConnect().setItem(None)
                    c.getConnect().setConnect(None)
                    c.setItem(None)
                    c.setConnect(None)

    def update(self):
        if len(self.dicTrans) is not 0 and self.showtext is not self.dicTrans[getLanguage()]:
            self.shouldUpdate = True
            self.showtext = self.dicTrans[getLanguage()]

        for row in range(0, self.tabVar.rowCount()):
            combobox = self.tabVar.cellWidget(row, 2)
            items = []
            for i in reversed(range(1, combobox.count())):
                items.append(combobox.itemText(i))
                if combobox.itemText(i) not in self.scene.listNameVars:
                    combobox.removeItem(i)
                    combobox.setCurrentIndex(0)
            for var in self.scene.listNameVars:
                if var not in items:
                    combobox.addItem(var)

        self.updateVarValues()
        self.updateImg()
        if self.shouldUpdateConnections:
            self.updateConnections()

    def moveToPos(self, pos, connect=False):

        if connect is False and self.posmouseinItem is not None:
            pos = pos - self.posmouseinItem
        self.setPos(pos)
        self.parentBlock.setPos(copy.deepcopy(self.pos()))
        self.scene.activeShouldSave()
        for c in self.connections:
            if c.getType() in (TOP, LEFT) and self is self.scene.getItemSelected() and connect is not True:
                if c.getIdItem() is not None:
                    c.getConnect().setItem(None)
                    c.getConnect().setConnect(None)
                    c.setItem(None)
                    c.setConnect(None)
            elif c.getType() is BOTTOM:
                if c.getIdItem() is not None:
                    self.scene.getVisualItem(c.getIdItem()).moveToPos(
                        self.pos() + QtCore.QPointF(0, self.img.height() - 5), connect)
            elif c.getType() is BOTTOMIN:
                if c.getIdItem() is not None:
                    self.scene.getVisualItem(c.getIdItem()).moveToPos(self.pos() + QtCore.QPointF(17, 33), connect)
            elif c.getType() is RIGHT:
                if c.getIdItem() is not None:
                    self.scene.getVisualItem(c.getIdItem()).moveToPos(
                        self.pos() + QtCore.QPointF(self.img.width() - 5, 0), connect)

    def getLastItem(self):
        for c in self.connections:
            if c.getType() is BOTTOM:
                if c.getConnect() is None:
                    return c
                else:
                    return self.scene.getVisualItem(c.getIdItem()).getLastItem()
        return None

    def getLastRightItem(self):
        for c in self.connections:
            if c.getType() is RIGHT:
                if c.getConnect() is None:
                    return c
                else:
                    return self.scene.getVisualItem(c.getIdItem()).getLastItem()
        return None

    def moveToFront(self):
        self.setZValue(1)
        for c in self.connections:
            if c.getType() is BOTTOM and c.getConnect() is not None:
                self.scene.getVisualItem(c.getIdItem()).moveToFront()
                break

    def mouseMoveEvent(self, event):
        if self.isEnabled():
            self.setPos(event.scenePos() - self.posmouseinItem)
            self.parentBlock.setPos(self.pos())
            self.scene.activeShouldSave()

    def mousePressEvent(self, event):
        if self.isEnabled():
            if event.button() is QtCore.Qt.MouseButton.LeftButton:
                self.posmouseinItem = event.scenePos() - self.pos()
                self.scene.setIdItemSelected(self.id)
                if self.DialogVar is not None:
                    self.DialogVar.close()
            if event.button() is QtCore.Qt.MouseButton.RightButton:
                self.popMenu.exec_(event.screenPos())
                # self.scene.setIdItemSelected(None)
                # if self.DialogVar is not None:
                #     self.DialogVar.open()
                #     self.scene.setTable(self.DialogVar)

    def mouseDoubleClickEvent(self, event):
        if self.isEnabled():
            if event.button() is QtCore.Qt.MouseButton.LeftButton:
                self.scene.setIdItemSelected(None)
                if self.DialogVar is not None:
                    self.DialogVar.open()
                    self.scene.setTable(self.DialogVar)
            if event.button() is QtCore.Qt.MouseButton.RightButton:
                pass

    def mouseReleaseEvent(self, event):
        if self.isEnabled():
            if event.button() is QtCore.Qt.MouseButton.LeftButton:
                self.posmouseinItem = None
                self.scene.setIdItemSelected(None)
            if event.button() is QtCore.Qt.MouseButton.RightButton:
                self.posmouseinItem = None
                self.scene.setIdItemSelected(None)
                pass

    def delete(self):
        self.DialogVar.close()
        self.scene.removeItem(self.id)
        del self.cvImg
        del self.img
        del self.foot
        del self.header
        del self.timer
        del self.DialogVar
        for c in self.connections:
            if c.getIdItem() is not None:
                if c.getType() in [BOTTOM, BOTTOMIN, RIGHT]:
                    self.scene.getVisualItem(c.getIdItem()).delete()
                else:
                    c.getConnect().setConnect(None)
                    c.getConnect().setItem(None)
        if self.parentBlock.name == "when":
            # self.scene.removeByNameControl(self.parentBlock.nameControl)
            self.scene.parent.delWhen(self.parentBlock.nameControl)
        if self.parentBlock.name == "main":
            self.scene.parent.mainButton.setEnabled(True)
        del self.parentBlock

        del self

    def isBlockDef(self):
        if self.parentBlock.name == "when":
            return True
        for c in self.connections:
            if c.getType() in [TOP, BOTTOM, RIGHT, LEFT]:
                return False

        return True

    def setEnabledDependentBlocks(self,enable):
        self.shouldUpdate = True
        self.setEnabled(enable)
        for c in self.connections:
            if c.getIdItem() is not None and c.getType() not in [TOP, LEFT]:
                self.scene.getVisualItem(c.getIdItem()).setEnabledDependentBlocks(enable)
