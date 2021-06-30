from __future__ import print_function, absolute_import

import os, sys, inspect, warnings
from importlib import import_module
from learnbot_dsl.Clients.Devices import __all__ as deviceList

ignore = [
    '__init__.py',
    'visual_auxiliary.py'
]
#Ruta de funciones del programa
__path = os.path.dirname(os.path.realpath(__file__))
#Ruta de funciones local
__localFunctionsPath = os.path.join(os.getenv('HOME'), ".learnblock", "functions")


def getFuntions():
    functions = {}
    #Posibles direcciones a buscar funciones
    dirnames = [__path, __localFunctionsPath]
    sys.path.append(__path)
    normDeviceList = [ x.lower() for x in deviceList ]
    for dirname in dirnames:
        #Si no esiste ruta continuamos con la siguiente
        if not os.path.exists(dirname):
            continue
        for filename in os.listdir(dirname):
            fullname = os.path.join(dirname, filename)
            #Desglosamos nombre de funcion y su extension
            name, extension = os.path.splitext(filename)
            #ignoramos los que no sean .py o esten en la lista de ignorados
            if (os.path.isfile(fullname) and extension != '.py') or filename in ignore:
                continue
            #Si encontramos una carpeta la añadimos para posterior busqueda
            if os.path.isdir(fullname):
                dirnames.append(fullname)
                continue
            #Comprobamos que la funcion tenga un Device, por nombre de la carpeta
            #si no sera basico
            if os.path.basename(dirname).lower() in normDeviceList:
                _type = os.path.basename(dirname)
            else:
                _type = "basics"
            sys.path.append(dirname)
            module_name = name
            try:
                func = getattr(import_module(module_name), name)
                # args = inspect.getargspec(func)
                functions[name] = dict(function=func, type=_type)
            except Exception as e:
                print("error", e, module_name, name, fullname)
    return functions


if __name__ == '__main__':
    function = getFuntions()
    for _ in map(print, function):
        pass
