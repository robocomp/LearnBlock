import os
import inspect
from importlib import import_module

ignore = [
    '__init__.py'
]

functions = {}
params = {}
paramsDefaults = {}
dirnames = ['functions']

for dirname in dirnames:
	for filename in os.listdir(dirname):
		fullname = os.path.join(dirname, filename)
		if filename.find('.pyc')>0 or filename in ignore:
			continue
		if os.path.isdir(fullname):
			dirnames.append(fullname)
			continue

		name = os.path.splitext(filename)[0]
		module_name = dirname.replace('/','.') + '.' + name

		func = getattr(import_module(module_name), name)
		args = inspect.getargspec(func)
		functions[name] = func
		params[name] = args.args[1:]
		paramsDefaults[name] = args.defaults

