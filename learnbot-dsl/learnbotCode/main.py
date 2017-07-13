import os
from subprocess import call
print os.getcwd()


from LearnBlock import *

from pyparsing import Word, alphas, alphanums
from pyparsing import Optional, Suppress, ZeroOrMore, Group

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