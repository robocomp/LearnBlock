#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import

import sys
from pyparsing import *

HEADER = """
#EXECUTION: python code_example.py config
from __future__ import print_function, absolute_import
from learnbot_dsl.functions import getFuntions
functions = getFuntions()
import learnbot_dsl.<LearnBotClient> as <LearnBotClient>
import sys, time, os
global lbot

try:
    lbot = <LearnBotClient>.Client(sys.argv)
except Exception as e:
    print("hay un Error")
    print(e)
    raise(e)

"""


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


OBRACE, CBRACE, SEMI, OPAR, CPAR = map(Literal, "{};()")

reserved_words = (Keyword('def') | Keyword('=') | Keyword('function') | Keyword('>=') | Keyword('<=') | Keyword(
    '<') | Keyword('>') | Keyword('deactivate') | Keyword('activate') | Keyword('not') | Keyword('True') | Keyword(
    'False') | Keyword('or') | Keyword('and') | Keyword('main') | Keyword('if') | Keyword('else') | Keyword(
    'elif') | Keyword('when') | Keyword('while') | Keyword('end'))
iden = Word(alphanums + "_")
identifier = Group(~reserved_words + iden).setResultsName("IDENTIFIER")

QUOTE = Literal("\"")
OR = Literal("or")
AND = Literal("and")
NOT = Group(Literal("not")).setResultsName('NOT')
plus = Literal("+")
minus = Literal("-")
mult = Literal("*")
div = Literal("/")
lpar = Literal("(")
rpar = Literal(")")
TRUE = Group(Literal("True")).setResultsName('TRUE')
FALSE = Group(Literal("False")).setResultsName('FALSE')
NONE = Group(Literal("None")).setResultsName('NONE')
eq = Literal("=")
point = Literal('.')
coma = Literal(",")
COLONS = Suppress(Literal(":"))
SEMICOL = Literal(";")
plusorminus = Literal('+') | Literal('-')
e = CaselessLiteral('E')
number = Word(nums)
integer = Combine(Optional(plusorminus) + number)
NUMS = Group(Combine(integer + Optional(point + Optional(number)) + Optional(e + integer))).setResultsName("NUMBER")

L = Literal("<")
NL = Literal(">")
LE = Literal("<=")
NLE = Literal(">=")
E = Literal("==")
NE = Literal("!=")
END = Literal("end")
SECTAB = ZeroOrMore("\t")
CHAINBETTENQUOTE = Group(QuotedString('"')).setResultsName("STRING")

"""-----------------COMPARACIONES-------------------"""
COMP = Group(L | NL | LE | NLE | E | NE).setResultsName("COMP")

"""-----------------OPERADORES----------------------"""
SRMD = Group(plus | minus | mult | div).setResultsName("SRMD")

"""-----------------FUNCTION-------------------------"""
FUNCTION = Group(
    Suppress(Literal("function")) + Suppress(point) + identifier.setResultsName('name') + Suppress(lpar) + Group(
        Optional(NUMS | identifier) + ZeroOrMore(Suppress(coma) + (NUMS | identifier))).setResultsName(
        "args") + Suppress(rpar)).setResultsName("FUNCTION")

"""-----------------FIELDS---------------------------"""
FIELDS = Optional(NOT) + NUMS | FUNCTION | TRUE | FALSE | identifier | CHAINBETTENQUOTE

"""-----------------OPERACIONES---------------------"""
ORAND = Group(OR | AND).setResultsName('ORAND')

"""-----------------OPERACIONES---------------------"""
OPERATION = Group(FIELDS + ZeroOrMore( (SRMD | ORAND) + FIELDS)).setResultsName("OPERATION")

"""-----------------SIMPLEFUNCTION-------------------------"""
SIMPLEFUNCTION = Group(identifier.setResultsName('name') + Suppress(lpar) + Group(
    Optional(NUMS | identifier) + ZeroOrMore(Suppress(coma) + (NUMS | identifier))).setResultsName("args") + Suppress(
    rpar)).setResultsName("SIMPLEFUNCTION")

"""-----------------PASS-------------------------"""
PASS = Group(Literal("pass")).setResultsName("PASS")

"""-----------------CONDICIONES---------------------"""
COMPOP = Group(OPERATION + COMP + OPERATION).setResultsName("COMPOP")
OPTIONCONDITION = FUNCTION | SIMPLEFUNCTION | TRUE | FALSE | COMPOP | identifier
SIMPLECONDITION = Group(Optional(NOT) + OPTIONCONDITION).setResultsName("SIMPLECONDITION")
CONDITION = Group(SIMPLECONDITION + ZeroOrMore(( ORAND | SRMD ) + SIMPLECONDITION)).setResultsName("CONDITION")

"""-----------------asignacion-VARIABLES------------"""

ASSIGSTRING = Group((CHAINBETTENQUOTE | NUMS) + ZeroOrMore(SRMD + (CHAINBETTENQUOTE | NUMS))).setResultsName(
    'ASSIGSTRING')

NONEVAR = NONE.setResultsName("NONEVAR")
VAR = Group(SECTAB + identifier.setResultsName("name") + Suppress(eq) + ( NONEVAR | OPERATION )).setResultsName("VAR")
# TODO +=
# Solved error var =  0

"""-----------------LINEA---------------------------"""
LINE = Forward()
LINES = Group(LINE + ZeroOrMore(LINE)).setResultsName('LINES')

"""-----------------bloque-IF-----------------------"""
ELSE = Forward()
ELSEIF = Forward()
INIF = LINES & (ZeroOrMore(ELSEIF) + Optional(ELSE))

ELSEIF << Group(
    SECTAB + Suppress(Literal("elif")) + Group(CONDITION).setResultsName('condition') + COLONS + LINES.setResultsName(
        'content')).setResultsName("ELIF")
ELSE << Group(SECTAB + Suppress(Literal("else")) + COLONS + LINES.setResultsName('content')).setResultsName("ELSE")
IF = Group(
    SECTAB + Suppress(Literal("if")) + Group(CONDITION).setResultsName('condition') + COLONS + LINES.setResultsName(
        'content') + Group(ZeroOrMore(ELSEIF) + Optional(ELSE)).setResultsName("OPTIONAL") + Suppress(
        END)).setResultsName("IF")

"""-----------------LOOP----------------------------"""
BLOQUEWHILE = Group(
    SECTAB + Suppress(Literal("while")) + Group(CONDITION).setResultsName('condition') + COLONS + LINES.setResultsName(
        'content') + Suppress(Literal("end"))).setResultsName("WHILE")

"""-----------------WHEN+CONDICION------------------"""
BLOQUEWHENCOND = Group(SECTAB + Suppress(Literal("when")) + identifier.setResultsName("name") + Optional(
    Suppress(eq) + Group(CONDITION).setResultsName('condition')) + COLONS + LINES.setResultsName('content') + Literal(
    "end")).setResultsName("WHEN")

"""-----------------ACTIVATE-CONDITION----------------"""
ACTIVATE = Group(Suppress(Literal("activate")) + identifier.setResultsName("name")).setResultsName("ACTIVATE")
DEACTIVATE = Group(Suppress(Literal("deactivate")) + identifier.setResultsName("name")).setResultsName("DEACTIVATE")

"""-----------------LINEA---------------------------"""
LINE << (SIMPLEFUNCTION | FUNCTION | IF | BLOQUEWHILE | VAR | ACTIVATE | DEACTIVATE | PASS)

"""-----------------DEF----------------------------"""
DEF = Group(Suppress(Literal("def ")) + identifier.setResultsName("name") + Suppress(lpar) + Suppress(
    rpar) + COLONS + LINES.setResultsName('content') + Suppress(Literal("end"))).setResultsName("DEF")

"""-----------------IMPORT----------------------------"""
IMPORT = Group(Suppress(Literal("import")) + QuotedString('"')).setResultsName("IMPORT")

"""-----------------MAIN----------------------------"""
MAIN = Group(Suppress(Literal("main")) + COLONS + LINES.setResultsName('content')).setResultsName("MAIN") + Suppress(
    Literal("end"))
LB = ZeroOrMore(IMPORT) + ZeroOrMore(LINES) + ZeroOrMore(DEF) + (MAIN | ZeroOrMore(BLOQUEWHENCOND))
LB.ignore(pythonStyleComment)

ini = []

def __parserFromFile(file):
    with open(file) as f:
        text = f.read()
        ret = __parserFromString(text)
        return ret


def __parserFromString(text):
    global ini
    ini = []
    try:
        LB.ignore(pythonStyleComment)
        ret = LB.parseString(text)
        return ret
    except ParseException as pe:
        print(pe.line)
        print(' ' * (pe.col - 1) + '^')
        print(pe)


def __generatePy(lines):
    list_var = []
    text = ""
    imports = None
    thereareWhens = False
    for x in lines:
        if x.getName() is 'WHEN':
            thereareWhens = True
            list_var.append("time_" + str(x.name[0]))
            list_var.append(str(x.name[0]) + "_start")
            list_var.append(x.name[0])
        elif x.getName() is 'VAR':
            list_var.append(x.name[0])
        elif x.getName() is 'IMPORT':
            if imports is None:
                imports = "imports = ["
            imports += '"' + x[0] + '", '
    if imports is not None:
        imports = imports[:-2] + "]"
        text += "\n" + imports + """
for f in imports:
    for subPath in [os.path.join(f, x) for x in os.listdir(f)]:
        if os.path.isdir(os.path.abspath(subPath)):
            for subsubPath in [os.path.join(subPath, x) for x in os.listdir(subPath)]:
                if os.path.basename(subsubPath) == os.path.basename(os.path.dirname(subsubPath)) + ".py":
                    # execfile(os.path.abspath(subsubPath), globals())
                    exec(open(os.path.abspath(subsubPath)).read())
"""
    global ini
    for x in lines:
        x.getName()
        if x.getName() is "MAIN" and thereareWhens:
            continue
        if x.getName() is "LINES":
            for y in x:
                print(y.getName())
                text = __process(y, list_var, text)
        else:
            text = __process(x, list_var, text)

    if thereareWhens is True:
        print(thereareWhens)
        for x in lines:
            if x.getName() is 'WHEN':
                if x.name[0] == "start":
                    text += "when_" + str(x.name[0]) + "()\n"
        text += "\n\nwhile True:\n"
        for line in ini:
            text += "\t" + line
        for x in lines:
            if x.getName() is 'WHEN':
                if x.name[0] != "start":
                    text += "\twhen_" + str(x.name[0]) + "()\n"
        text += "\tpass"
    return text


def __process(line, list_var=[], text="", index=0):
    TYPE = line.getName()

    if TYPE is 'MAIN':
        for cLine in line.content:
            text += __process(cLine, [], "", 0) + "\n"
    elif TYPE is 'DEF':
        text = __processDEF(line, list_var, text, 1)
    elif TYPE is 'WHEN':
        text = __processWHEN(line, list_var, text)
    elif TYPE is 'WHILE':
        text = __processWHILE(line, text, index)
    elif TYPE is 'IF':
        text = __processIF(line, text, index)
    elif TYPE is 'ELIF':
        text = __processELIF(line, text, index)
    elif TYPE is 'ELSE':
        text = __processELSE(line, text, index)
    elif TYPE is 'ACTIVATE':
        text = __processACTIVATE(line, text, index)
    elif TYPE is 'DEACTIVATE':
        text = __processDEACTIVATE(line, text, index)
    elif TYPE is 'VAR':
        text = __processASSIG(line, text, index)
    elif TYPE is 'OPERATION':
        text = __processOP(line, text, index)
    elif TYPE is 'FUNCTION':
        text = __processFUNCTION(line, text, index)
    elif TYPE is 'SIMPLEFUNCTION':
        text = __processSIMPLEFUNCTION(line, text, index)
    elif TYPE is 'CONDITION':
        text = __processCONDITION(line, text, index)
    elif TYPE is 'ASSIGSTRING':
        text = __processASSIGSTRING(line, text, index)
    elif TYPE is 'SIMPLECONDITION':
        text = __processSIMPLECONDITION(line, text, index)
    elif TYPE is 'PASS':
        text += "\t" * index + "pass\n"
    elif TYPE is 'NONEVAR':
        text += "None"
    elif TYPE is 'STRING':
        text += '"' + line[0] + '"'
    elif TYPE in ['FALSE', 'TRUE', 'IDENTIFIER', 'SRMD', 'ORAND', "NUMBER"]:
        text = line[0]
    else:
        print("The type is ", TYPE , line)
    return text

def __processDEF(line, list_var, text="", index=0):
    text += "\ndef " + line.name[0] + "():\n"
    for x in list_var:
        text += "\t" * index + "global " + x + "\n"
    for field in line.content:
        text = __process(field, [], text, index) + "\n\n"
    return text


def __processFUNCTION(line, text="", index=0):
    if text is not "":
        text += "\t" * index
    text += "functions.get(\"" + line.name[0] + "\")(lbot"
    for x in line.args:
        text += ", " + x[0]
    text += ")"
    return text


def __processSIMPLEFUNCTION(line, text="", index=0):
    if text is not "":
        text += "\t" * index
    text += line.name[0] + "("
    if len(line.args) is not 0:
        for x in line.args:
            text += x[0] + ","
        text = text[:-1] + ")"
    else:
        text += ")"
    return text


# ---------------------------------------
# Process NUMVAR, BOOLVAR, STRINGVAR
# ---------------------------------------

def __processASSIG(line, text="", index=0):
    text += "\t" * index + line.name[0] + " = " + __process(line[1]) + "\n"
    return text


def __processASSIGSTRING(line, text="", index=0):
    for field in line:
        if field.getName() is 'STRING':
            text += "\"" + field[0] + "\" "
        elif field.getName() is 'NUMBER':
            text += "str(" + field[0] + ") "
        else:
            text += field[0] + " "
    return text


def __processACTIVATE(line, text="", index=0):
    text += "\t" * index + line.name[0] + " = True\n"
    return text


def __processDEACTIVATE(line, text="", index=0):
    text += "\t" * index + line.name[0] + " = False\n"
    return text


def __processWHILE(line, text="", index=0):
    text += "\n" + "\t" * index + "while "
    for c in line.condition:
        text += __process(line.condition[0])
    text += ":\n"

    index += 1
    for field in line.content:
        text = __process(field, [], text, index) + "\n"

    index -= 1
    return text


def __processWHEN(line, list_var, text="", index=0):
    global ini
    text += "\ndef when_" + str(line.name[0]) + "():\n"
    index += 1
    for x in list_var:
        text += "\t" * index + "global " + x + "\n"
    if str(line.name[0]) != "start":
        text += "\t" * index + "if time_" + str(line.name[0]) + " is 0:\n\t\t" + str(
        line.name[0]) + "_start = time.time()\n"

        text += "\t" * index + "if " + str(line.name[0]) + ":\n"
        index += 1
    for cline in line.content:
        text = __process(cline, [], text, index) + "\n"

    text += "\t" * index + "time_" + str(line.name[0]) + " = time.time() -" + str(
        line.name[0]) + "_start\n"
    if str(line.name[0]) != "start":
        text += "\telse:\n\t\ttime_" + str(line.name[0]) + " = 0\n"
    index -= 1
    if line.condition is not "":
        ini.append(line.name[0] + " = " + __process(line.condition[0]) + "\n")

    text = "\ntime_" + str(line.name[0]) + " = 0\n" + str(line.name[0]) + "_start = time.time()\n" + text

    if line.condition is "":
        text = '\n' + line.name[0] + " =  None\n" + text
    return text


def __processOP(line, text="", index=0):
    for field in line:
        text += __process(field) + " "
    return text


def __processCOMPOP(line, text="", index=0):
    for field in line:
        TYPE = field.getName()
        if TYPE is 'OPERATION':
            text += __process(field)
        elif TYPE is 'COMP':
            text += field[0] + " "
    return text


def __processSIMPLECONDITION(line, text="", index=0):
    for field in line:
        TYPE = field.getName()
        if TYPE is 'NOT':
            text += "not "
        elif TYPE in ['IDENTIFIER', 'SIMPLEFUNCTION', 'FUNCTION', 'TRUE', 'FALSE']:
            text += __process(field)
        elif TYPE is "COMPOP":
            text += __processCOMPOP(field)
    return text


def __processCONDITION(line, text="", index=0):
    for field in line:
        if field.getName() is 'SIMPLECONDITION':
            text += __process(field) + " "
        elif field.getName() is 'ORAND':
            text += field[0] + " "
        elif field.getName() is 'SRMD':
            text += field[0] + " "
    return text


def __processELIF(line, text="", index=0):
    text += "\t" * index + "elif "
    for c in line.condition:
        text += __process(line.condition[0])
    text += ":\n"
    index += 1
    for field in line.content:
        text = __process(field, [], text, index) + "\n"
    return text


def __processELSE(line, text="", index=0):
    text += "\t" * index + "else:\n"
    index += 1
    for field in line.content:
        text = __process(field, [], text, index) + "\n"
    return text


def __processIF(line, text="", index=0):
    text += "\n"+"\t" * index + "if "
    for c in line.condition:
        text += __process(line.condition[0])
    text += ":\n"

    index += 1
    for field in line.content:
        text = __process(field, [], text, index) + "\n"

    index -= 1
    for field in line.OPTIONAL:
        text = "\t" * index + __process(field, [], text, index)
    return text

def parserLearntBotCodeOnlyUserFuntion(code):
    text = ""
    try:
        tree = __parserFromString(code)

        text = __generatePy(tree)
    except Exception as e:
        print(e)
    return text

def parserLearntBotCode(inputFile, outputFile, physicalRobot=False):
    try:
        tree = __parserFromFile(inputFile)
    except Exception as e:
        print(e)
        raise e
    text = """
time_global_start = time.time()
def elapsedTime(umbral):
    global time_global_start
    time_global = time.time()-time_global_start
    return time_global > umbral
    """
    text += __generatePy(tree)

    if physicalRobot:
        header = HEADER.replace('<LearnBotClient>', 'LearnBotClient_PhysicalRobot')
    else:
        header = HEADER.replace('<LearnBotClient>', 'LearnBotClient')
    if text is not "":
        with open(outputFile, 'w') as f:
            f.write(header)
            f.write(text)
        return True
    else:
        return False


if __name__ == "__main__":
    argv = sys.argv[1:]
    if len(argv) is not 3:
        print(bcolors.FAIL + "You must give 2 arguments")
        print("\timputfile\tFile to parser")
        print("\toutputfile\tFile to parser")
        print("\tphysicalRobot\t 1/0 to true or false" + bcolors.ENDC)
        exit(-1)
    if argv[0] == argv[1]:
        print(bcolors.FAIL + "Imputfile must be different to outputfile" + bcolors.ENDC)
        exit(-1)
    print(bcolors.OKGREEN + "Generating file " + argv[1] + bcolors.ENDC)
    text = "\ntime_global_start = time.time()"
    text += "\ndef elapsedTime(umbral):\n\tglobal time_global_start\n\ttime_global = time.time()-time_global_start\n\treturn time_global > umbral\n\n"
    text += __generatePy(__parserFromFile(argv[0]))
    print(bcolors.OKGREEN + "Generating file " + argv[1] + "\t[100%]" + bcolors.ENDC)
    if bool(argv[2]):
        header = HEADER.replace('<LearnBotClient>', 'LearnBotClient_PhysicalRobot')
    else:
        header = HEADER.replace('<LearnBotClient>', 'LearnBotClient')
    with open(argv[1], 'w') as f:
        f.write(header)
        f.write(text)
