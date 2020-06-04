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

usedFunctions = <USEDCALLS>

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

KEYWORDS = (
    Keyword('def')
    | Keyword('=')
    | Keyword('function')
    | Keyword('>=')
    | Keyword('<=')
    | Keyword('<')
    | Keyword('>')
    | Keyword('deactivate')
    | Keyword('activate')
    | Keyword('not')
    | Keyword('True')
    | Keyword('False')
    | Keyword('or')
    | Keyword('and')
    | Keyword('main')
    | Keyword('if')
    | Keyword('else')
    | Keyword('elif')
    | Keyword('when')
    | Keyword('while')
    | Keyword('end')
    | Keyword('None')
)

NAME = Word(initChars=alphas, bodyChars=alphanums + '_')

OPAR = Suppress(Literal('('))
CPAR = Suppress(Literal(')'))
COLON = Suppress(Literal(':'))
INDENT = Suppress(ZeroOrMore('\t'))
END = Suppress(Literal('end'))
DOT = Literal('.')

PLUA = Literal('+=')
MINA = Literal('-=')
DIVA = Literal('/=')
MULA = Literal('*=')
ASSIGN = Literal('=')

NOT = Literal('not')
OR = Literal('or')
AND = Literal('and')
PLUS = Literal('+')
MINUS = Literal('-')
TIMES = Literal('*')
OVER = Literal('/')

LT = Literal('<')
GT = Literal('>')
LE = Literal('<=')
GE = Literal('>=')
EQ = Literal('==')
NE = Literal('!=')

DIGITS = Word(nums)
SIGN = Literal('+') | Literal('-')
INTEGER = Combine(Optional(SIGN) + DIGITS)
EXP = CaselessLiteral('E')
NUMBER = Combine(
    INTEGER
    + Optional(DOT + Optional(DIGITS))
    + Optional(EXP + INTEGER)
)

IDENTIFIER = ~KEYWORDS + NAME
TRUE = Literal('True')
FALSE = Literal('False')
NONE = Literal('None')
STRING = QuotedString('"')

class Value:
    def __init__(self, tokens):
        self.value = tokens[0]

    def to_python(self, gen):
        return self.value

VALUE = (
    NUMBER
    | TRUE
    | FALSE
    | NONE
    | STRING
    | IDENTIFIER
).setParseAction(Value)

"""-----------------COMPARACIONES-------------------"""
COMP = LT | GT | LE | GE | EQ | NE

"""-----------------OPERATION-----------------"""
OPERATION = Forward()

"""-----------------CALL-------------------------"""
class Call:
    def __init__(self, tokens):
        self.function = tokens[0]
        self.args = tokens[1].asList()

    def to_python(self, gen):
        args = ', '.join([arg.to_python(gen) for arg in self.args])

        return f'robot.{self.function}({args})'

CALL = (
    Suppress(Literal('function'))
    + Suppress(DOT)
    + IDENTIFIER
    + OPAR
    + Group(Optional(delimitedList(OPERATION)))
    + CPAR
).setParseAction(Call)

"""-----------------SIMPLECALL-------------------------"""
class SimpleCall:
    def __init__(self, tokens):
        self.function = tokens[0]
        self.args = tokens[1].asList()

    def to_python(self, gen):
        args = ', '.join([arg.to_python(gen) for arg in self.args])

        return f'{self.function}({args})'

SIMPLECALL = Group(
        IDENTIFIER
        + OPAR
        + Group(Optional(delimitedList(OPERATION)))
        + CPAR
    ).setParseAction(SimpleCall)

"""-----------------OPERACIONES---------------------"""
class UnaryOp:
    def __init__(self, tokens):
        self.operator = tokens[0][0]
        self.operand = tokens[0][1]

    def to_python(self, gen):
        operand = self.operand.to_python(gen)

        return f'{self.operator} {operand}'

class BinaryOp:
    def __init__(self, tokens):
        self.left = tokens[0][0]
        self.operator = tokens[0][1]
        self.right = tokens[0][2]

    def to_python(self, gen):
        # TODO: this is buggy, as it doesn't take into account parentheses!

        left = self.left.to_python(gen)
        right = self.right.to_python(gen)

        return f'{left} {self.operator} {right}'

OPTABLE = [
    (MINUS, 1, opAssoc.RIGHT, UnaryOp),
    (PLUS,  1, opAssoc.RIGHT, UnaryOp),
    (NOT,   1, opAssoc.RIGHT, UnaryOp),
    (OVER,  2, opAssoc.LEFT, BinaryOp),
    (TIMES, 2, opAssoc.LEFT, BinaryOp),
    (MINUS, 2, opAssoc.LEFT, BinaryOp),
    (PLUS,  2, opAssoc.LEFT, BinaryOp),
    (COMP,  2, opAssoc.LEFT, BinaryOp),
    (AND,   2, opAssoc.LEFT, BinaryOp),
    (OR,    2, opAssoc.LEFT, BinaryOp),
]

OPERATION << infixNotation(VALUE | CALL, OPTABLE, OPAR, CPAR)

"""-----------------PASS-------------------------"""
class Pass:
    def __init__(self, location, tokens):
        self.location = location

    def to_python(self, gen):
        return 'pass'

PASS = Literal('pass').setParseAction(Pass)

"""-----------------asignacion-VARIABLES------------"""
class Var:
    def __init__(self, tokens):
        self.name = tokens[0]
        self.operator = tokens[1]
        self.right = tokens[2]

    def to_python(self, gen):
        right = self.right.to_python(gen)

        return f'{self.name} {self.operator} {right}\n'

VAR = (
    INDENT
    + IDENTIFIER
    + (ASSIGN | PLUA | MINA | DIVA | MULA)
    + OPERATION
).setParseAction(Var)

"""-----------------LINEA---------------------------"""
LINE = Forward()
LINES = Group(OneOrMore(LINE))

"""-----------------bloque-IF-----------------------"""
class If:
    def __init__(self, tokens):
        self.condition = tokens[0]
        self.body = tokens[1].asList()
        self.alternatives = tokens[2].asList()

    def to_python(self, gen):
        condition = self.condition.to_python(gen)
        output = f'if {condition}:\n'

        for node in self.body + self.alternatives:
            output += node.to_python(gen)

        return output

class ElseIf:
    def __init__(self, tokens):
        self.condition = tokens[0]
        self.body = tokens[1].asList()

    def to_python(self, gen):
        output = f'elif {self.condition.to_python(gen)}:\n'

        for node in self.body:
            output += node.to_python(gen)

        return output

class Else:
    def __init__(self, tokens):
        self.body = tokens[0].asList()

    def to_python(self, gen):
        output = f'else:\n'

        for node in self.body:
            output += node.to_python(gen)

        return output

ELSE = Forward()
ELSEIF = Forward()

ELSEIF << Group(
    INDENT
    + Suppress(Literal('elif'))
    + OPERATION
    + COLON
    + LINES
).setParseAction(ElseIf)

ELSE << (
    INDENT
    + Suppress(Literal('else'))
    + COLON
    + LINES
).setParseAction(Else)

IF = (
    INDENT
    + Suppress(Literal('if'))
    + OPERATION
    + COLON
    + LINES
    + Group(ZeroOrMore(ELSEIF) + Optional(ELSE))
    + END
).setParseAction(If)

"""-----------------LOOP----------------------------"""
class While:
    def __init__(self, tokens):
        self.condition = tokens[0]
        self.body = tokens[1].asList()

    def to_python(self, gen):
        output = f'while {self.condition.to_python(gen)}:\n'

        for node in self.body:
            output += node.to_python(gen)

        return output

BLOQUEWHILE = (
    INDENT
    + Suppress(Literal('while'))
    + OPERATION
    + COLON
    + LINES
    + END
).setParseAction(While)

"""-----------------WHEN+CONDICION------------------"""
class When:
    def __init__(self, tokens):
        self.condition = tokens[0]
        self.body = tokens[1].asList()

BLOQUEWHENCOND = (
    INDENT
    + Suppress(Literal('when'))
    + IDENTIFIER
    + Optional(
        Suppress(ASSIGN)
        + OPERATION
    )
    + COLON
    + LINES
    + END
).setParseAction(When)

"""-----------------ACTIVATE-CONDITION----------------"""
class Activate:
    def __init__(self, tokens):
        self.name = tokens[0]

    def to_python(self, gen):
        return f'state_{self.name} = True\n'

class Deactivate:
    def __init__(self, tokens):
        self.name = tokens[0]

    def to_python(self, gen):
        return f'state_{self.name} = False\n'

ACTIVATE = Suppress(Literal('activate')) + IDENTIFIER
DEACTIVATE = Suppress(Literal('deactivate')) + IDENTIFIER

"""-----------------LINEA---------------------------"""
LINE << (
    SIMPLECALL
    | CALL
    | IF
    | BLOQUEWHILE
    | VAR
    | ACTIVATE
    | DEACTIVATE
    | PASS
)

"""-----------------DEF----------------------------"""
class Definition:
    def __init__(self, tokens):
        self.name = tokens[0]
        self.body = tokens[1].asList()

DEF = (
    Suppress(Literal('def'))
    + IDENTIFIER
    + OPAR
    + CPAR
    + COLON
    + LINES
    + END
).setParseAction(Definition)

"""-----------------IMPORT----------------------------"""
class Import:
    def __init__(self, tokens):
        self.path = tokens[0]

    def to_python(self, gen):
        return f'import "{self.path}"\n'

IMPORT = (
    Suppress(Literal('import'))
    + STRING
).setParseAction(Import)

"""-----------------MAIN----------------------------"""
class Main:
    def __init__(self, tokens):
        self.body = tokens[0].asList()

    def to_python(self, gen):
        output = ''

        for node in self.body:
            output += node.to_python(gen)

        return output

MAIN = (
    Suppress(Literal('main'))
    + COLON
    + LINES
    + END
).setParseAction(Main)

class Program:
    def __init__(self, tokens):
        print(tokens)
        self.imports = tokens[0].asList()
        self.inits = tokens[1].asList()
        self.defs = tokens[2].asList()
        self.blocks = tokens[3].asList()

    def to_python(self, gen):
        nodes = self.imports + self.inits + self.defs + self.blocks
        output = ''

        for node in nodes:
            output += node.to_python(gen)

        return output

LB = (
    Group(ZeroOrMore(IMPORT))
    + Group(ZeroOrMore(LINE))
    + Group(ZeroOrMore(DEF))
    + Group(MAIN | ZeroOrMore(BLOQUEWHENCOND))
).setParseAction(Program)

LB.ignore(pythonStyleComment)

# We use infixNotation, so performance without this is HORRIBLE
# enablePackrat makes use of the Packrat method for parsing, which recognizes
# and memoizes repeating patterns so they are not re-evaluated each time.
#
# See: github.com/pyparsing/pyparsing/wiki/Performance-Tips
LB.enablePackrat()

class PythonGenerator:
    def __init__(self):
        pass

    def generate_python(self, tree):
        return tree.to_python(self)

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
        tree = LB.parseString(text, parseAll=True)[0]
        return True, tree
    except ParseException as pe:
        print(pe.line)
        print(' ' * (pe.col - 1) + '^')
        print(pe)

        return False, pe

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

def __processDEF(line, list_var, text="", index=0):
    text += "\ndef " + line.nameDEFCALL[0] + "():\n"
    for x in list_var:
        if __findUsedVar(x, line.asList()):
            text += "<TABHERE>" * index + "global " + x + "\n"
    for field in line.content:
        text = __process(field, [], text, index) + "\n\n"
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

def parserLearntBotCodeOnlyUserFuntion(code):
    text = ""
    # TODO: check for errors
    try:
        _, tree = __parserFromString(code)

        text = __generatePy(tree)
        text = cleanCode(_code=text)
    except Exception as e:
        traceback.print_exc()
    return text

def parserLearntBotCode(inputFile, outputFile, client_name):
    global usedFunctions

    errors = []

    try:
        success, output = __parserFromFile(inputFile)
    except Exception as e:
        traceback.print_exc()
        raise e
    if not success:
        errors.append({
            'level': 'error',
            'message': "Parse error",
            'span': (output.lineno, None),
        })

        return False, errors
    else:
        text = elapsedTimeFunction
        text += signalHandlerFunction
        text += __generatePy(output)
        text += endOfProgram
        text = cleanCode(_code=text)

        header = HEADER.replace('<Client>', client_name).replace("<USEDCALLS>", str(usedFunctions))
        header = cleanCode(_code=header)

        with open(outputFile, 'w') as f:
            f.write(header)
            f.write(text)

        return header, errors

def parserLearntBotCodeFromCode(code, name_client):
    global usedFunctions

    errors = []

    try:
        success, output = __parserFromString(code)
    except Exception as e:
        traceback.print_exc()
        raise e
    if not success:
        errors.append({
            'level': 'error',
            'message': "Parse error",
            'span': (output.lineno, None),
        })

        return False, errors
    else:
        text = elapsedTimeFunction
        text += signalHandlerFunction
        text += __generatePy(output)
        text += endOfProgram
        text = cleanCode(_code=text)
        header = HEADER.replace('<Client>', name_client).replace("<USEDCALLS>", str(usedFunctions))
        header = cleanCode(_code=header)

        return header + text, errors

def cleanCode(_code):
    newcode = _code.replace(" :", ":").replace("  ", " ").replace("\n\n\n", "\n\n")
    while _code != newcode:
        _code = newcode
        newcode = _code.replace(" :", ":").replace("  ", " ").replace("\n\n\n", "\n\n")
    return _code.replace("<TABHERE>","    ")

src = """
if x == 2:
    pass
end
"""

if __name__ == "__main__":
    textprueba = """

x = None

main:
    x = 0
    x = 1
    x = a + b
    x = a + b * c
    x = (a + b) * c
    x = a + b + c
    x = 2 + 3 - 5 == 0 and x > y
    x = not not True
    if x == 2:
        pass
    end
end

"""
    try:
        tree = __parserFromString(textprueba)[1]
        gen= PythonGenerator()
        print(tree.__dict__)
        print(gen.generate_python(tree))
        exit(-1)
        # OLD CODE STARTING HERE
        text = __generatePy(__parserFromString(textprueba)[1])
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
