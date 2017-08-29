import numpy as np
import copy
import cv2
import PySide.QtCore

TOP = 0
BOTTOM = 1
BOTTOMIN = -1
RIGHT = 3
LEFT = 4

SIMPLEBLOCK = 1
COMPLEXBLOCK = 2

OPERATOR = 0
CONTROL = 1
FUNTION = 2
VARIABLE = 3
USERFUNCTION = 4


class Connection:

    def __init__(self, point, parent, type,):
        self.__parent = parent
        self.__connect = None
        self.__point = point
        self.__idItem = None
        self.__type = type

    def setType(self,type):
        self.__type = type
    def setItem(self,id):
        self.__idItem = id
    def setPoint(self,point):
        self.__point = point
    def setConnect(self,connect):
        self.__connect=connect
    def setParent(self,parent):
        self.__parent = parent

    def getType(self):
        return self.__type
    def getIdItem(self):
        return self.__idItem
    def getPosPoint(self):
        return self.__point + self.__parent.pos
    def getPoint(self):
        return self.__point
    def getConnect(self):
        return self.__connect
    def getParent(self):
        return self.__parent
    def __del__(self):
        del self.__parent
        del self.__connect
        del self.__point
        del self.__item
        del self.__type


class Variable():
    def __init__(self,type,name,defaul):
        self.type = type
        self.name = name
        self.defaul = defaul

class Block():
    def __init__(self,name,funtionType,listVar = None,file = None):
        self.listImg=[]
        self.name = name
        self.funtionType = funtionType
        self.listVar = listVar
        self.file = file

def generateBlock(img, x, name, typeBlock, connections=None, vars=None, type=None):
    im = None
    sizeleter = 13
    varText = ""
    if type in [FUNTION, USERFUNCTION]:
        varText = "("
        if vars is not None:
            for var in vars:
                varText += var + ","
            varText = varText[:-1] + ")"
        else:
            varText = "()"
    elif type is VARIABLE:
        if vars is not None:
            for var in vars:
                varText =  " set to " + var
    if typeBlock is COMPLEXBLOCK:
        if vars is None:
            varText = ""
        left = img[0:img.shape[0], 0:60]
        right = img[0:img.shape[0], img.shape[1] - 10:img.shape[1]]
        line = img[0:img.shape[0], 72:73]
        h = left.shape[0]
        textSize = ((len(name)+len(varText)) * sizeleter)
        if textSize is 0:
            textSize = 22
        w = left.shape[1] + right.shape[1] + textSize - 22
        im = np.ones((h, w, 4), dtype=np.uint8)
        im[0:h, 0:left.shape[1]] = copy.copy(left)
        im[0:right.shape[0], im.shape[1] - right.shape[1]:im.shape[1]] = copy.copy(right)
        for i in range(left.shape[1], im.shape[1] - right.shape[1]):
            im[0:line.shape[0], i:i + 1] = copy.copy(line)

        header = copy.copy(im[0:39, 0:im.shape[1]])
        foot = copy.copy(im[69:104, 0:im.shape[1]])
        line = copy.copy(im[50:51, 0:im.shape[1]])
        im = np.ones((header.shape[0] + foot.shape[0] + x - 4, header.shape[1], 4), dtype=np.uint8)
        im[0:header.shape[0], 0:header.shape[1]] = header
        im[im.shape[0] - foot.shape[0]:im.shape[0], 0:foot.shape[1]] = foot
        for i in range(39, im.shape[0] - foot.shape[0]):
            im[i:i + line.shape[0], 0:header.shape[1]] = copy.copy(line[::,:header.shape[1]])
    else:
        left = img[0:img.shape[0], 0:43]
        right = img[0:img.shape[0], img.shape[1] - 10:img.shape[1]]
        line = img[0:img.shape[0], 43:44]
        im = np.ones((left.shape[0], left.shape[1] + right.shape[1] + ((len(name)+len(varText)) * sizeleter) , 4), dtype=np.uint8)
        im[0:left.shape[0], 0:left.shape[1]] = copy.copy(left)
        im[0:right.shape[0], im.shape[1] - right.shape[1]:im.shape[1]] = copy.copy(right)
        for i in range(left.shape[1], im.shape[1] - right.shape[1]):
            im[0:line.shape[0], i:i + 1] = copy.copy(line)
    cv2.putText(im, name+varText, (10, 27), cv2.FONT_HERSHEY_TRIPLEX, 0.75, (0, 0, 0, 255), 1,25)
    if connections is not None and len(connections) > 0:
        if not isinstance(connections[0],Connection):
            for point, t in connections:
                if t is RIGHT:
                    point.setX(im.shape[1]-5)
        else:
            for c in connections:
                if c.getType() is RIGHT:
                    c.getPoint().setX(im.shape[1] - 5)
    return im

