import inspect
import os
from subprocess import call

path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

for x in os.listdir(path):
    if os.path.isfile(path + "/" + x) and x.endswith(".ui"):
        if not os.path.exists(path + "/" + x.replace(".ui", ".py")) or os.path.getmtime(path + "/" + x) > os.path.getmtime(path + "/" + x.replace(".ui", ".py")):
            if call(["pyside-uic", "-o", path + "/" + x.replace(".ui", ".py"), path + "/" + x]) is 1:
                print "Error al generar gui.py"
                exit(-1)
            else:
                print "pyside-uic", "-o", x.replace(".ui", ".py"), x + "    successfully"


__all__ = ['guiAddVar', 'guiupdatedSuccessfully', 'guiGui', 'guiGuiCreateBlock', 'guiDelVar', 'guiCreateFunctions', 'guiAddNumberOrString', 'guiAddWhen', 'guiDelWhen']


import addVar as guiAddVar
import interface as guiGui
import createBlock as guiGuiCreateBlock
import delVar as guiDelVar
import createFunctions as guiCreateFunctions
import addNumberOrString as guiAddNumberOrString
import addWhen as guiAddWhen
import delWhen as guiDelWhen
import updatedSuccessfully as guiupdatedSuccessfully
