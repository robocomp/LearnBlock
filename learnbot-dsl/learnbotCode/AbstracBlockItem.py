from PySide import QtCore



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

class AbstractBlockItem():
    def __init__(self, x, y, nameFuntion, file, vars, connections=None, typeBlock=SIMPLEBLOCK, type=None, dict = None):
        self.pos = QtCore.QPointF(x, y)
        self.name = nameFuntion
        self.file = file
        self.vars = vars
        self.connections = []
        for point, typeConnection in connections:
            self.connections.append(Connection(point, self, typeConnection))
        self.typeBlock = typeBlock
        self.type = type
        self.id = id

    def setId(self, id):
        self.id = id

    def pos(self):
        return self.pos

    def setPos(self,pos):
        self.pos = pos

    def updateVars(self,vars):
        for index in range(len(vars)):
            self.vars[index].defaul = vars[index]
