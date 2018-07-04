#!/usr/bin/env python
# -*- coding: utf-8 -*-
import inspect
import os
path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

from blocks import pathBlocks

from parserConfigBlock import *
__all__ = ["pathImgBlocks","pathConfig","reload_functions"]
pathConfig = path
def reload_functions():
    global configBlocks
    functions = parserConfigBlock(path+"/configMotor")
    functions += parserConfigBlock(path+"/configOthers")
    functions += parserConfigBlock(path+"/configControl")
    functions += parserConfigBlock(path+"/configPerceptual")
    functions += parserConfigBlock(path+"/configPropriopercetive")
    functions += parserConfigBlock(path+"/configOperators")
    functions += parserConfigBlock(path+"/configExpressions")
    functions += parserConfigBlock(path+"/configCollab")
    for f in functions:
        for i in range( len( f.img ) ):
            f.img[i] = pathBlocks + "/" +f.img[i]

    return functions
pathImgBlocks = pathBlocks


