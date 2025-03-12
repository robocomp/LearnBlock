#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import
import os, binascii
from PySide6 import QtGui, QtWidgets

from learnbot_dsl.blocksConfig.blocks import hsv_color
from learnbot_dsl.learnbotCode.AbstractBlock import *
from learnbot_dsl.learnbotCode.Language import getLanguage
import tempfile, uuid, sys, traceback

def str2hex(text):
    if sys.version_info[0]>=3:
        return text.encode('utf-8').hex()
    else:
        return str(binascii.hexlify(bytes(text)))

class Block_Button(QtWidgets.QPushButton):

    def __init__(self, args):
        if len(args) == 14:
            self.__parent, self.__text, self.__dicTrans, self.hue, self.__view, self.__scene, self.__file, self.__connections, self.__vars, self.__blockType, self.__table, self.__row, self.__type, self.__dicToolTip = args
        elif len(args) == 6:
            self.__parent, abstracBlock, self.__view, self.__scene, self.__table, self.__row = args
            self.__text = abstracBlock.name
            self.__dicTrans = abstracBlock.dicTrans
            self.__dicToolTip = abstracBlock.dicToolTip
            self.__file = abstracBlock.file
            self.__connections = abstracBlock.connections
            self.__vars = abstracBlock.vars
            self.__blockType = abstracBlock.typeBlock
            self.__type = abstracBlock.type
            self.hue = abstracBlock.hue

        QtWidgets.QPushButton.__init__(self)
        #change color block

        self.loadImg()

        self.clicked.connect(self.on_clickedButton)
        self.__item = self.__table.item(self.__row, 0)
        self.updateToolTip()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updateImg)
        self.timer.start(5)
        self.setFlat(True)

    def loadImg(self):
        """Load or generate the image for the block and apply translations and styles."""
        self.tmpFile = self._generateTmpFilename()
        self.showtext = self._getShowText()

        if not os.path.exists(self.tmpFile):
            im = self._loadAndModifyImage()
            variables = self._getVariablesForImage()
            img = generateBlock(im, 34, self.showtext, self.__blockType, self.__connections, variables, self.__type)
            cv2.imwrite(self.tmpFile, img, (cv2.IMWRITE_PNG_COMPRESSION, 9))
        else:
            img = cv2.imread(self.tmpFile, cv2.IMREAD_UNCHANGED)

        self._updateIconDisplay(img)

    def _generateTmpFilename(self):
        """Create a unique filename for the block's temporary image file."""
        try:
            connection_types = [type for _, type in self.__connections]
        except:
            connection_types = [c.getType() for c in self.__connections]
        tmpString = (
            f"{self.__text}{self.__type}{self.__blockType}{len(self.__connections)}"
            f"{''.join(map(str, connection_types))}{getLanguage()}"
        )
        return os.path.join(tempfile.gettempdir(), f".{str2hex(tmpString)}.png")

    def _getShowText(self):
        """Retrieve the display text based on available translations."""
        if self.__dicTrans:
            return self.__dicTrans.get(getLanguage(), self.__text)
        return self.__text

    def _loadAndModifyImage(self):
        """Load the base image and apply hue adjustments."""
        im = cv2.imread(self.__file, cv2.IMREAD_UNCHANGED)

        if im is None:
            raise ValueError("Error: No se pudo cargar la imagen. Verifica la ruta del archivo.")

        # Convertir a HSV solo los primeros 3 canales (R, G, B)
        hsv = cv2.cvtColor(im[:, :, :3], cv2.COLOR_BGR2HSV)

        # Modificar el tono (hue) y la saturación
        hsv[:, :, 0] = (hsv[:, :, 0] + self.hue) % 180  # Hue está en un rango de 0-179 en OpenCV
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] + 255, 0, 255)  # Evitar saturación fuera de rango

        # Convertir de vuelta a RGB
        modified_img = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

        # Verificar si la imagen original tenía un canal alfa
        if im.shape[2] == 4:
            # Si tiene canal alfa, fusionarlo con la imagen modificada
            result = np.dstack((modified_img, im[:, :, 3]))
        else:
            result = modified_img

        return result

    def _getVariablesForImage(self):
        """Retrieve translated variable names for the block."""
        if self.__type != VARIABLE:
            return [
                x.translate.get(getLanguage(), x.name) if hasattr(x, "translate") else x.name
                for x in self.__vars
            ]
        return []

    def _updateIconDisplay(self, img):
        """Update icon display settings in the UI."""
        width = self.__parent.ui.functions.width() - 51
        self.__table.setColumnWidth(0, width - 20)
        self.setIconSize(QtCore.QSize(width - 20, img.shape[0]))
        self.__table.setRowHeight(self.__row, img.shape[0])
        self.setIcon(QtGui.QIcon(self.tmpFile))
        self.setStyleSheet("QPushButton { text-align: left; }")

    def updateIconSize(self, width):
        size = self.iconSize()
        size.setWidth(width)
        # print(self.__row)
        # print(self.__table.row(self.__row))
        size.setHeight(self.__table.rowHeight(self.__row))
        self.setIconSize(size)

    def updateToolTip(self):
        try:
            text = ""
            if len(self.__dicToolTip) != 0:
                text = self.__dicToolTip[getLanguage()]
            sizeline = 0
            if len(self.__dicTrans) != 0:
                textout = self.__dicTrans[getLanguage()] + ": "
            else:
                textout = self.__text + ": "
            for word in text.split(" "):
                sizeline += len(word)
                if sizeline < 50:
                    textout += word + " "
                else:
                    textout += "\n" + word + " "
                    sizeline = len(word)
            self.setToolTip(textout)
        except:
            pass

    def getCopy(self, table):
        return Block_Button(
            (self.__parent, self.getAbstracBlockItem(), self.__view, self.__scene, table, table.rowCount() - 1))

    def getCurrentText(self):
        return self.showtext

    def removeTmpFile(self):
        try:
            os.remove(self.tmpFile)
        except Exception as e:
            traceback.print_exc()

    def updateImg(self):
        if len(self.__dicTrans) != 0 and self.showtext != self.__dicTrans[getLanguage()]:
            self.loadImg()
            self.updateToolTip()

    def on_clickedButton(self):
        block = AbstractBlock(0, 0, self.__text, self.__dicTrans, self.__file, copy.deepcopy(self.__vars), self.hue, "",
                              self.__connections, self.__blockType, self.__type)
        self.__scene.addItem(copy.deepcopy(block))
        if self.__text == "main":
            self.setEnabled(False)

    def getAbstracBlockItem(self):
        return AbstractBlock(0, 0, self.__text, self.__dicTrans, self.__file, copy.deepcopy(self.__vars), self.hue, "",
                             self.__connections, self.__blockType, self.__type, dicToolTip=self.__dicToolTip)

    def delete(self, row):
        self.__table.removeCellWidget(row, 0)
        self.__table.removeRow(row)
        self.__scene.removeByName(self.__text,False)
        del self

    def getText(self):
        return self.__text
