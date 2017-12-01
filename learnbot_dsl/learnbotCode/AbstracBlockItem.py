from PySide import QtCore
from Block import *

class AbstractBlockItem():
    def __init__(self, x, y, nameFuntion, dicTrans, file, vars, connections=None, typeBlock=SIMPLEBLOCK, type=None, dict = None):
        self.pos = QtCore.QPointF(x, y)
        self.name = nameFuntion
        self.file = file
        self.vars = vars
        self.connections = []
        self.dicTrans = dicTrans
        if len(connections) > 0:
            if not isinstance(connections[0],Connection):
                for point, typeConnection in connections:
                    self.connections.append(Connection(point, self, typeConnection))
            else:
                for c in connections:
                    self.connections.append(c)
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
