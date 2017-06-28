import os
from subprocess import call
if call(["pyside-uic","-o","gui.py","interface.ui"]) is 1:
    print "Error al generar gui.py"
    exit(-1)

import gui,sys
from PySide import QtGui, QtCore

from Scene import *
from VisualFuntion import *
from View import *
from LearnBlock import *
import cv2



from pyparsing import Word, alphas, alphanums, nums, OneOrMore, CharsNotIn, Literal, Combine
from pyparsing import cppStyleComment, Optional, Suppress, ZeroOrMore, Group, StringEnd, srange
from pyparsing import nestedExpr, CaselessLiteral

semicolon = Suppress(Word(";"))
quote     = Suppress(Word("\""))
op        = Suppress(Word("{"))
cl        = Suppress(Word("}"))
opp       = Suppress(Word("("))
clp       = Suppress(Word(")"))

var = Word(alphas)
identifier = Word( alphas+"_", alphanums+"_" )
vars = Optional(var + ZeroOrMore(Suppress(Word(","))) + var)
Pfunctions = identifier.setResultsName('namefuntion') + opp + vars.setResultsName('vars') + clp

commIdentifier = Group(identifier.setResultsName('identifier'))

code = Group(Suppress(Word("code")) + op + ZeroOrMore(identifier) +cl)
f = Pfunctions+code
#print f.parseString(text)


if __name__ ==  "__main__":
    LearnBlock()