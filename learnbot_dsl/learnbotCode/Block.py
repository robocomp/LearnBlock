from __future__ import print_function, absolute_import
import copy
from PySide6 import QtCore

import cv2
import numpy as np

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
WHEN = 5
LIBRARY = 6


class Connection:

    def __init__(self, point, parent, type, ):
        self.__parent = parent
        self.__connect = None
        self.__point = point
        self.__idItem = None
        self.__type = type

    def __str__(self):
        text = "Connection: \n" \
               "\tid item : " + str(self.__parent.id) + "\n" \
               "\tid item connected : " + str(self.__idItem) + "\n" \
               "\ttype : " + ["top", "bottom", "", "right", "left", "bottomin"][self.__type] + "\n" \
               "\tposition = " + str(self.__point)
        return text

    def setType(self, type):
        self.__type = type

    def setItem(self, id):
        self.__idItem = id

    def setPoint(self, point):
        self.__point = point

    def setConnect(self, connect):
        self.__connect = connect

    def setParent(self, parent):
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
        del self.__type


class Variable:
    translate = {}
    values = []
    translateValues = {}
    def __init__(self, type=None, name=None, default=None, translate={}, dict=None):
        if dict is not None:
            self.type = dict["type"]
            self.name = dict["name"]
            self.defaul = dict["default"]
            if self.type == "list":
                print("entro")
                self.values = dict["values"]
                self.translateValues = dict["translateValues"]
            if "translate" in dict:
                self.translate = dict["translate"]
        else:
            self.type = type
            self.name = name
            self.defaul = default
            self.translate = translate
    def __str__(self):
        return "type      = " + self.type + "\n" \
               "name      = " + self.name + "\n"\
               "default   = " + self.defaul + "\n" \
               "translate = " + str(self.translate) + "\n"

def generateBlock(img, x, name, typeBlock, connections=None, vars_=None, type_=None, nameControl=""):
    im = None
    sizeleter = 15
    varText = ""
    if not isinstance(vars_, list):
        vars_ = []
    if type_ in [FUNTION, USERFUNCTION, LIBRARY] or (type_ is CONTROL and len(vars_) != 0):
        varText = "(" + ", ".join(vars_) + ")"
    elif type_ == VARIABLE:
        if len(vars_) != 0:
            for var in vars_:
                varText = str(var)
                break
    text = name + varText

    textSize = (len(text) * sizeleter)
    if textSize == 0:
        textSize = 22
    nameControlSize = (len(nameControl) * sizeleter)


    if typeBlock == COMPLEXBLOCK:
        left = img[0:img.shape[0], 0:60]
        right = img[0:img.shape[0], img.shape[1] - 10:img.shape[1]]
        line = img[0:img.shape[0], 72:73]
        h = left.shape[0]
        textSize = max([textSize, nameControlSize])
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
            im[i:i + line.shape[0], 0:header.shape[1]] = copy.copy(line[::, :header.shape[1]])
    else:
        left = img[0:img.shape[0], 0:43]
        right = img[0:img.shape[0], img.shape[1] - 10:img.shape[1]]
        line = img[0:img.shape[0], 43:44]
        im = np.ones((left.shape[0], left.shape[1] + right.shape[1] + textSize, 4),
                     dtype=np.uint8)
        im[0:left.shape[0], 0:left.shape[1]] = copy.copy(left)
        im[0:right.shape[0], im.shape[1] - right.shape[1]:im.shape[1]] = copy.copy(right)
        for i in range(left.shape[1], im.shape[1] - right.shape[1]):
            im[0:line.shape[0], i:i + 1] = copy.copy(line)


    cv2.putText(im, text, (10, 27), cv2.FONT_HERSHEY_TRIPLEX, 0.75, (0, 0, 0, 255), 2, 25)
    cv2.putText(im, nameControl, (10, im.shape[0] - 10), cv2.FONT_HERSHEY_TRIPLEX, 0.75, (0, 0, 0, 255), 2, 25)

    if connections is not None and len(connections) > 0:
        if not isinstance(connections[0], Connection):
            for point, t in connections:
                if t == RIGHT:
                    point.setX(im.shape[1] - 5)
        else:
            for c in connections:
                if c.getType() == RIGHT:
                    c.getPoint().setX(im.shape[1] - 5)
    return im

def generate_error_block(img):
    img_border = cv2.copyMakeBorder(img, 10, 10, 10, 10, cv2.BORDER_CONSTANT, None, (0,0,0,0))
    a = img_border[:,:,3]
    kernel = np.ones((15, 15), np.uint8)
    a2 = cv2.erode(a, kernel, iterations=1)
    mask = cv2.blur(a-a2,(7,7))
    mask = mask[10:-10,10:-10]
    other_c = np.zeros_like(mask, np.uint8)
    result_img = np.dstack((other_c, other_c, mask))
    img_error = cv2.addWeighted(img[:,:,0:3], 1, result_img, 1, 0)
    img_error = np.concatenate((img_error, np.expand_dims(img[:,:,3],axis=-1)), axis=2)
    return img_error

def loadConfigBlock(img):
    fh = open(img, "r")
    text = fh.readlines()
    fh.close()
    connections = []
    blockType = None
    for line in text:
        if "type" in line:
            line = line.replace("\n", "")
            line = line.split(" ")
            blockType = line[1]
            if "simple" in blockType:
                blockType = SIMPLEBLOCK
            elif "complex" in blockType:
                blockType = COMPLEXBLOCK
        else:
            line = line.replace("\n", "")
            line = line.replace(" ", "")
            c = line.split(",")
            type = None
            if "TOP" in c[2]:
                type = TOP
            elif "BOTTOMIN" in c[2]:
                type = BOTTOMIN
            elif "BOTTOM" in c[2]:
                type = BOTTOM
            elif "RIGHT" in c[2]:
                type = RIGHT
            elif "LEFT" in c[2]:
                type = LEFT
            connections.append((QtCore.QPointF(int(c[0]), int(c[1])), type))
    return blockType, connections


if __name__ == '__main__':
    img = cv2.imread("/home/ivan/robocomp/components/LearnBlock/learnbot_dsl/blocksConfig/blocks/block7.png", -1)
    img_error = generate_error_block(img)
    cv2.imshow("img_error", img_error)
    cv2.waitKey(0)