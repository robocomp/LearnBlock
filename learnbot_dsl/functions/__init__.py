
import os
import inspect
from importlib import import_module
import perceptual.back_obstacle

ignore = [
    '__init__.py',
    'visual_auxiliary.py'
]

__path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

functions = {}
params = {}
paramsDefaults = {}
dirnames = [__path]

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
		module_name = module_name[module_name.find("learnbot_dsl"):]
		func = getattr(import_module(module_name), name)
		args = inspect.getargspec(func)
		functions[name] = func
		params[name] = args.args[1:]
		paramsDefaults[name] = args.defaults



