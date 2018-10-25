from __future__ import print_function, absolute_import
import inspect, os, sys
from subprocess import call
# import learnbot_dsl.guis.DelWhen as DelWhen
# import learnbot_dsl.guis.TabLibrary as TabLibrary
# import learnbot_dsl.guis.Learnblock as Learnblock
# import learnbot_dsl.guis.UpdatedSuccessfully as UpdatedSuccessfully
# import learnbot_dsl.guis.AddNumberOrString as AddNumberOrString
# import learnbot_dsl.guis.DelVar as DelVar
# import learnbot_dsl.guis.CreateFunctions as CreateFunctions
# import learnbot_dsl.guis.CreateBlock as CreateBlock
# import learnbot_dsl.guis.AddVar as AddVar
# import learnbot_dsl.guis.EditVar as EditVar
# import learnbot_dsl.guis.AddWhen as AddWhen

path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
# sys.path.append(path)
# __all__ = ['pathGuis',
#            'DelWhen',
#            'TabLibrary',
#            'Learnblock',
#            'UpdatedSuccessfully',
#            'AddNumberOrString',
#            'DelVar',
#            'CreateFunctions',
#            'CreateBlock',
#            'AddVar',
#            'EditVar.py',
#            'AddWhen'
#            ]

pathGuis = path

for x in os.listdir(path):
    out = x
    name, extension = os.path.splitext(os.path.abspath(out))
    absPath = os.path.abspath(x)
    if os.path.isfile(absPath) and extension == ".ui":
        if not os.path.exists(name + ".py") or os.path.getmtime(absPath) > os.path.getmtime(name + ".py"):
            if call(["pyside-uic", "-o", name + ".py", absPath]) is 1:
                print("Error al generar ", name)
                exit(-1)
            else:
                print("pyside-uic", "-o", os.path.splitext(x)[-1] + ".py", x + "    successfully")

# import learnbot_dsl.guis.DelWhen as DelWhen
# import learnbot_dsl.guis.TabLibrary as TabLibrary
# import learnbot_dsl.guis.Learnblock as Learnblock
# import learnbot_dsl.guis.UpdatedSuccessfully as UpdatedSuccessfully
# import learnbot_dsl.guis.AddNumberOrString as AddNumberOrString
# import learnbot_dsl.guis.DelVar as DelVar
# import learnbot_dsl.guis.CreateFunctions as CreateFunctions
# import learnbot_dsl.guis.CreateBlock as CreateBlock
# import learnbot_dsl.guis.AddVar as AddVar
# import learnbot_dsl.guis.EditVar as EditVar
# import learnbot_dsl.guis.AddWhen as AddWhen