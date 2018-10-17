import inspect
import os
from subprocess import call

path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

for x in os.listdir(path):
    absPath = os.path.abspath(x)
    name, extension = os.path.splitext(absPath)
    if os.path.isfile(absPath) and extension == ".ui":
        if not os.path.exists(name + ".py") or os.path.getmtime(absPath) > os.path.getmtime(name + ".py"):
            if call(["pyside-uic", "-o", name + ".py", absPath]) is 1:
                print "Error al generar gui.py"
                exit(-1)
            else:
                print "pyside-uic", "-o", os.path.splitext(x)[-1] + ".py", x + "    successfully"

pathGuis=path
__all__ = ['guiAddVar', 'guiupdatedSuccessfully', 'guiGui', 'guiGuiCreateBlock', 'guiDelVar', 'guiCreateFunctions', 'guiAddNumberOrString', 'guiAddWhen', 'guiDelWhen', "pathGuis"]


import addVar as guiAddVar
import interface as guiGui
import createBlock as guiGuiCreateBlock
import delVar as guiDelVar
import createFunctions as guiCreateFunctions
import addNumberOrString as guiAddNumberOrString
import addWhen as guiAddWhen
import delWhen as guiDelWhen
import updatedSuccessfully as guiupdatedSuccessfully
