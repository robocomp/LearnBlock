import inspect
import os
from subprocess import call


path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

if call(["pyside-uic","-o",path+"/gui.py",path+"/interface.ui"]) is 1:
    print "Error al generar gui.py"
    exit(-1)
if call(["pyside-uic","-o",path+"/var.py",path+"/var.ui"]) is 1:
    print "Error al generar var.py"
    exit(-1)

if call(["pyside-uic","-o",path+"/createBlock.py",path+"/createBlock.ui"]) is 1:
    print "Error al generar var.py"
    exit(-1)

if call(["pyside-uic","-o",path+"/addVar.py",path+"/addVar.ui"]) is 1:
    print "Error al generar var.py"
    exit(-1)
__all__ = ['guiAddVar','guiGui','guiGuiCreateBlock','guiNewVar']


import addVar
import gui
import createBlock
import newVar

guiAddVar = addVar
guiGui = gui
guiGuiCreateBlock = createBlock
guiNewVar = newVar