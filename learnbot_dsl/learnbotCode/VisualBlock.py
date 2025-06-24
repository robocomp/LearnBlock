from __future__ import print_function, absolute_import
from PySide6 import QtGui,QtWidgets
from math import *
import pickle, os, json
import learnbot_dsl.guis.EditVar as EditVar
from learnbot_dsl.learnbotCode.Block import *
from learnbot_dsl.learnbotCode.Language import getLanguage
from learnbot_dsl.learnbotCode.toQImage import *
from learnbot_dsl.learnbotCode.Parser import parserLearntBotCodeOnlyUserFuntion
from  learnbot_dsl.learnbotCode import getAprilTextDict
class KeyPressEater(QtCore.QObject):
    def eventFilter(self, obj, event):
        if isinstance(event, QtGui.QMouseEvent) and event.buttons() & QtCore.Qt.RightButton:
            return True
        return False

def toLBotPy(inst, ntab=1, offset=0):
    text = inst[0]
    if inst[1]["TYPE"] in [USERFUNCTION, LIBRARY]:
        text = inst[0] + "()"
    else:
        inst[1]["VISUALBLOCK"].startOffset = offset
    if inst[1]["TYPE"] is CONTROL:
        if inst[1]["VARIABLES"] is not None:
            text = inst[0] + "("
            for var in inst[1]["VARIABLES"]:
                text += var + ", "
            text = text[0:-2] + ""
            text += ")"
    if inst[1]["TYPE"] is FUNTION:
        text = "function." + inst[0] + "("
        if inst[1]["VARIABLES"] is not None:
            for var in inst[1]["VARIABLES"]:
                text += var + ", "
            text = text[0:-2] + ""
        text += ")"
    elif inst[1]["TYPE"] is VARIABLE:
        text = inst[0]
        if inst[1]["VARIABLES"] is not None:
            text += " = "
            for var in inst[1]["VARIABLES"]:
                text += var

    if inst[1]["RIGHT"] is not None:
        text += " "
        text += toLBotPy(inst[1]["RIGHT"], ntab, len(text) + offset)
    if inst[1]["BOTTOMIN"] is not None:
        text += ":\n" + "\t" * ntab
        text += toLBotPy(inst[1]["BOTTOMIN"], ntab + 1, len(text) + offset)
    if inst[0] in ["while", "while True"]:
        text += "\n" + "\t" * (ntab - 1) + "end"
    if inst[0] == "else" or (inst[0] in ["if", "elif"] and (inst[1]["BOTTOM"] is None or (
            inst[1]["BOTTOM"] is not None and inst[1]["BOTTOM"][0] not in ["elif", "else"]))):
        text += "\n" + "\t" * (ntab - 1) + "end"

    inst[1]["VISUALBLOCK"].endOffset = len(text)-1 + offset

    if inst[1]["BOTTOM"] is not None:
        text += "\n" + "\t" * (ntab - 1)
        text += toLBotPy(inst[1]["BOTTOM"], ntab, len(text) + offset)
    return text

def EuclideanDist(p1, p2):
    p = p1 - p2
    return sqrt(pow(p.x(), 2) + pow(p.y(), 2))


class VarGui(QtWidgets.QDialog, EditVar.Ui_Dialog):

    def init(self):
        self.setupUi(self)

    def getTable(self):
        return self.table

    def setSlotToDeleteButton(self, fun):
        self.deleteButton.clicked.connect(fun)
        self.okButton.clicked.connect(self.close)


class VisualBlock(QtWidgets.QGraphicsPixmapItem, QtWidgets.QWidget):

    def __init__(self, parentBlock, parent=None, scene=None):
        """
        Initializes a VisualBlock instance based on a given parent block, setting up
        display attributes, connections, image properties, and interactions within the scene.

        Parameters:
        - parentBlock: The block this visual representation is based on.
        - parent: Optional parent widget, if applicable.
        - scene: The scene where this VisualBlock is displayed.
        """

        # Initialize offsets for positioning connections
        self.startOffset = None
        self.endOffset = None

        # List to store any active notifications for this block
        self._notifications = []

        # Reference to the associated logical block (parentBlock)
        self.parentBlock = parentBlock

        # Store block type and ID for quick access
        self.__typeBlock = self.parentBlock.typeBlock
        self.__type = self.parentBlock.type
        self.id = self.parentBlock.id

        # Initialize connection information and mark block as not highlighted
        self.connections = self.parentBlock.connections
        self.highlighted = False

        # Set each connection’s parent to the current block
        for c in self.connections:
            c.setParent(self.parentBlock)

        # Dictionary to store translations, if available
        self.dicTrans = parentBlock.dicTrans

        # Determine if an update is needed initially
        self.shouldUpdate = True

        # Set display text based on the available translations or block name
        self.showtext = self.dicTrans.get(getLanguage(), self.parentBlock.name) if self.dicTrans else self.parentBlock.name

        # Initialize as both a QGraphicsPixmapItem and QWidget
        QtWidgets.QGraphicsPixmapItem.__init__(self)
        QtWidgets.QWidget.__init__(self)


        # Load Image of block
        # Load the block’s image and extract RGB and Alpha channels for customization
        im = cv2.imread(self.parentBlock.file, cv2.IMREAD_UNCHANGED)
        b, g, r, a = cv2.split(im)

        # Convert image to RGB format for hue and saturation adjustment
        rgb = cv2.merge((r, g, b))
        hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)

        # Adjust hue and increase saturation for visual distinction
        h, s, v = cv2.split(hsv)

        h = h + self.parentBlock.hue
        s = s + self.parentBlock.saturation
        v[v>200] = self.parentBlock.brightness

        hsv = cv2.merge((h, s, v))

        # Convert back to RGB and merge with alpha channel to preserve transparency
        im = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
        r, g, b = cv2.split(im)
        self.cvImg = cv2.merge((b, g, r, a))
        self.cvImg = np.require(self.cvImg, np.uint8, 'C')

        # Generate final image with text overlay, using block’s characteristics
        img = generateBlock(self.cvImg, 34, self.showtext, self.parentBlock.typeBlock, None, self.parentBlock.type,
                            self.parentBlock.nameControl)
        qImage = toQImage(img)

        # Attempt to save the header and footer sections of the image
        try:
            self.header = copy.copy(self.cvImg[0:39, 0:149])
            self.foot = copy.copy(self.cvImg[69:104, 0:149])
        except Exception:
            pass

        # Set the pixmap representation for this VisualBlock
        self.img = QtGui.QPixmap(qImage)

        # Store a reference to the scene in which this block is located
        self.scene = scene

        # Enable movement of the block and set its stacking order
        self.setFlags(QtWidgets.QGraphicsItem.ItemIsMovable)
        self.setZValue(1)

        # Place the block at the initial position of the logical block
        self.setPos(self.parentBlock.pos)

        # Notify the scene that changes may need to be saved
        self.scene.activeShouldSave()
        self.updatePixmap()

        # Timer setup to trigger periodic updates for this block
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)

        # Initialize variables for managing mouse position and dialog interactions
        self.posmouseinItem = None
        self.DialogVar = None
        self.popMenu = None

        # Create any necessary dialogs related to this block
        self.create_dialogs()

        # Initialize connection management variables
        self.sizeIn = 0
        self.shouldUpdateConnections = False

    def addNotification(self, notification):
        tooltip = self.toolTip()

        if tooltip:
            tooltip += '<hr />'

        tooltip += notification.simpleHtml()

        self.setToolTip(tooltip)
        self._notifications.append(notification)

    def clearNotifications(self):
        self._notifications = []
        self.setToolTip('')

    def notifications(self):
        return self._notifications

    def highlight(self):
        self.highlighted = True
        self.updateImg(force=True)
        self.updatePixmap()

    def unhighlight(self):
        self.highlighted = False
        self.updateImg(force=True)
        self.updatePixmap()

    def updatePixmap(self):
        self.setPixmap(self.img)

    def create_dialogs(self):

        if self.DialogVar is not None:
            del self.DialogVar

        vars = self.parentBlock.vars

        self.DialogVar = VarGui()
        self.DialogVar.init()
        self.DialogVar.setSlotToDeleteButton(self.delete)
        self.tabVar = self.DialogVar.getTable()
        self.tabVar.verticalHeader().setVisible(False)
        self.tabVar.horizontalHeader().setVisible(True)
        self.tabVar.setColumnCount(4)
        self.tabVar.setRowCount(len(vars))
        self.tableHeader = [] #QtCore.QStringList()
        self.tableHeader.append(self.tr('Name'))
        self.tableHeader.append(self.tr('Constant'))
        self.tableHeader.append(self.tr('Set to'))
        self.tableHeader.append(self.tr('Type'))
        self.tabVar.setHorizontalHeaderLabels(self.tableHeader)
        self.tabVar.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)

        # i = 0
        for i, var in zip(range(len(vars)),vars):
            try:
                if getLanguage() in var.translate:
                    self.tabVar.setCellWidget(i, 0, QtWidgets.QLabel(var.translate[getLanguage()]))
                else:
                    self.tabVar.setCellWidget(i, 0, QtWidgets.QLabel(var.name))
            except:
                self.tabVar.setCellWidget(i, 0, QtWidgets.QLabel(var.name))
            if var.type in ["float","int", "string"]:
                edit = QtWidgets.QLineEdit()
                if var.type == "float":
                    edit.setValidator(QtGui.QDoubleValidator())
                    self.tabVar.setCellWidget(i,3,QtWidgets.QLabel(self.tr('number')))
                elif var.type == "int":
                    edit.setValidator(QtGui.QIntValidator())
                    self.tabVar.setCellWidget(i,3,QtWidgets.QLabel(self.tr('number')))
                else:
                    self.tabVar.setCellWidget(i,3,QtWidgets.QLabel(self.tr('string')))
                if var.type == "string":
                    edit.setText(var.defaul.replace('\"', ''))
                else:
                    edit.setText(var.defaul)
                self.tabVar.setCellWidget(i, 1, edit)
            elif var.type == "boolean":
                combobox = QtWidgets.QComboBox()
                combobox.addItem("True")
                combobox.addItem("False")
                if var.defaul in ("0", "False"):
                    combobox.setCurrentIndex(1)
                else:
                    combobox.setCurrentIndex(0)
                self.tabVar.setCellWidget(i, 1, combobox)
                self.tabVar.setCellWidget(i,3,QtWidgets.QLabel(self.tr('boolean')))
            elif var.type == "list":
                values = var.translateValues[getLanguage()]
                combobox = QtWidgets.QComboBox()
                combobox.addItems(values)
                self.tabVar.setCellWidget(i, 1, combobox)
                self.tabVar.setCellWidget(i,3,QtWidgets.QLabel(self.tr('list')))
            elif var.type == "apriltext":
                dictApriText = getAprilTextDict()
                combobox = QtWidgets.QComboBox()
                combobox.addItems([x for x in dictApriText])
                self.tabVar.setCellWidget(i, 1, combobox)
                self.tabVar.setCellWidget(i,3,QtWidgets.QLabel(self.tr('apriltext')))

            combobox = QtWidgets.QComboBox()
            combobox.addItem(self.tr('Constant'))
            self.tabVar.setCellWidget(i, 2, combobox)
#            self.tabVar.setCellWidget(i,3,QtWidgets.QLabel(var.type))
            # i += 1

        if self.popMenu is not None:
            del self.popMenu
            del self.keyPressEater

        self.popMenu = QtWidgets.QMenu(self)

        self.keyPressEater = KeyPressEater(self.popMenu)
        self.popMenu.installEventFilter(self.keyPressEater)

        action1 = QtGui.QAction(self.tr('Edit'), self)
        action1.triggered.connect(self.on_clicked_menu_edit)
        self.popMenu.addAction(action1)
        if self.parentBlock.name not in ["main", "when"]:
            if self.parentBlock.type is USERFUNCTION and self.parentBlock.typeBlock is COMPLEXBLOCK:
                action3 = QtGui.QAction(self.tr('Export Block'), self)
                action3.triggered.connect(self.on_clicked_menu_export_block)
                self.popMenu.addAction(action3)
            else:
                action0 = QtGui.QAction(self.tr('Duplicate'), self)
                action0.triggered.connect(self.on_clicked_menu_duplicate)
                self.popMenu.addAction(action0)

        self.popMenu.addSeparator()
        action2 = QtGui.QAction(self.tr('Delete'), self)
        action2.triggered.connect(self.on_clicked_menu_delete)
        # action2.installEventFilter(self.keyPressEater)
        self.popMenu.addAction(action2)

    def on_clicked_menu_export_block(self):
        if self.parentBlock.name not in ["main", "when"] and self.parentBlock.type is USERFUNCTION and self.parentBlock.typeBlock is COMPLEXBLOCK:

            self.scene.stopAllblocks()
            path = QtWidgets.QFileDialog.getExistingDirectory(self, self.tr('Select Library'), self.scene.parent.libraryPath, QtWidgets.QFileDialog.ShowDirsOnly)
            self.scene.startAllblocks()
            ret = None
            try:
                os.mkdir(os.path.join(path, self.parentBlock.name))
            except:
                msgBox = QtWidgets.QMessageBox()
                msgBox.setWindowTitle(self.tr("Warning"))
                msgBox.setIcon(QtWidgets.QMessageBox.Warning)
                msgBox.setText(self.tr("This module already exists"))
                msgBox.setInformativeText(self.tr("Do you want to overwrite the changes?"))
                msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok| QtWidgets.QMessageBox.Cancel)
                msgBox.setDefaultButton(QtWidgets.QMessageBox.Ok)
                ret = msgBox.exec_()
            if ret is None or ret == QtWidgets.QMessageBox.Ok:
                path = os.path.join(path, self.parentBlock.name)
                # Save blockProject
                lBInstance = self.scene.parent
                with open(os.path.join(path, self.parentBlock.name + ".blockProject"), 'wb') as fichero:
                    dic = copy.deepcopy(lBInstance.scene.dicBlockItem)
                    for id in dic:
                        block = dic[id]
                        block.file = os.path.basename(block.file)
                    pickle.dump(
                        (dic, lBInstance.listNameWhens, lBInstance.listUserFunctions, lBInstance.listNameVars, lBInstance.listNameUserFunctions),
                        fichero, 0)
                # Save config block
                dictBlock = {}
                dictBlock["name"] = self.parentBlock.name
                dictBlock["type"] = "library"
                dictBlock["shape"] = ["blockVertical"]
                with open(os.path.join(path, self.parentBlock.name + ".conf"),'w') as f:
                    json.dump([dictBlock], f)
                # Save script learnCode
                inst = self.getInstructions()
                code = "def " + toLBotPy(inst) + "\nend\n\n"
                with open(os.path.join(path, self.parentBlock.name + ".lb"), 'w') as f:
                    f.write(code)
                # Save script python
                codePython = parserLearntBotCodeOnlyUserFuntion(code)
                with open(os.path.join(path, self.parentBlock.name + ".py"), 'w') as f:
                    f.write(codePython)
                pass

    def on_clicked_menu_duplicate(self):
        if self.parentBlock.name not in ["main", "when"] and not (self.parentBlock.type is USERFUNCTION and self.parentBlock.typeBlock is COMPLEXBLOCK):
            self.duplicate()
            self.scene.startAllblocks()
            self.scene.parent.savetmpProject()

    def duplicate(self, old_id=None, id=None, connection=None):
        blockDuplicate = self.parentBlock.copy()
        blockDuplicate.setPos(self.parentBlock.pos + QtCore.QPointF(50, 50))
        self.scene.addItem(blockDuplicate, False, False, False)
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
        if self.DialogVar is not None and len(self.parentBlock.getVars())>0:
            self.setCurrentParamInDialog()
            self.DialogVar.open()
            self.scene.setTable(self.DialogVar)

    def setCurrentParamInDialog(self):
        varS = self.parentBlock.getVars()
        if len(varS)>0:
            combo = self.tabVar.cellWidget(0, 2)
            assignList = [combo.itemText(i) for i in range(combo.count())]
            for cell, var in zip(range(len(varS)), varS):
                if varS[cell].defaul in assignList:
                    index = assignList.index(varS[cell].defaul)
                    self.tabVar.cellWidget(cell, 2).setCurrentIndex(index)
                    if var.type in ["float","int", "string"]:
                        self.tabVar.cellWidget(cell, 1).setText("")
                    else:
                        self.tabVar.cellWidget(cell, 1).setCurrentIndex(0)

    def on_clicked_menu_delete(self):
        self.delete()

    def start(self):
        self.timer.start(5)

    def stop(self):
        self.timer.stop()

    def activeUpdateConections(self):
        self.shouldUpdateConnections = True

    def getNameFuntion(self):
        return self.parentBlock.name

    def getIdItemBottomConnect(self):
        for c in [conn for conn in self.connections if conn.getType() is BOTTOM]:
            return self.scene.getVisualItem(c.getIdItem())

    def getIdItemTopConnect(self):
        for c in [conn for conn in self.connections if conn.getType() is TOP]:
            return self.scene.getVisualItem(c.getIdItem())

    def getNumSubBottom(self, n=0, size=0):
        size += self.img.height() - 5
        for c in [conn for conn in self.connections if conn.getType() is BOTTOM]:
            if c.getConnect() is None:
                return n + 1, size + 1
            else:
                return self.scene.getVisualItem(c.getIdItem()).getNumSubBottom(n + 1, size)
        return n + 1, size + 1

    def getNumSub(self, n=0):
        for c in [conn for conn in self.connections if conn.getType() is BOTTOMIN and conn.getConnect() is not None]:
            return self.scene.getVisualItem(c.getIdItem()).getNumSubBottom()
        return 0, 0

    def getInstructionsRIGHT(self, inst=[]):
        for c in [conn for conn in self.connections if conn.getType() is RIGHT and conn.getIdItem() is not None]:
            inst = self.scene.getVisualItem(c.getIdItem()).getInstructions()
        if len(inst) == 0:
            return None
        return inst

    def getInstructionsBOTTOM(self, inst=[]):
        for c in [conn for conn in self.connections if conn.getType() is BOTTOM and conn.getIdItem() is not None]:
            inst = self.scene.getVisualItem(c.getIdItem()).getInstructions()
        if len(inst) == 0:
            return None
        return inst

    def getInstructionsBOTTOMIN(self, inst=[]):
        for c in [conn for conn in self.connections if conn.getType() is BOTTOMIN and conn.getIdItem() is not None]:
            inst = self.scene.getVisualItem(c.getIdItem()).getInstructions()
        if len(inst) == 0:
            return None
        return inst

    def getVars(self):
        vars = []
        varS = self.parentBlock.getVars()
        # for cell in range(0, self.tabVar.rowCount()):
        for cell, var in zip(range(len(varS)), varS):

            if self.tabVar.cellWidget(cell, 2).currentText() == self.tr('Constant'):
                if self.tabVar.cellWidget(cell, 3).text() == "boolean":
                    vars.append(self.tabVar.cellWidget(cell, 1).currentText())
                elif self.tabVar.cellWidget(cell, 3).text() == "list":
                    vars.append('"' + var.values[self.tabVar.cellWidget(cell, 1).currentIndex()] + '"')
                elif self.tabVar.cellWidget(cell, 3).text() == "apriltext":
                    vars.append('"' +self.tabVar.cellWidget(cell, 1).currentText() + '"')
                elif self.tabVar.cellWidget(cell, 3).text() == "string":
                    vars.append('"'+self.tabVar.cellWidget(cell, 1).text()+'"')
                else:
                    vars.append(self.tabVar.cellWidget(cell, 1).text())
            else:
                vars.append(self.tabVar.cellWidget(cell, 2).currentText())
        if len(vars) == 0:
            vars = None
        return vars

    def getInstructions(self, inst=[]):
        instRight = self.getInstructionsRIGHT()
        instBottom = self.getInstructionsBOTTOM()
        instBottomIn = self.getInstructionsBOTTOMIN()
        nameControl = self.parentBlock.nameControl
        if nameControl == "":
            nameControl = None
        dic = {}
        dic["NAMECONTROL"] = nameControl
        dic["RIGHT"] = instRight
        dic["BOTTOM"] = instBottom
        dic["BOTTOMIN"] = instBottomIn
        dic["VARIABLES"] = self.getVars()
        dic["TYPE"] = self.__type
        dic["VISUALBLOCK"] = self
        return self.getNameFuntion(), dic

    def getId(self):
        return self.parentBlock.id

    def updateImg(self, force=False):
        size = self.calculateSize()

        # Check if image needs to be updated
        if self.needsImageUpdate(size, force):
            self.sizeIn = size
            self.updateMainImage(size)

            # Adjust connections if needed
            if self.sizeIn != size or self.shouldUpdateConnections or force:
                self.adjustConnections()

        self.shouldUpdate = False

    def calculateSize(self):
        """Determine the required size for the image, defaulting to 34."""
        if self.__typeBlock is COMPLEXBLOCK:
            _, size = self.getNumSub()
        else:
            size = 34
        return max(size, 34)

    def needsImageUpdate(self, size, force):
        """Check if image update is required based on size or update flags."""
        return self.sizeIn != size or self.shouldUpdate or force

    def updateMainImage(self, size):
        """Generate and set the main image for the block."""
        im = generateBlock(
            self.cvImg, size, self.showtext, self.__typeBlock, None, self.getVars(), self.__type,
            self.parentBlock.nameControl
        )
        if self.highlighted:
            im = generate_error_block(im)

        if not self.isEnabled():
            im = self.applyDisabledEffect(im)

        qImage = toQImage(im)
        self.img = QtGui.QPixmap(qImage)
        self.updatePixmap()

    def applyDisabledEffect(self, im):
        """Convert image to grayscale to indicate disabled state."""
        r, g, b, a = cv2.split(im)
        gray = cv2.cvtColor(im, cv2.COLOR_RGBA2GRAY)
        im = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)
        return cv2.merge((r, g, b, a))

    def adjustConnections(self):
        """Adjust the positions of connected items based on connection type."""
        for connection in self.connections:
            if connection.getType() is BOTTOM:
                self.adjustBottomConnection(connection)
            elif connection.getType() is RIGHT:
                self.adjustRightConnection(connection)

    def adjustBottomConnection(self, connection):
        """Set the bottom connection point and reposition connected item if necessary."""
        connection.setPoint(QtCore.QPointF(connection.getPoint().x(), self.img.height() - 5))
        if connection.getIdItem() is not None:
            self.scene.getVisualItem(connection.getIdItem()).moveToPos(
                self.pos() + QtCore.QPointF(0, self.img.height() - 5)
            )

    def adjustRightConnection(self, connection):
        """Set the right connection point and reposition connected item if necessary."""
        connection.setPoint(QtCore.QPointF(self.img.width() - 5, connection.getPoint().y()))
        if connection.getIdItem() is not None:
            self.scene.getVisualItem(connection.getIdItem()).moveToPos(
                self.pos() + QtCore.QPointF(self.img.width() - 5, 0)
            )

    def updateVarValues(self):
        vars = self.getVars()
        prev_vars = self.parentBlock.getVars()
        if vars is not None:
            for i in range(0, len(vars)):
                if vars[i] != prev_vars[i].defaul:
                    self.shouldUpdate = True
                    self.parentBlock.updateVars(vars)
                    break

    def updateConnections(self):
        for c in [conn for conn in self.connections if conn.getConnect() is not None and EuclideanDist(conn.getPosPoint(), conn.getConnect().getPosPoint()) > 7]:
            c.getConnect().setItem(None)
            c.getConnect().setConnect(None)
            c.setItem(None)
            c.setConnect(None)

    def update(self):
        if len(self.dicTrans) != 0 and self.showtext is not self.dicTrans[getLanguage()]:
            #Language change

            self.create_dialogs()

            self.shouldUpdate = True
            self.showtext = self.dicTrans[getLanguage()]
            vars = self.parentBlock.vars
            for i, var in zip(range(len(vars)), vars):
                try:
                    if getLanguage() in var.translate:
                        self.tabVar.setCellWidget(i, 0, QtWidgets.QLabel(var.translate[getLanguage()]))
                    else:
                        self.tabVar.setCellWidget(i, 0, QtWidgets.QLabel(var.name))
                    if var.type == "list":
                        values = var.translateValues[getLanguage()]
                        val = self.tabVar.cellWidget(i, 1).currentIndex()
                        combobox = QtWidgets.QComboBox()
                        combobox.addItems(values)
                        self.tabVar.setCellWidget(i, 1, combobox)
                        combobox.setCurrentIndex(val)
                except:
                    self.tabVar.setCellWidget(i, 0, QtWidgets.QLabel(var.name))

        for row in range(0, self.tabVar.rowCount()):
            combobox = self.tabVar.cellWidget(row, 2)
            items = []
            for i in reversed(range(1, combobox.count())):
                items.append(combobox.itemText(i))
                if combobox.itemText(i) not in self.scene.parent.listNameVars:
                    combobox.removeItem(i)
                    combobox.setCurrentIndex(0)
            for var in self.scene.parent.listNameVars:
                if var not in items:
                    combobox.addItem(var)

        self.updateVarValues()
        self.updateImg()
        if self.shouldUpdateConnections:
            self.updateConnections()

    def moveToPos(self, pos, connect=False):
        if self.highlighted:
            self.unhighlight()
            self.clearNotifications()
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
        for c in [conn for conn in self.connections if conn.getType() is BOTTOM]:
            if c.getConnect() is None:
                return c
            else:
                return self.scene.getVisualItem(c.getIdItem()).getLastItem()
        return None

    def getLastRightItem(self):
        for c in [conn for conn in self.connections if conn.getType() is RIGHT]:
            if c.getConnect() is None:
                return c
            else:
                return self.scene.getVisualItem(c.getIdItem()).getLastRightItem()
        return None

    def moveToFront(self):
        self.setZValue(1)
        for c in [conn for conn in self.connections if conn.getType() in [BOTTOM, BOTTOMIN] and conn.getConnect() is not None]:
            self.scene.getVisualItem(c.getIdItem()).moveToFront()

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

    def delete(self, savetmp=True):
        self.DialogVar.close()
        del self.cvImg
        del self.img
        del self.foot
        del self.header
        del self.timer
        del self.DialogVar
        for c in [conn for conn in self.connections if conn.getIdItem() is not None]:
            if c.getType() in [BOTTOM, BOTTOMIN, RIGHT]:
                self.scene.getVisualItem(c.getIdItem()).delete(savetmp=False)
            else:
                c.getConnect().setConnect(None)
                c.getConnect().setItem(None)
        if self.parentBlock.name == "when":
            self.scene.parent.delWhen(self.parentBlock.nameControl)
        if self.parentBlock.name == "main" and self.scene.parent.mainButton is not None:
            self.scene.parent.mainButton.setEnabled(True)
        self.scene.removeItem(self.id, savetmp)
        del self.parentBlock
        del self

    def isBlockDef(self):
        if self.parentBlock.name == "when":
            return True
        if len([conn for conn in self.connections if conn.getType() in [TOP, BOTTOM, RIGHT, LEFT]])>0:
            return False
        return True

    def setEnabledDependentBlocks(self,enable):
        self.shouldUpdate = True
        self.setEnabled(enable)
        for c in [conn for conn in self.connections if conn.getIdItem() is not None and conn.getType() not in [TOP, LEFT]]:
            self.scene.getVisualItem(c.getIdItem()).setEnabledDependentBlocks(enable)
