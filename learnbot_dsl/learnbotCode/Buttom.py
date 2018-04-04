from PySide import QtGui, QtCore
import cv2, os
from Language import *
from Block import *
from AbstracBlockItem import *


class MyButtom(QtGui.QPushButton):

    def __init__(self,args):
        if len(args) is 11:
            self.__text, self.__dicTrans, self.__view, self.__scene, self.__file, self.__connections, self.__vars, self.__blockType, self.__table, self.__row, self.__type = args
            self.tmpFile = "tmp/" + self.__text + str(self.__type) + str(self.__row) + ".png"

        elif len(args) is 5:
            abstracBlockItem, self.__view, self.__scene, self.__table, self.__row = args
            self.__text = abstracBlockItem.name
            self.__dicTrans = abstracBlockItem.dicTrans
            self.__file = abstracBlockItem.file
            self.__connections = abstracBlockItem.connections
            self.__vars = abstracBlockItem.vars
            self.__blockType = abstracBlockItem.typeBlock
            self.__type = abstracBlockItem.type
            self.tmpFile = "tmp/" + self.__text + str(self.__type) + str(self.__row) + ".png"

        QtGui.QPushButton.__init__(self)
        im = cv2.imread(self.__file, cv2.IMREAD_UNCHANGED)
        self.showtext = self.__text
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updateImg)

        if len( self.__dicTrans ) is not 0:
            self.showtext = self.__dicTrans[ getLanguage() ]
            self.timer.start(10)
        var=[x.name for x in self.__vars]
        img = generateBlock(im, 34, self.showtext, self.__blockType, self.__connections, var, self.__type)
        cv2.imwrite(self.tmpFile, img, (cv2.IMWRITE_PNG_COMPRESSION, 9))
        self.setIcon(QtGui.QIcon(self.tmpFile))
        self.setIconSize(QtCore.QSize(135, im.shape[0]))
        self.setFixedSize(QtCore.QSize(150, im.shape[0]))
        self.__table.setRowHeight(self.__row, im.shape[0])
        self.clicked.connect(self.clickedButton)
        self.__item = self.__table.item(self.__row,0)


    def removeTmpFile(self):
        try:
            os.remove(self.tmpFile)
        except Exception as e:
            print e

    def updateImg(self):
        if len( self.__dicTrans ) is not 0 and self.showtext is not self.__dicTrans[ getLanguage() ]:
            self.showtext = self.__dicTrans[ getLanguage() ]
            im = cv2.imread(self.__file, cv2.IMREAD_UNCHANGED)
            img = generateBlock(im, 34, self.showtext, self.__blockType, self.__connections, None, self.__type)
            cv2.imwrite(self.tmpFile, img, (cv2.IMWRITE_PNG_COMPRESSION, 9))
            self.setIcon(QtGui.QIcon(self.tmpFile))
            self.setIconSize(QtCore.QSize(135, im.shape[0]))
            self.setFixedSize(QtCore.QSize(150, im.shape[0]))

    def clickedButton(self):
        block = AbstractBlockItem(0, 0, self.__text, self.__dicTrans, self.__file, copy.deepcopy(self.__vars), "", self.__connections,self.__blockType,self.__type)
        self.__scene.addItem(block)

    def getAbstracBlockItem(self):
        return AbstractBlockItem(0,0,self.__text, self.__dicTrans, self.__file, copy.deepcopy(self.__vars), "", self.__connections, self.__blockType,self.__type)

    def delete(self,row):
        self.__table.removeCellWidget(row,0)
        self.__table.removeRow(row)
        self.__scene.removeByName(self.__text)
        del self

    def getText(self):
        return self.__text
