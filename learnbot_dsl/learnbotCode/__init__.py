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

if call(["pyside-uic","-o",path+"/delVar.py",path+"/delVar.ui"]) is 1:
    print "Error al generar delVar.py"
    exit(-1)
if call(["pyside-uic","-o",path+"/createFunctions.py",path+"/createFunctions.ui"]) is 1:
    print "Error al generar createFunctions.py"
    exit(-1)
if call(["pyside-uic","-o",path+"/addNumberOrString.py",path+"/addNumberOrString.ui"]) is 1:
    print "Error al generar addNumberOrString.py"
    exit(-1)
if call(["pyside-uic","-o",path+"/addWhen.py",path+"/addWhen.ui"]) is 1:
    print "Error al generar addWhen.py"
    exit(-1)
if call(["pyside-uic","-o",path+"/delWhen.py",path+"/delWhen.ui"]) is 1:
    print "Error al generar addWhen.py"
    exit(-1)
__all__ = ['guiAddVar', 'guiGui', 'guiGuiCreateBlock', 'guiDelVar', 'guiCreateFunctions', 'guiAddNumberOrString', 'guiAddWhen', 'guiDelWhen', 'guiTab']


import addVar as guiAddVar
import gui as guiGui
import createBlock as guiGuiCreateBlock
import delVar as guiDelVar
import createFunctions as guiCreateFunctions
import addNumberOrString as guiAddNumberOrString
import addWhen as guiAddWhen
import delWhen as guiDelWhen
import tab as guitab
#
# guiAddVar = addVar
# guiGui = gui
# guiGuiCreateBlock = createBlock
# guiNewVar = newVar
# guiDelVar = delVar
# guiCreateFunctions = createFunctions
# guiAddNumberOrString = addNumberOrString
# guiAddWhen = addWhen
