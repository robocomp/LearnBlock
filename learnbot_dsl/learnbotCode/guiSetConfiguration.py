import guis.setConfiguration as setConfig
from VisualFuntion import *
import os
from blocksConfig import pathBlocks, pathConfig
listBlock = []
listNameBlocks = []
import cv2

class guiSetConfiguration(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.ui = setConfig.Ui_Dialog()
        self.ui.setupUi(self)
	

