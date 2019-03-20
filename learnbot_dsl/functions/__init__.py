from __future__ import print_function, absolute_import

import os, sys, inspect, warnings
from importlib import import_module

ignore = [
    '__init__.py',
    'visual_auxiliary.py'
]

__path = os.path.dirname(os.path.realpath(__file__))
__localFunctionsPath = os.path.join(os.getenv('HOME'), ".learnblock", "functions")


def getFuntions():
    functions = {}
    dirnames = [__path, __localFunctionsPath]
    sys.path.append(__path)
    for dirname in dirnames:
        if not os.path.exists(dirname):
            continue
        for filename in os.listdir(dirname):
            fullname = os.path.join(dirname, filename)
            name, extension = os.path.splitext(filename)
            _type = os.path.basename(dirname)
            if dirname == __localFunctionsPath:
                _type = "basics"
            if (os.path.isfile(fullname) and extension != '.py') or filename in ignore:
                continue
            if os.path.isdir(fullname):
                dirnames.append(fullname)
                continue
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
