import inspect
import os
path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

from parserConfigBlock import *
__all__ = ["configBlocks"]

functions = parserConfigBlock(path+"/configFuntions")
functions += parserConfigBlock(path+"/configControl")
functions += parserConfigBlock(path+"/configPerceptual")
functions += parserConfigBlock(path+"/configPropiopercetive")
functions += parserConfigBlock(path+"/configOperators")

configBlocks = functions