from PySide import QtCore, QtGui
from VisualFuntion import *

class MyView(QtGui.QGraphicsView):
    def __init__(self,parent,arg=None):
        QtGui.QGraphicsView.__init__(self,parent)

