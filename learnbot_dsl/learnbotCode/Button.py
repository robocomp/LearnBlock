#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from PySide import QtGui

from AbstractBlock import *
from Language import *
import tempfile
import uuid

class Block_Button(QtGui.QPushButton):

    def __init__(self, args):
        if len(args) is 14:
            self.__parent, self.__text, self.__dicTrans, self.hue, self.__view, self.__scene, self.__file, self.__connections, self.__vars, self.__blockType, self.__table, self.__row, self.__type, self.__dicToolTip = args
            self.tmpFile = os.path.join(tempfile.gettempdir(), str(uuid.uuid4().hex) + ".png")

        elif len(args) is 6:
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
            self.tmpFile = os.path.join(tempfile.gettempdir(), str(uuid.uuid4().hex) + ".png")

        QtGui.QPushButton.__init__(self)
        #change color block
        im = cv2.imread(self.__file, cv2.IMREAD_UNCHANGED)
        r, g, b, a = cv2.split(im)
        rgb = cv2.merge((r, g, b))
        hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
        h, s, v = cv2.split(hsv)
        h = h + self.hue
        s = s + 130
        hsv = cv2.merge((h, s, v))
        im = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
        r, g, b = cv2.split(im)
        im = cv2.merge((r, g, b, a))

        self.showtext = self.__text

        if len(self.__dicTrans) is not 0:
            self.showtext = self.__dicTrans[getLanguage()]
            self.updateImg()
        var = [x.name for x in self.__vars]
        img = generateBlock(im, 34, self.showtext, self.__blockType, self.__connections, var, self.__type)
        cv2.imwrite(self.tmpFile, img, (cv2.IMWRITE_PNG_COMPRESSION, 9))
        self.setIcon(QtGui.QIcon(self.tmpFile))
        self.setIconSize(QtCore.QSize(135, im.shape[0]))
        self.setFixedSize(QtCore.QSize(150, im.shape[0]))
        self.__table.setRowHeight(self.__row, im.shape[0])
        self.clicked.connect(self.on_clickedButton)
        self.__item = self.__table.item(self.__row, 0)
        self.updateToolTip()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updateImg)
        self.timer.start(5)

    def updateToolTip(self):
        try:
            text = self.__dicToolTip[getLanguage()]
            sizeline = 0
            textout = ""
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
            print e

    def updateImg(self):
        if len(self.__dicTrans) is not 0 and self.showtext is not self.__dicTrans[getLanguage()]:
            self.showtext = self.__dicTrans[getLanguage()]
            im = cv2.imread(self.__file, cv2.IMREAD_UNCHANGED)
            # change color block
            r, g, b, a = cv2.split(im)
            rgb = cv2.merge((r, g, b))
            hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
            h, s, v = cv2.split(hsv)
            h = h + self.hue
            s = s + 130
            hsv = cv2.merge((h, s, v))
            im = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
            r, g, b = cv2.split(im)
            im = cv2.merge((r, g, b, a))
            img = generateBlock(im, 34, self.showtext, self.__blockType, self.__connections, None, self.__type)
            cv2.imwrite(self.tmpFile, img, (cv2.IMWRITE_PNG_COMPRESSION, 9))
            self.setIcon(QtGui.QIcon(self.tmpFile))
            self.setIconSize(QtCore.QSize(135, im.shape[0]))
            self.setFixedSize(QtCore.QSize(150, im.shape[0]))
            self.updateToolTip()

    def on_clickedButton(self):
        block = AbstractBlock(0, 0, self.__text, self.__dicTrans, self.__file, copy.deepcopy(self.__vars), self.hue, "",
                              self.__connections, self.__blockType, self.__type)
        self.__scene.addItem(copy.deepcopy(block))
        if self.__text == "main":
            self.setEnabled(False)

    def getAbstracBlockItem(self):
        return AbstractBlock(0, 0, self.__text, self.__dicTrans, self.__file, copy.deepcopy(self.__vars), self.hue, "",
                             self.__connections, self.__blockType, self.__type)

    def delete(self, row):
        self.__table.removeCellWidget(row, 0)
        self.__table.removeRow(row)
        self.__scene.removeByName(self.__text)
        del self

    def getText(self):
        return self.__text
