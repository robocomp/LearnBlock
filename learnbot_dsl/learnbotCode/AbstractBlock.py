#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Block import *


class AbstractBlock():

    def __init__(self, x, y, nameFunction, dicTrans, file, vars, hue, nameControl="", connections=None,
                 typeBlock=SIMPLEBLOCK, type=None, dicToolTip=None):
        self.pos = QtCore.QPointF(x, y)
        self.name = nameFunction
        self.file = file
        self.vars = vars
        self.connections = []
        self.dicTrans = dicTrans
        self.dicToolTip = dicToolTip
        self.nameControl = nameControl
        if len(connections) > 0:
            if not isinstance(connections[0], Connection):
                for point, typeConnection in connections:
                    self.connections.append(Connection(point, self, typeConnection))
            else:
                for c in connections:
                    self.connections.append(c)
        self.typeBlock = typeBlock
        self.type = type
        self.id = id
        self.hue = hue

    def setId(self, id):
        self.id = id

    def pos(self):
        return self.pos

    def setPos(self, pos):
        self.pos = pos

    def updateVars(self, vars):
        for index in range(len(vars)):
            self.vars[index].defaul = vars[index]

    def getVars(self):
        return self.vars
