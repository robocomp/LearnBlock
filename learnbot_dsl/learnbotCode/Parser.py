#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import

import sys, traceback
import itertools
from pyparsing import *

HEADER = """
#EXECUTION: python code.py
from __future__ import print_function, absolute_import
import sys, os, time, traceback
sys.path.insert(0, os.path.join(os.getenv('HOME'), ".learnblock", "clients"))
from <Client> import Robot
import signal
import sys

usedFunctions = <USEDFUNCTIONS>

try:
<TABHERE>robot = Robot(availableFunctions = usedFunctions)
except Exception as e:
<TABHERE>print("Problems creating a robot instance")
<TABHERE>traceback.print_exc()
<TABHERE>raise(e)

"""
elapsedTimeFunction = """
time_global_start = time.time()
def elapsedTime(umbral):
<TABHERE>global time_global_start
<TABHERE>time_global = time.time()-time_global_start
<TABHERE>return time_global > umbral

"""

signalHandlerFunction = """
def signal_handler(sig, frame):
<TABHERE>robot.stop()
<TABHERE>sys.exit(0)

signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

"""

endOfProgram = """
robot.stop()
sys.exit(0)

"""

loadLibraryCode = """
for f in imports:
<TABHERE>for subPath in [os.path.join(f, x) for x in os.listdir(f)]:
<TABHERE><TABHERE>if os.path.isdir(os.path.abspath(subPath)):
<TABHERE><TABHERE><TABHERE>for subsubPath in [os.path.join(subPath, x) for x in os.listdir(subPath)]:
<TABHERE><TABHERE><TABHERE><TABHERE>if os.path.basename(subsubPath) == os.path.basename(os.path.dirname(subsubPath)) + ".py":
<TABHERE><TABHERE><TABHERE><TABHERE><TABHERE># execfile(os.path.abspath(subsubPath), globals())
<TABHERE><TABHERE><TABHERE><TABHERE><TABHERE>exec(open(os.path.abspath(subsubPath)).read())
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
    'elif') | Keyword('when') | Keyword('while') | Keyword('end') | Keyword('None'))
iden = Word(initChars=alphas, bodyChars=alphanums + "_")
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

PLUE = Literal("+=")
MINE = Literal("-=")
DIVE = Literal("/=")
MULE = Literal("*=")

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
ORAND = Group(OR | AND).setResultsName('ORAND')

"""-----------------OPERADORES----------------------"""
SRMD = Group(plus | minus | mult | div).setResultsName("SRMD")

FUNCTION_FIELDS = Group(Optional(NOT) + (NUMS | TRUE | FALSE | identifier | CHAINBETTENQUOTE)).setResultsName("FIELD")

"""-----------------FUNCTION-------------------------"""
FUNCTION = Group(
    Suppress(Literal("function")) + Suppress(point) + identifier.setResultsName('nameFUNCTION') + Suppress(lpar) + Group(
        Optional(FUNCTION_FIELDS) + ZeroOrMore(Suppress(coma) + (FUNCTION_FIELDS))).setResultsName(
        "args") + Suppress(rpar)).setResultsName("FUNCTION")

"""-----------------FIELDS---------------------------"""
OPERATION = Forward()

FIELDS = Group(Optional(NOT) + (NUMS | TRUE | FALSE | FUNCTION | identifier | Group(Suppress(Literal("(")) + OPERATION + Suppress(Literal(")"))).setResultsName("OPERATIONFIELD") |  CHAINBETTENQUOTE)).setResultsName("FIELD")

"""-----------------SIMPLEFUNCTION-------------------------"""
SIMPLEFUNCTION = Group(identifier.setResultsName('nameDEFFUNCTION') + Suppress(lpar) + Group(
    Optional(FIELDS) + ZeroOrMore(Suppress(coma) + (FIELDS))).setResultsName("args") + Suppress(
    rpar)).setResultsName("SIMPLEFUNCTION")

"""-----------------PASS-------------------------"""
PASS = Group(Literal("pass")).setResultsName("PASS")

"""-----------------OPERACIONES---------------------"""
OPERATION << Group(FIELDS + OneOrMore( (SRMD | ORAND) + FIELDS)).setResultsName("OPERATION")

"""-----------------CONDICIONES---------------------"""
COMPOP = Group(( OPERATION | FIELDS ) + COMP + ( OPERATION | FIELDS )).setResultsName("COMPOP")
OPTIONCONDITION = FUNCTION | SIMPLEFUNCTION | TRUE | FALSE | COMPOP | identifier
SIMPLECONDITION = Group(Optional(NOT) + OPTIONCONDITION).setResultsName("SIMPLECONDITION")
CONDITION = Group(SIMPLECONDITION + ZeroOrMore(( ORAND | SRMD | COMP ) + SIMPLECONDITION)).setResultsName("CONDITION")

"""-----------------asignacion-VARIABLES------------"""

ASSIGSTRING = Group((CHAINBETTENQUOTE | NUMS) + ZeroOrMore(SRMD + (CHAINBETTENQUOTE | NUMS))).setResultsName('ASSIGSTRING')

NONEVAR = NONE.setResultsName("NONEVAR")
VAR = Group(SECTAB + identifier.setResultsName("nameVAR") + (eq | PLUE | MINE | DIVE | MULE) + ( OPERATION | FIELDS | NONEVAR )).setResultsName("VAR")

"""-----------------LINEA---------------------------"""
LINE = Forward()
LINES = Group(LINE + ZeroOrMore(LINE)).setResultsName('LINES')

"""-----------------bloque-IF-----------------------"""
ELSE = Forward()
ELSEIF = Forward()

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
BLOQUEWHENCOND = Group(SECTAB + Suppress(Literal("when")) + identifier.setResultsName("nameWHEN") + Optional(
    Suppress(eq) + Group(CONDITION).setResultsName('condition')) + COLONS + LINES.setResultsName('content') + Literal(
    "end")).setResultsName("WHEN")

"""-----------------ACTIVATE-CONDITION----------------"""
ACTIVATE = Group(Suppress(Literal("activate")) + identifier.setResultsName("nameWHEN")).setResultsName("ACTIVATE")
DEACTIVATE = Group(Suppress(Literal("deactivate")) + identifier.setResultsName("nameWHEN")).setResultsName("DEACTIVATE")

"""-----------------LINEA---------------------------"""
LINE << (SIMPLEFUNCTION | FUNCTION | IF | BLOQUEWHILE | VAR | ACTIVATE | DEACTIVATE | PASS)

"""-----------------DEF----------------------------"""
DEF = Group(Suppress(Literal("def ")) + identifier.setResultsName("nameDEFFUNCTION") + Suppress(lpar) + Suppress(
    rpar) + COLONS + LINES.setResultsName('content') + Suppress(Literal("end"))).setResultsName("DEF")

"""-----------------IMPORT----------------------------"""
IMPORT = Group(Suppress(Literal("import")) + QuotedString('"')).setResultsName("IMPORT")

"""-----------------MAIN----------------------------"""
MAIN = Group(Suppress(Literal("main")) + COLONS + LINES.setResultsName('content')).setResultsName("MAIN") + Suppress(
    Literal("end"))
LB = ZeroOrMore(IMPORT) + ZeroOrMore(LINES) + ZeroOrMore(DEF) + (MAIN | ZeroOrMore(BLOQUEWHENCOND))
LB.ignore(pythonStyleComment)

ini = []

def __listVariables(tree):
    l = []
    for k in tree:
        if isinstance(k, ParseResults):
            lA = __listVariables(k)
            for x in lA:
                if x not in l:
                    l.append(x)
            if len(k) > 0 and not isinstance(k[0], ParseResults) and k.getName() in ["IDENTIFIER", "nameVAR"]:
                if k[0] not in l:
                    l.append(k[0])
    return l

def __findUsedVar(var, lines):
    for l in lines:
        if type(l) is list:
            if __findUsedVar(var, l):
                return True
        if var in l:
            return True
    return False    


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

list_when = []
usedFunctions = []

def __generatePy(lines):
    global usedFunctions
    usedFunctions = []
    text = "\n"
    imports = ['"' + x[0] + '"' for x in lines if x.getName() is 'IMPORT']
    if len(imports)>0:
        imports = "imports = [" + ", ".join(imports) + "]"
        text = "\n" + imports + loadLibraryCode
    global list_when
    list_when = [x.nameWHEN[0] for x in lines if x.getName() is "WHEN"]
    list_var=__listVariables(lines)
#    for x in list_when:
#        list_var.append("time_" + str(x))
#        list_var.append(str(x) + "_start")
#        list_var.append("state_" + x)
    global ini
    for x in lines:
        if x.getName() is "MAIN" and len(list_when)>0 or x.getName() is "IMPORT":
            continue
        if x.getName() is "LINES":
            for y in x:
                text = __process(y, list_var, text) + "\n"
        else:
            text = __process(x, list_var, text)
    if len(list_when) > 0:
        if 'start' in list_when:
            text += "\nwhen_start()\n"
        text += "\n\nwhile True:\n"
        text += "".join(["<TABHERE>" + line for line in ini])
        whens = ["<TABHERE>when_" + str(x.nameWHEN[0]) + "()\n" for x in lines if x.getName() is 'WHEN' and x.nameWHEN[0] != "start"]
        if len(whens)>0:
            text += "".join(whens)
        else:
            text += "<TABHERE>pass"
    return text


def __process(line, list_var=[], text="", index=0):
    TYPE = line.getName()
    if TYPE is 'MAIN':
        text += "\n".join([__process(cLine, [], "", 0) for cLine in line.content])
    elif TYPE is 'FIELD':
        text += __processFIELD(line, "")
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
    elif TYPE is 'OPERATIONFIELD':
        text = __processOPF(line, text, index)
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
        text += "<TABHERE>" * index + "pass\n"
    elif TYPE is 'NONEVAR':
        text += "None"
    elif TYPE is 'STRING':
        text += '"' + line[0] + '"'
    elif TYPE in ['FALSE', 'TRUE', 'IDENTIFIER', 'SRMD', 'ORAND', "NUMBER","NOT"]:
        text = line[0]
    else:
        print("The type is ", TYPE , line)
    return text

def __processFIELD(line, text="", index=0):
    for field in line:
        text+=__process(field)
    return text

def __processDEF(line, list_var, text="", index=0):
    text += "\ndef " + line.nameDEFFUNCTION[0] + "():\n"
    for x in list_var:
        if __findUsedVar(x, line.asList()):
            text += "<TABHERE>" * index + "global " + x + "\n"
    for field in line.content:
        text = __process(field, [], text, index) + "\n\n"
    return text


def __processFUNCTION(line, text="", index=0):
    if text is not "":
        text += "<TABHERE>" * index
    global usedFunctions
    if line.nameFUNCTION[0] not in usedFunctions:
        usedFunctions.append(line.nameFUNCTION[0])
    text += "robot." + line.nameFUNCTION[0] + "("
    text += ",".join([__process(x) for x in line.args])
    # for x in line.args:
    #     text += ", " + __process(x)
    text += ")"
    return text


def __processSIMPLEFUNCTION(line, text="", index=0):
    if text is not "":
        text += "<TABHERE>" * index
    text += line.nameDEFFUNCTION[0] + "("
    if len(line.args) is not 0:
        for x in line.args:
            text += __process(x) + ","
        text = text[:-1] + ")"
    else:
        text += ")"
    return text


# ---------------------------------------
# Process NUMVAR, BOOLVAR, STRINGVAR
# ---------------------------------------

def __processASSIG(line, text="", index=0):
    text += "<TABHERE>" * index + line.nameVAR[0] + " " + line[1] + " " + __process(line[2])
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
    text += "<TABHERE>" * index + "state_" + line.nameWHEN[0] + " = True\n"
    return text


def __processDEACTIVATE(line, text="", index=0):
    text += "<TABHERE>" * index + "state_" + line.nameWHEN[0] + " = False\n"
    return text


def __processWHILE(line, text="", index=0):
    text += "\n" + "<TABHERE>" * index + "while "
    for c in line.condition:
        text += __process(line.condition[0])
    text += ":\n"

    index += 1
    for field in line.content:
        text = __process(field, [], text, index) + "\n"

    index -= 1
    return text


def __processWHEN(line, list_var, text="", index=0):
    global ini, list_when
    name = str(line.nameWHEN[0])
    whenText = """
<INIVARIABLES>
def when_<NAME>():
<TABHERE>global <GLOBALSVARIABLES>
"""
    if name != "start":
        whenText += """<TABHERE>if time_<NAME> is 0:
<TABHERE><TABHERE><NAME>_start = time.time()
<TABHERE>if state_<NAME>:\n"""
        index += 2
    else:
        index += 1
    states = ["state_" + x for x in list_when if x!="start"]

    globalVariables = list(set([name + "_start", "time_" + name, "state_" + name]))
    for v in [x for x in list_when]:
        if __findUsedVar(v, line.asList()):
            if "time_"+v not in globalVariables:
                globalVariables.append("time_"+v)
            if "state_"+v not in globalVariables:
                globalVariables.append("state_"+v)

    for v in [x for x in list_var]:
        if __findUsedVar(v, line.asList()) and v not in globalVariables:
            globalVariables.append(v)

    text += whenText.replace("<GLOBALSVARIABLES>", ", ".join(globalVariables))
    for cline in line.content:
        text = __process(cline, [], text, index) + "\n"

    if name != "start":
        text = text.replace("<INIVARIABLES>", "<NAME>_start = time.time()\nstate_<NAME> = False\ntime_<NAME> = 0\n")
        text += "<TABHERE><TABHERE>time_<NAME> = time.time() - <NAME>_start\n" \
                "<TABHERE>if not state_<NAME>:\n" \
                "<TABHERE><TABHERE>time_<NAME> = 0\n"
            #    "<NAME>_start = time.time()\n" \
            #    "state_<NAME> = False\n" +\
            #    text +\
    else:
        text = text.replace("<INIVARIABLES>", "")
    text = text.replace("<NAME>", name)
    index -= 1
    if line.condition is not "":
        ini.append("state_" + name + " = " + __process(line.condition[0]) + "\n")
    # else:
    #     text = '\n' + name + " =  None\n" + text
    return text


def __processOP(line, text="", index=0):
    text += " ".join([__process(field) for field in line])
    # for field in line:
    #     text += __process(field) + " "
    return text

def __processOPF(line, text="", index=0):
    text += "(" + " ".join([__process(field) for field in line]) + ")"
    # for field in line:
    #     text += __process(field) + " "
    return text

def __processCOMPOP(line, text="", index=0):
    for field in line:
        TYPE = field.getName()
        if TYPE is 'OPERATION':
            text += __process(field)
        elif TYPE is 'COMP':
            text += field[0] + " "
        elif TYPE is "FIELD":
            text += __process(field[0]) + " "
        else:
            print("__processCOMPOP", TYPE)
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
        elif field.getName() is 'COMP':
            text += field[0] + " "
    return text


def __processELIF(line, text="", index=0):
    text += "<TABHERE>" * index + "elif "
    for c in line.condition:
        text += __process(line.condition[0])
    text += ":\n"
    index += 1
    for field in line.content:
        text = __process(field, [], text, index) + "\n"
    return text


def __processELSE(line, text="", index=0):
    text += "<TABHERE>" * index + "else:\n"
    index += 1
    for field in line.content:
        text = __process(field, [], text, index) + "\n"
    return text


def __processIF(line, text="", index=0):
    text += "\n"+"<TABHERE>" * index + "if "
    for c in line.condition:
        text += __process(line.condition[0])
    text += ":\n"

    index += 1
    for field in line.content:
        text = __process(field, [], text, index) + "\n"

    index -= 1
    for field in line.OPTIONAL:
        text = "<TABHERE>" * index + __process(field, [], text, index)
    return text

def parserLearntBotCodeOnlyUserFuntion(code):
    text = ""
    try:
        tree = __parserFromString(code)

        text = __generatePy(tree)
        text = cleanCode(_code=text)
    except Exception as e:
        traceback.print_exc()
    return text

def parserLearntBotCode(inputFile, outputFile, client_name):
    global usedFunctions

    try:
        tree = __parserFromFile(inputFile)
    except Exception as e:
        traceback.print_exc()
        raise e
    text = elapsedTimeFunction
    text += signalHandlerFunction
    text += __generatePy(tree)
    text += endOfProgram
    text = cleanCode(_code=text)

    header = HEADER.replace('<Client>', client_name).replace("<USEDFUNCTIONS>", str(usedFunctions))
    header = cleanCode(_code=header)
    if text is not "":
        with open(outputFile, 'w') as f:
            f.write(header)
            f.write(text)
        return True
    else:
        return False

def parserLearntBotCodeFromCode(code, name_client):
    global usedFunctions

    try:
        tree = __parserFromString(code)
    except Exception as e:
        traceback.print_exc()
        raise e
    text = elapsedTimeFunction
    text += signalHandlerFunction
    text += __generatePy(tree)
    text += endOfProgram
    text = cleanCode(_code=text)
    header = HEADER.replace('<Client>', name_client).replace("<USEDFUNCTIONS>", str(usedFunctions))
    header = cleanCode(_code=header)

    if text is not "":
        return header + text
    else:
        return False

def cleanCode(_code):
    newcode = _code.replace(" :", ":").replace("  ", " ").replace("\n\n\n", "\n\n")
    while _code != newcode:
        _code = newcode
        newcode = _code.replace(" :", ":").replace("  ", " ").replace("\n\n\n", "\n\n")
    return _code.replace("<TABHERE>","    ")


if __name__ == "__main__":
    textprueba = """


when hay_alguien_triste = function.is_there_somebody_sad():
	if 1 < time_hay_alguien_triste:
		function.expressSadness()
	end
end

when start:
	function.look_up()
	function.expressNeutral()
end

when hay_alguien_sorprendido = function.is_there_somebody_surprised():
	if 1 < time_hay_alguien_sorprendido:
		function.expressSurprise()
	end
end

when hay_alguien_enfadado = function.is_there_somebody_angry():
	if 1 < time_hay_alguien_enfadado:
		function.expressAnger()
	end
end

when hay_alguien_neutral = function.is_there_somebody_neutral():
	if 1 < time_hay_alguien_neutral:
		function.expressNeutral()
	end
end

when hay_alguien_alegre = function.is_there_somebody_happy():
	if 1 < time_hay_alguien_alegre:
		function.expressJoy()
	end
end

"""
    try:
        print(__parserFromString(textprueba))
        text = __generatePy(__parserFromString(textprueba))
        text = cleanCode(_code=text)
        print("----------------\n\n", text)
    except ParseException as pe:
        print(pe.line)
        print(' ' * (pe.col - 1) + '^')
        print(pe)

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
    if bool(argv[2]):
        header = HEADER.replace('<Client>', 'LearnBotClient_PhysicalRobot')
    else:
        header = HEADER.replace('<Client>', 'LearnBotClient')
    text = header
    text += elapsedTimeFunction
    text += signalHandlerFunction
    text += __generatePy(__parserFromFile(argv[0]))
    text = cleanCode(_code=text)
    print(bcolors.OKGREEN + "Generating file " + argv[1] + "\t[100%]" + bcolors.ENDC)

    with open(argv[1], 'w') as f:
        f.write(text)
