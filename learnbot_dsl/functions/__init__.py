from __future__ import print_function, absolute_import

import os, sys, inspect
from importlib import import_module
# import perceptual.back_obstacle

ignore = [
    '__init__.py',
    'visual_auxiliary.py'
]

__path = os.path.dirname(os.path.realpath(__file__))
def getFuntions():
	functions = {}
	params = {}
	paramsDefaults = {}
	dirnames = [__path, os.path.join(os.getenv('HOME'), ".learnblock", "functions")]
	sys.path.append(__path)
	for dirname in dirnames:
		if not os.path.exists(dirname):
			continue
		for filename in os.listdir(dirname):
			fullname = os.path.join(dirname, filename)
			name, extension = os.path.splitext(filename)
			if (os.path.isfile(fullname) and extension != '.py') or filename in ignore:
				continue
			if os.path.isdir(fullname):
				dirnames.append(fullname)
				continue
			sys.path.append(dirname)
			# module_name = dirname.replace('/','.') + '.' + name
			# module_name = module_name[module_name.rfind("learnbot_dsl"):]
			module_name = name
			try:
				func = getattr(import_module(module_name), name)
				args = inspect.getargspec(func)
				functions[name] = func
				params[name] = args.args[1:]
				paramsDefaults[name] = args.defaults
			except Exception as e:
				print("error", e, module_name, name)
	return functions

getFuntions()