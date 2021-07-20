#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import

import sys, traceback
import itertools
from learnbot_dsl.learnbotCode.Notification import *
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

class Node:
    last_stmt = None

    def __init__(self, src, start, tokens):
        global last_parsed

        end = tokens[-1]
        del tokens[-1]

        sl = lineno(start, src)
        sc = col(start, src)

        el = lineno(end, src)
        ec = col(end, src)

        self.start = sl, sc, start
        self.end = el, ec, end

    def signature(self, ctx):
        return [], True

    def typecheck(self, ctx):
        return True

    @property
    def used_vars(self):
        return set()

    @classmethod
    def set_last_statement(cls, last):
        cls.last_stmt = last

    @classmethod
    def last_statement(cls):
        return cls.last_stmt

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

ENDLOC = Empty().leaveWhitespace().setParseAction(lambda s, loc, t: loc)

NAME = Word(initChars = alphas, bodyChars = alphanums + '_')

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
EXP = CaselessLiteral('E')
INTEGER = Combine(Optional(SIGN) + DIGITS)
NUMBER = Combine(
    INTEGER
    + Optional(DOT + Optional(DIGITS))
    + Optional(EXP + INTEGER)
)

class Identifier(Node):
    def __init__(self, src, start, tokens):
        super().__init__(src, start, tokens)
        self.name = tokens[0]

    def to_python(self, gen, *_):
        return self.name

    @property
    def used_vars(self):
        return {self.name}

IDENTIFIER = (~KEYWORDS + NAME + ENDLOC).setParseAction(Identifier)

TRUE = Literal('True')
FALSE = Literal('False')
NONE = Literal('None')
STRING = QuotedString('"', escChar = '\\', unquoteResults = False)

class Value(Node):
    def __init__(self, src, start, tokens):
        super().__init__(src, start, tokens)
        self.value = eval(tokens[0])

    def to_python(self, gen, *_):
        return repr(self.value)

    def signature(self, ctx):
        if type(self.value) == int:
            output = float
        elif self.value == None:
            output = True
        else:
            output = type(self.value)

        return [], output

VALUE = ((
    NUMBER
    | TRUE
    | FALSE
    | NONE
    | STRING
) + ENDLOC).setParseAction(Value)

"""-----------------OPERATION-----------------"""
OPERATION = Forward()

"""-----------------CALL-------------------------"""
class Call(Node):
    def __init__(self, src, start, tokens):
        super().__init__(src, start, tokens)

        self.function = tokens[0]
        self.args = tokens[1].asList()

    def to_python(self, gen, *_):
        function = self.function.to_python(gen)
        args = [arg.to_python(gen) for arg in self.args]

        global usedFunctions
        if function not in usedFunctions:
            usedFunctions.append(function)

        return f'robot.{function}({", ".join(args)})'

    def typecheck(self, ctx):
        # TODO: check that the arguments match the function signature
        return all([node.typecheck(ctx) for node in self.args])

    @property
    def used_vars(self):
        return {var for arg in self.args
                    for var in arg.used_vars}

CALL = (
    Suppress(Literal('function')).addParseAction(lambda: Node.set_last_statement(Call))
    - Suppress(DOT)
    - IDENTIFIER
    - OPAR
    - Group(Optional(delimitedList(OPERATION)))
    - CPAR
    + ENDLOC
).setParseAction(Call)

"""-----------------SIMPLECALL-------------------------"""
class SimpleCall(Node):
    def __init__(self, src, start, tokens):
        super().__init__(src, start, tokens)

        self.function = tokens[0]
        self.args = tokens[1].asList()

    def to_python(self, gen, *_):
        function = self.function.to_python(gen)
        args = [arg.to_python(gen) for arg in self.args]

        return f'{function}({", ".join(args)})'

    def typecheck(self, ctx):
        # TODO: check that the arguments match the function signature
        return all([node.typecheck(ctx) for node in self.args])

    @property
    def used_vars(self):
        return {var for arg in self.args
                    for var in arg.used_vars}

# SIMPLECALL = (Group(
#         IDENTIFIER.addParseAction(lambda: Node.set_last_statement(SimpleCall))
#         + OPAR
#         - Group(Optional(delimitedList(OPERATION)))
#         - CPAR
#     ) + ENDLOC).setParseAction(SimpleCall)

SIMPLECALL = (
        IDENTIFIER.addParseAction(lambda: Node.set_last_statement(SimpleCall))
        + OPAR
        - Group(Optional(delimitedList(OPERATION)))
        - CPAR
        + ENDLOC).setParseAction(SimpleCall)


"""-----------------OPERACIONES---------------------"""
class UnaryOp(Node):
    def __init__(self, src, start, tokens):
        [[operator, operand]] = tokens

        self.operator = operator
        self.operand = operand

        sl = lineno(start, src)
        sc = col(start, src)

        self.start = sl, sc, start
        self.end = operand.end

    def to_python(self, gen, max_precedence = float('inf'), *_):
        precedence = gen.precedence_of(self.operator, UnaryOp)

        # This makes pure symbolic operators be closer to their operands,
        # avoiding confusion with their infix counterparts.
        #
        # For example:
        #
        # -a - -b instead of - a - - b
        sep = ' ' if self.operator.isalnum() else ''

        if precedence <= max_precedence:
            operand = self.operand.to_python(gen, precedence)
            return f'{self.operator}{sep}{operand}'
        else:
            operand = self.operand.to_python(gen)
            return f'({self.operator}{sep}{operand})'

    def typecheck(self, ctx):
        [input], _ = self.signature(ctx)
        _, output = self.operand.signature(ctx)

        return ctx.unify(self.operand, output, input) and self.operand.typecheck(ctx)

    def signature(self, ctx):
        return ctx.operator_signature(self.operator, BinaryOp)

    @property
    def used_vars(self):
        return self.operand.used_vars

class BinaryOp(Node):
    def __init__(self, src, start, tokens):
        [[*rest, op, last]] = tokens

        # NOTE: this assumes left associativity. This is fine for us, as we
        # don't have any right-associative operators
        self.left = BinaryOp(src, start, [rest]) if len(rest) > 1 else rest[0]
        self.operator = op
        self.right = last

        sl = lineno(start, src)
        sc = col(start, src)

        self.start = sl, sc, start
        self.end = last.end

    def to_python(self, gen, max_precedence = float('inf'), *_):
        precedence = gen.precedence_of(self.operator, BinaryOp)

        if precedence <= max_precedence:
            left = self.left.to_python(gen, precedence)
            right = self.right.to_python(gen, precedence)

            return f'{left} {self.operator} {right}'
        else:
            left = self.left.to_python(gen)
            right = self.right.to_python(gen)

            return f'({left} {self.operator} {right})'

    def typecheck(self, ctx):
        [li, ri], _ = self.signature(ctx)
        _, lo = self.left.signature(ctx)
        _, ro = self.right.signature(ctx)

        return ctx.unify(self.left, lo, li) and ctx.unify(self.right, ro, ri) and self.left.typecheck(ctx) and self.right.typecheck(ctx)

    def signature(self, ctx):
        return ctx.operator_signature(self.operator, BinaryOp)

    @property
    def used_vars(self):
        vars = self.left.used_vars
        vars = vars.union(self.right.used_vars)

        return vars

OPTABLE = [
    # operator parser   arity  associativity  class,    input type      output type
    (PLUS | MINUS,      1,     opAssoc.RIGHT, UnaryOp,  [float],        float),
    (NOT,               1,     opAssoc.RIGHT, UnaryOp,  [bool],         bool),
    (TIMES | OVER,      2,     opAssoc.LEFT,  BinaryOp, [float, float], float),
    (PLUS | MINUS,      2,     opAssoc.LEFT,  BinaryOp, [float, float], float),
    (LT | GT | LE | GE, 2,     opAssoc.LEFT,  BinaryOp, [bool, bool],   bool),
    (EQ | NE,           2,     opAssoc.LEFT,  BinaryOp, [True, True],   True),
    (AND,               2,     opAssoc.LEFT,  BinaryOp, [bool, bool],   bool),
    (OR,                2,     opAssoc.LEFT,  BinaryOp, [bool, bool],   bool),
]

OPERATION << infixNotation(SIMPLECALL | VALUE | IDENTIFIER | CALL, OPTABLE, OPAR, CPAR)

"""-----------------PASS-------------------------"""
class Pass(Node):
    def __init__(self, src, start, tokens):
        super().__init__(src, start, tokens)

    def to_python(self, gen, *_):
        return 'pass'

PASS = (Literal('pass') + ENDLOC).setParseAction(Pass)

"""-----------------asignacion-VARIABLES------------"""
class Var(Node):
    def __init__(self, src, start, tokens):
        super().__init__(src, start, tokens)

        self.var = tokens[0]
        self.operator = tokens[1]
        self.right = tokens[2]

    def to_python(self, gen, *_):
        var = self.var.to_python(gen)
        right = self.right.to_python(gen)

        return f'{var} {self.operator} {right}'

    def typecheck(self, ctx):
        # TODO: check also inputs
        var = self.var.to_python(None)

        _, vo = ctx.lookup(var)
        _, ro = self.right.signature(ctx)

        uo = ctx.unify(self.right, ro, vo)

        if uo:
            signature = [], uo
            ctx.update_signature(var, signature)

        return self.right.typecheck(ctx)

    @property
    def used_vars(self):
        vars = self.var.used_vars
        vars = vars.union(self.right.used_vars)

        return vars

VAR = (
    INDENT
    + IDENTIFIER
    + (ASSIGN | PLUA | MINA | DIVA | MULA).addParseAction(lambda: Node.set_last_statement(Var))
    - OPERATION
    + ENDLOC
).setParseAction(Var)

"""-----------------LINEA---------------------------"""
LINE = Forward()
LINES = Group(OneOrMore(LINE))

"""-----------------bloque-IF-----------------------"""
class If(Node):
    def __init__(self, src, start, tokens):
        super().__init__(src, start, tokens)

        self.condition = tokens[0]
        self.body = tokens[1].asList()
        self.alternatives = tokens[2].asList()

    def to_python(self, gen):
        condition = self.condition.to_python(gen)
        output = f'if {condition}:\n'

        gen.indent()

        for node in self.body:
            output += gen.tabs() + node.to_python(gen) + '\n'

        gen.dedent()

        for node in self.alternatives:
            output += gen.tabs() + node.to_python(gen)

        return output

    def typecheck(self, ctx):
        _, co = self.condition.signature(ctx)

        return ctx.unify(self.condition, co, bool) and all([node.typecheck(ctx) for node in self.body])

    @property
    def used_vars(self):
        vars = {var for node in self.body + self.alternatives
                    for var in node.used_vars}

        vars = vars.union(self.condition.used_vars)

        return vars

class ElseIf(Node):
    def __init__(self, src, start, tokens):
        super().__init__(src, start, tokens)

        self.condition = tokens[0]
        self.body = tokens[1].asList()

    def to_python(self, gen, *_):
        condition = self.condition.to_python(gen)
        output = f'elif {condition}:\n'

        gen.indent()

        for node in self.body:
            output += gen.tabs() + node.to_python(gen) + '\n'

        gen.dedent()

        return output

    def typecheck(self, ctx):
        _, co = self.condition.signature(ctx)

        return ctx.unify(self.condition, co, bool) and all([node.typecheck(ctx) for node in self.body])

    @property
    def used_vars(self):
        vars = {var for node in self.body
                    for var in node.used_vars}

        vars = vars.union(self.condition.used_vars)

        return vars

class Else(Node):
    def __init__(self, src, start, tokens):
        super().__init__(src, start, tokens)

        self.body = tokens[0].asList()

    def to_python(self, gen, *_):
        output = f'else:\n'

        gen.indent()

        for node in self.body:
            output += gen.tabs() + node.to_python(gen) + '\n'

        gen.dedent()

        return output

    def typecheck(self, ctx):
        return all([node.typecheck(ctx) for node in self.body])

    @property
    def used_vars(self):
        return {var for node in self.body
                    for var in node.used_vars}

ELSE = Forward()
ELSEIF = Forward()

ELSEIF << (
    INDENT
    + Suppress(Literal('elif')).addParseAction(lambda: Node.set_last_statement(ElseIf))
    - OPERATION
    - COLON
    - LINES
    + ENDLOC
).setParseAction(ElseIf)

ELSE << (
    INDENT
    + Suppress(Literal('else')).addParseAction(lambda: Node.set_last_statement(Else))
    - COLON
    - LINES
    + ENDLOC
).setParseAction(Else)

IF = (
    INDENT
    + Suppress(Literal('if')).addParseAction(lambda: Node.set_last_statement(If))
    - OPERATION
    - COLON
    - LINES
    - Group(ZeroOrMore(ELSEIF) + Optional(ELSE))
    - END
    + ENDLOC
).setParseAction(If)

"""-----------------LOOP----------------------------"""
class While(Node):
    def __init__(self, src, start, tokens):
        super().__init__(src, start, tokens)

        # print("while condition", tokens[0])
        self.condition = tokens[0]
        self.body = tokens[1].asList()

    def to_python(self, gen, *_):
        condition = self.condition.to_python(gen)
        output = f'while {condition}:\n'

        gen.indent()

        for node in self.body:
            output += gen.tabs() + node.to_python(gen) + '\n'

        gen.dedent()

        return output

    def typecheck(self, ctx):
        _, co = self.condition.signature(ctx)

        return ctx.unify(self.condition, co, bool) and all([node.typecheck(ctx) for node in self.body])

    @property
    def used_vars(self):
        vars = {var for node in self.body
                    for var in node.used_vars}

        vars = vars.union(self.condition.used_vars)

        return vars

BLOQUEWHILE = (
    INDENT
    + Suppress(Literal('while')).addParseAction(lambda: Node.set_last_statement(While))
    - OPERATION
    - COLON
    - LINES
    - END
    + ENDLOC
).setParseAction(While)

"""-----------------WHEN+CONDICION------------------"""
class When(Node):
    def __init__(self, src, start, tokens):
        super().__init__(src, start, tokens)

        self.name = tokens[0]
        self.right = tokens[1] if len(tokens) == 3 else None
        self.body = tokens[-1].asList()

    def to_python(self, gen, *_):
        name = self.name.to_python(gen)

        if name != 'start':
            output = f'{name}_start = time.time()\n'
            output += gen.tabs() + f'state_{name} = False\n'
            output += gen.tabs() + f'time_{name} = 0\n'
            output += gen.tabs() + f'def when_{name}():\n'
        else:
            output = f'def when_{name}():\n'

        globals = {var for var in self.used_vars
                       if gen.is_global(var)}

        globals.add(f'time_{name}')
        globals.add(f'state_{name}')
        globals.add(f'{name}_start')

        for when in gen.whens:
            if when in self.used_vars and when not in globals:
                globals.add(f'time_{when}')
                globals.add(f'state_{when}')
                globals.add(f'{when}_start')

        gen.indent()

        if globals:
            output += gen.tabs() + 'global ' + ', '.join(globals) + '\n'

        if name != 'start':
            output += gen.tabs() + f'if time_{name} == 0:\n'

            gen.indent()
            output += gen.tabs() + f'{name}_start = time.time()\n'
            gen.dedent()

            output += gen.tabs() + f'if state_{name}:\n'
            gen.indent()

        for node in self.body:
            output += gen.tabs() + node.to_python(gen) + '\n'

        if name != 'start':
            output += gen.tabs() + f'time_{name} = time.time() - {name}_start\n'
            gen.dedent()
            output += gen.tabs() + f'if not state_{name}:\n'

            gen.indent()
            output += gen.tabs() + f'time_{name} = 0\n'
            gen.dedent()

        gen.dedent()

        return output.strip()

    def typecheck(self, ctx):
        if self.right is None:
            return True
        else:
            _, co = self.right.signature(ctx)

            return ctx.unify(self.right, co, bool) and all([node.typecheck(ctx) for node in self.body])
 
    @property
    def used_vars(self):
        vars = {var for node in self.body
                    for var in node.used_vars}

#        vars = vars.union(self.condition.used_vars)

        return vars


BLOQUEWHENCOND = (
    INDENT
    + Suppress(Literal('when')).addParseAction(lambda: Node.set_last_statement(When))
    - IDENTIFIER
    - Optional(
        Suppress(ASSIGN)
        - OPERATION
    )
    - COLON
    - LINES
    - END
    + ENDLOC
).setParseAction(When)

"""-----------------ACTIVATE-CONDITION----------------"""
class Activate(Node):
    def __init__(self, src, start, tokens):
        super().__init__(src, start, tokens)
        self.name = tokens[0].name

    def to_python(self, gen, *_):
        return f'state_{self.name} = True'
    
    @property
    def used_vars(self):
        return {f'state_{self.name}'}


class Deactivate(Node):
    def __init__(self, src, start, tokens):
        super().__init__(src, start, tokens)
        self.name = tokens[0].name

    def to_python(self, gen, *_):
        return f'state_{self.name} = False'

    @property
    def used_vars(self):
        return {f'state_{self.name}'}


ACTIVATE = (
    Suppress(Literal('activate')).addParseAction(lambda: Node.set_last_statement(Activate))
    - IDENTIFIER
    + ENDLOC
).setParseAction(Activate)

DEACTIVATE = (
    Suppress(Literal('deactivate')).addParseAction(lambda: Node.set_last_statement(Deactivate))
    - IDENTIFIER
    + ENDLOC
).setParseAction(Deactivate)

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
class Def(Node):
    def __init__(self, src, start, tokens):
        super().__init__(src, start, tokens)

        self.name = tokens[0]
        self.body = tokens[1].asList()

    def to_python(self, gen, *_):
        name = self.name.to_python(gen)
        output = f'def {name}():\n'

        gen.indent()

        globals = {var for var in self.used_vars
                       if gen.is_global(var)}

        if globals:
            output += gen.tabs() + 'global ' + ', '.join(globals) + '\n'

        for node in self.body:
            output += gen.tabs() + node.to_python(gen) + '\n'

        gen.dedent()

        return output

    def typecheck(self, ctx):
        return all([node.typecheck(ctx) for node in self.body])

    @property
    def used_vars(self):
        return {var for node in self.body
                    for var in node.used_vars}

DEF = (
    Suppress(Literal('def')).addParseAction(lambda: Node.set_last_statement(Def))
    - IDENTIFIER
    - OPAR
    - CPAR
    - COLON
    - LINES
    - END
    + ENDLOC
).setParseAction(Def)

"""-----------------IMPORT----------------------------"""
class Import(Node):
    def __init__(self, src, start, tokens):
        super().__init__(src, start, tokens)
        self.path = tokens[0][0]

    def to_python(self, gen, *_):
        gen.imports += self.path

        return ''

IMPORT = (
    Suppress(Literal('import')).addParseAction(lambda: Node.set_last_statement(Import))
    - STRING
    + ENDLOC
).setParseAction(Import)

"""-----------------MAIN----------------------------"""
class Main(Node):
    def __init__(self, src, start, tokens):
        super().__init__(src, start, tokens)
        self.body = tokens[0].asList()

    def to_python(self, gen, *_):
        output = ''

        for node in self.body:
            output += gen.tabs() + node.to_python(gen) + '\n'

        return output

    def typecheck(self, ctx):
        return all([node.typecheck(ctx) for node in self.body])

    @property
    def used_vars(self):
        return {var for node in self.body
                    for var in node.used_vars}

MAIN = (
    Suppress(Literal('main')).addParseAction(lambda: Node.set_last_statement(Main))
    - COLON
    - LINES
    - END
    + ENDLOC
).setParseAction(Main)

class Program(Node):
    def __init__(self, src, start, tokens):
        super().__init__(src, start, tokens)

        self.imports = tokens[0].asList()
        self.inits = tokens[1].asList()
        self.defs = tokens[2].asList()
        self.blocks = tokens[3].asList()

    def to_python(self, gen, *_):
        output = ''

        for node in self.nodes:
            output += gen.tabs() + node.to_python(gen) + '\n'

        return output

    def typecheck(self, ctx):
        return all([node.typecheck(ctx) for node in self.nodes])

    @property
    def used_vars(self):
        return {var for node in self.inits + self.defs + self.blocks
                    for var in node.used_vars}

    @property
    def nodes(self):
        return self.imports + self.inits + self.defs + self.blocks

LB = (
    Group(ZeroOrMore(IMPORT))
    - Group(ZeroOrMore(LINE))
    - Group(ZeroOrMore(DEF))
    - Group(MAIN | ZeroOrMore(BLOQUEWHENCOND))
    + ENDLOC
).setParseAction(Program)

LB.ignore(pythonStyleComment)

# We use infixNotation, so performance without this is HORRIBLE
# enablePackrat makes use of the Packrat method for parsing, which recognizes
# and memoizes repeating patterns so they are not re-evaluated each time.
#
# See: github.com/pyparsing/pyparsing/wiki/Performance-Tips
LB.enablePackrat()

# So that location-based indexing in the source code works (without this, the
# `loc` parameter expands tabs, so positions are moved to the right when a tab
# is found)
LB.parseWithTabs()

class Context:
    def __init__(self, operators):
        self.operators = operators
        self.globals = {}

    def precedence_of(self, name, klass):
        """Find the binding precedence of a given operator in the operator table"""

        entry = self.lookup_operator(name, klass)
        return self.operators.index(entry)

    def lookup_operator(self, name, klass):
        """Lookup an operator in the operator table"""

        return next(entry for entry in self.operators
                          if entry[3] == klass
                          and entry[0].searchString(name))

    def operator_signature(self, name, klass):
        """Return the inputs and output type of the given operator"""

        entry = self.lookup_operator(name, klass)
        return entry[4], entry[5]

    def is_global(self, name):
        """Tells whether a variable is in the global context or not"""

        return name in self.globals

    def lookup(self, name):
        """Returns the signature associated with the given variable"""

        return self.globals[name]

    def update_signature(self, name, signature):
        """Updates the signature associated with the given variable"""

        self.globals[name] = signature

class PythonGenerator(Context):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.imports = []
        self.whens = []
        self.level = 0

    def indent(self):
        """Enter an indentation level"""

        self.level += 1

    def dedent(self):
        """Leave an indentation level"""

        self.level -= 1

    def tabs(self):
        """Returns the current indentation level as tabs"""

        return '<TABHERE>' * self.level

    @staticmethod
    def generate(tree):
        instance = PythonGenerator(OPTABLE)

        # Right now all variables are global, so any variable used in the code
        # will be found in this list. However this can change in the future,
        # so we won't assume every variable usage is global (although we'll
        # make it happen for now). Future-proofing!
        instance.globals = {var: ([], True) for var in tree.used_vars}
        instance.whens = {node.name.to_python(instance): node
                          for node in tree.blocks
                          if isinstance(node, When)}

        body = tree.to_python(instance)

        output = ''

        if instance.imports:
            output += f'imports = {instance.imports}'
            output += loadLibraryCode

        output += body

        if instance.whens:
            if 'start' in instance.whens:
                output += 'when_start()\n'

            output += 'while True:\n'
            instance.indent()

            inis = [instance.tabs() + f'state_{name} = ' + node.right.to_python(instance) + '\n'
                    for name, node in instance.whens.items()
                    if node.right]

            calls = [instance.tabs() + f'when_{name}()\n'
                     for name in instance.whens
                     if name != 'start']

            output += '\n'.join(inis)
            output += '\n'.join(calls)

            if not inis + calls:
                output += instance.tabs() + 'pass\n'

            instance.dedent()

        return (output
                .strip()
                .replace('<TABHERE>', '\t'))

class Typechecker(Context):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.mismatches = []

    def unify(self, node, a, b):
        if a == True:
            return b
        elif b == True:
            return a
        elif a and b and a == b:
            return a
        else:
            self.mismatches.append((node, a, b))
            return None

    @staticmethod
    def check(tree):
        instance = Typechecker(OPTABLE)

        # Right now all variables are global, so any variable used in the code
        # will be found in this list. However this can change in the future,
        # so we won't assume every variable usage is global (although we'll
        # make it happen for now). Future-proofing!
        instance.globals = {var: ([], True) for var in tree.used_vars}
        print("GLOBALS", instance.globals)
        tree.typecheck(instance)

        return instance.mismatches

class Parser:
    @staticmethod
    def parse_str(text):
        return LB.parseString(text, parseAll = True)[0]

# ini = []
usedFunctions = []

def parserLearntBotCodeOnlyUserFuntion(code):
    text = ""
    # TODO: check for notifications
    try:
        tree = Parser.parse_str(code)
        text = PythonGenerator.generate(tree)
    except Exception as e:
        traceback.print_exc()
    return text

def parserLearntBotCode(inputFile, outputFile, client_name):
    global usedFunctions

    notifications = []

    with open(inputFile) as f:
        code = f.read()

        try:
            output = Parser.parse_str(code)
            mismatches = [] #Typechecker.check(output)

            text = elapsedTimeFunction.replace("<TABHERE>", '\t')
            text += signalHandlerFunction.replace("<TABHERE>", '\t')
            text += PythonGenerator.generate(output)
            text += endOfProgram

            for mismatch in mismatches:
                node, got, expected = mismatch

                notifications.append(TypeMismatch(
                    src = code,
                    start = node.start,
                    end = node.end,
                    expected = expected.__name__,
                    got = got.__name__
                ))

            header = HEADER.replace('<Client>', client_name).replace("<USEDCALLS>", str(usedFunctions)).replace("<TABHERE>", '\t')

            with open(outputFile, 'w') as f:
                f.write(header)
                f.write(text)

            return header + text, notifications
        except ParseSyntaxException as pe:
            traceback.print_exc()

            print("=================================")
            print("ParseSyntaxException 1")
            print("=================================")
            print(pe.__dict__)

            notifications.append(InvalidSyntax(
                src = code,
                start = (pe.lineno, pe.col, pe.loc)
            ))
            return None, notifications
        except ParseException as pe:
            traceback.print_exc()

            notifications.append(InvalidSyntax(
                src = code,
                start = (pe.lineno, pe.col, pe.loc)
            ))
            return None, notifications

def parserLearntBotCodeFromCode(code, name_client):
    global usedFunctions

    notifications = []

    try:
        output = Parser.parse_str(code)
        mismatches = [] #Typechecker.check(output)

        text = elapsedTimeFunction.replace("<TABHERE>", '\t')
        text += signalHandlerFunction.replace("<TABHERE>", '\t')
        text += PythonGenerator.generate(output)
        text += endOfProgram
        header = HEADER.replace('<Client>', name_client).replace("<USEDCALLS>", str(usedFunctions)).replace("<TABHERE>", '\t')

        for mismatch in mismatches:
            node, got, expected = mismatch

            notifications.append(TypeMismatch(
                src = code,
                start = node.start,
                end = node.end,
                expected = expected.__name__,
                got = got.__name__
            ))

        return header + text, notifications
    except ParseSyntaxException as pe:
        traceback.print_exc()

        notifications.append(InvalidSyntax(
            src = code,
            start = (pe.lineno, pe.col, pe.loc),
            rule = Node.last_statement()
        ))
        return None, notifications
    except ParseException as pe:
        traceback.print_exc()
        notifications.append(InvalidSyntax(
            src = code,
            start = (pe.lineno, pe.col, pe.loc),
            rule = Node.last_statement()
        ))
        return None, notifications

if __name__ == "__main__":
    textprueba = """


main:
    x = 2
end

"""
    try:
        print("Original source code")
        print("====================")
        print()
        print(textprueba)
        print()

        print("Parse tree")
        print("==========")
        print()
        tree = Parser.parse_str(textprueba)
        print(tree.__dict__)
        print()

        print("Global variables")
        print("================")
        print()
        print(tree.used_vars)
        print()

        print("Python result")
        print("=============")
        print()
        print(PythonGenerator.generate(tree))
        print()

        print("Typechecks?")
        print("==========")
        print()
        mismatches = Typechecker.check(tree)
        print(not mismatches)
        print()

        print("Type mismatches")
        print("===============")
        print()
        print(mismatches)
        print()
        parserLearntBotCodeFromCode(textprueba, "robots")
    except Exception as pe:
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
    text += PythonGenerator.generate(Parser.parse_file(argv[0]))
    print(bcolors.OKGREEN + "Generating file " + argv[1] + "\t[100%]" + bcolors.ENDC)

    with open(argv[1], 'w') as f:
        f.write(text)
