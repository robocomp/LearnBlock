import os
from importlib import import_module

ignore = [
    '__init__.py',
]

functions = {}

for filename in os.listdir('functions'):
    fullname = os.path.join('functions', filename)
    if os.path.isdir(fullname) or filename in ignore:
        continue

    name = os.path.splitext(filename)[0]
    module_name = 'functions.' + name

    func = getattr(import_module(module_name), name)
    functions[name] = func

