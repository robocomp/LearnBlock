import inspect
import os
path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

from blocks import pathBlocks

from parserConfigBlock import *
__all__ = ["pathImgBlocks","pathConfig","reload_functions"]
pathConfig = path
def reload_functions():
    global configBlocks
    functions = parserConfigBlock(path+"/configMotor_es")
    functions += parserConfigBlock(path+"/configControl")
    functions += parserConfigBlock(path+"/configPerceptual_es")
    functions += parserConfigBlock(path+"/configPropriopercetive")
    functions += parserConfigBlock(path+"/configOperators")

    for f in functions:
        for i in range(len(f[1]["img"])):
            f[1]["img"][i] = pathBlocks + "/" +f[1]["img"][i]
    return functions
pathImgBlocks = pathBlocks


