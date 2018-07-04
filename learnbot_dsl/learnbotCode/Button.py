#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from PySide import QtGui

from AbstractBlock import *
from Language import *


class Block_Button(QtGui.QPushButton):

    def __init__(self, args):
        if len(args) is 13:
            self.__parent, self.__text, self.__dicTrans, self.__view, self.__scene, self.__file, self.__connections, self.__vars, self.__blockType, self.__table, self.__row, self.__type, self.__dicToolTip = args
            self.tmpFile = "tmp/" + self.__text + str(self.__type) + str(self.__row) + ".png"

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
            self.tmpFile = "tmp/" + self.__text + str(self.__type) + str(self.__row) + ".png"

        QtGui.QPushButton.__init__(self)

        im = cv2.imread(self.__file, cv2.IMREAD_UNCHANGED)
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
            img = generateBlock(im, 34, self.showtext, self.__blockType, self.__connections, None, self.__type)
            cv2.imwrite(self.tmpFile, img, (cv2.IMWRITE_PNG_COMPRESSION, 9))
            self.setIcon(QtGui.QIcon(self.tmpFile))
            self.setIconSize(QtCore.QSize(135, im.shape[0]))
            self.setFixedSize(QtCore.QSize(150, im.shape[0]))
            self.updateToolTip()

    def on_clickedButton(self):
        block = AbstractBlock(0, 0, self.__text, self.__dicTrans, self.__file, copy.deepcopy(self.__vars), "",
                              self.__connections, self.__blockType, self.__type)
        self.__scene.addItem(copy.deepcopy(block))

    def getAbstracBlockItem(self):
        return AbstractBlock(0, 0, self.__text, self.__dicTrans, self.__file, copy.deepcopy(self.__vars), "",
                             self.__connections, self.__blockType, self.__type)

    def delete(self, row):
        self.__table.removeCellWidget(row, 0)
        self.__table.removeRow(row)
        self.__scene.removeByName(self.__text)
        del self

    def getText(self):
        return self.__text
