from __future__ import print_function, absolute_import
import os, sys
from subprocess import call
path = os.path.dirname(os.path.realpath(__file__))
pathGuis = path

if __name__ == '__main__':
    for x in os.listdir(path):
        out = x
        name, extension = os.path.splitext(os.path.abspath(out))
        absPath = os.path.abspath(x)
        if os.path.isfile(absPath) and extension == ".ui":
            if not os.path.exists(name + ".py") or os.path.getmtime(absPath) > os.path.getmtime(name + ".py"):
                if call(["pyside2-uic", "-o", name + ".py", absPath]) is 1:
                    print("Error al generar ", name)
                    exit(-1)
                else:
                    print("pyside2-uic", "-o", os.path.splitext(x)[-1] + ".py", x + "    successfully")

