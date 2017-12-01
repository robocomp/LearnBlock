#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------
#   TODO Añadir definition de funciones.
#
#
# ------------------------------------------------------------------

from pyparsing import *
import sys

header = """

# EXECUTION: python code_example.py configSimulated

global lbot
lbot = LearnBotClientPR.Client(sys.argv)


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

OBRACE,CBRACE,SEMI,OPAR,CPAR = map(Literal, "{};()")

reserved_words = ( Keyword('>=') | Keyword('<=') | Keyword('<') | Keyword('>') | Keyword('deactive') | Keyword('active') | Keyword('not') | Keyword('True') | Keyword('False') | Keyword('or') | Keyword('and') | Keyword('main') | Keyword('if') | Keyword('else') | Keyword('elif') | Keyword('when') | Keyword('while') | Keyword('end'))
iden = Word( alphanums+"_")
identifier = Group( ~reserved_words + iden ).setResultsName( "IDENTIFIER" )
NUMS = Group( Word( nums ) ).setResultsName( "NUMBER" )

QUOTE = Word( "\"" )
OR    = Word( "or" )
AND   = Word( "and" )
NOT   = Word( "not" ).setResultsName( 'NOT' )
plus  = Word( "+" )
minus = Word( "-" )
mult  = Word( "*" )
div   = Word( "/" )
lpar  = Word( "(" )
rpar  = Word( ")" )
TRUE  = Group( Word( "True" ) ).setResultsName( 'TRUE' )
FALSE = Group( Word( "False" ) ).setResultsName( 'FALSE' )
eq    = Word( "=" )
point    = Word( "." )
coma    = Word( "," )
COLONS= Suppress(Word( ":" ))
SEMICOL= Word( ";" )




L      = Literal( "<" )
NL     = Literal( ">" )
LE     = Literal( "<=" )
NLE    = Literal( ">=" )
E      = Literal( "==" )
NE     = Literal( "!=" )
END    = Literal( "end" )
SECTAB = ZeroOrMore("\t")

"""-----------------COMPARACIONES-------------------"""
COMP  = Group( L | NL | LE | NLE | E | NE ).setResultsName( "COMP" )

"""-----------------OPERADORES----------------------"""
SRMD  = Group( plus | minus | mult | div ).setResultsName( "SRMD" )

"""-----------------OPERACIONES---------------------"""
OPERATION = Group( identifier + ZeroOrMore( SRMD + identifier ) ).setResultsName( "OPERATION" )

"""-----------------OPERACIONES---------------------"""
ORAND = Group( OR | AND ).setResultsName( 'ORAND' )

"""-----------------FUNTION-------------------------"""
FUNTION = Forward()

"""-----------------CONDICIONES---------------------"""
COMPOP = Group( OPERATION + COMP + OPERATION ).setResultsName( "COMPOP" )
OPTIONCONDITION =  COMPOP | FUNTION |identifier | TRUE | FALSE
SIMPLECONDITION = Group( Optional( NOT ) + OPTIONCONDITION ).setResultsName( "SIMPLECONDITION")
CONDITION = Group( SIMPLECONDITION + ZeroOrMore( ORAND + SIMPLECONDITION ) ).setResultsName( "CONDITION" )

"""-----------------asignacion-VARIABLES------------"""
CHAINBETTENQUOTE = Group( QuotedString( '"' ) ).setResultsName( "STRING" )
ASSIGSTRING = Group( ( CHAINBETTENQUOTE | NUMS ) + ZeroOrMore( SRMD + ( CHAINBETTENQUOTE | NUMS ) ) ).setResultsName( 'ASSIGSTRING' )
NUMVAR    = Group( SECTAB + identifier.setResultsName( "name" ) + Suppress( eq ) + OPERATION ).setResultsName( "NUMVAR" )
BOOLVAR   = Group( SECTAB + identifier.setResultsName( "name" ) + Suppress( eq ) + CONDITION ).setResultsName( "BOOLVAR" )
STRINGVAR = Group( SECTAB + identifier.setResultsName( "name" ) + Suppress( eq ) + ASSIGSTRING ).setResultsName( "STRINGVAR")   # Solved error var =  0

"""-----------------LINEA---------------------------"""
LINE   = Forward()
LINES  = Group( LINE + ZeroOrMore( LINE ) )

"""-----------------bloque-IF-----------------------"""
ELSE   = Forward()
ELSEIF  = Forward()
INIF   = LINES  &    ( ZeroOrMore( ELSEIF ) + Optional( ELSE ) )

ELSEIF << Group( SECTAB + Suppress( Literal( "elif" ) ) + Group( CONDITION ).setResultsName('condition') + COLONS + LINES.setResultsName('content') ).setResultsName( "ELIF" )
ELSE   << Group( SECTAB + Suppress( Literal( "else" ) ) +                                                  COLONS + LINES.setResultsName('content') ).setResultsName( "ELSE" )
IF     =  Group( SECTAB + Suppress( Literal( "if"   ) ) + Group( CONDITION ).setResultsName('condition') + COLONS + LINES.setResultsName('content')  + Group( ZeroOrMore( ELSEIF ) + Optional( ELSE ) ).setResultsName( "OPTIONAL" ) + Suppress( Literal( "end" ) ) ).setResultsName( "IF" )

"""-----------------LOOP----------------------------"""
BLOQUEWHILE    = Group( SECTAB + Suppress( Literal( "while" ) ) + Group( CONDITION ).setResultsName('condition') + COLONS + LINES.setResultsName('content') + Suppress( Literal("end") ) ).setResultsName("WHILE")

"""-----------------WHEN+CONDICION------------------"""
BLOQUEWHENCOND = Group( SECTAB + Suppress( Literal( "when" ) ) + identifier.setResultsName("name") + Optional( Suppress( eq )+ Group( CONDITION ).setResultsName( 'condition' ) ) + COLONS + LINES.setResultsName('content') + Literal("end") ).setResultsName( "WHEN" )

"""-----------------ACTIVE-CONDITION----------------"""
ACTIVE   = Group( Suppress( Literal( "active" ) ) + identifier.setResultsName( "name" ) ).setResultsName( "ACTIVE" )
DEACTIVE = Group( Suppress( Literal( "deactive" ) ) + identifier.setResultsName( "name" ) ).setResultsName( "DEACTIVE" )

"""-----------------FUNTION-------------------------"""
FUNTION = Group( Suppress( Literal( "function" ) ) + Suppress( point ) + identifier.setResultsName( 'name' ) + Suppress( lpar ) + Group( Optional( identifier ) + ZeroOrMore( Suppress( coma ) + identifier) ).setResultsName( "args" ) + Suppress( rpar )).setResultsName( "FUNCTION" )

"""-----------------LINEA---------------------------"""
LINE << ( FUNTION | IF | BLOQUEWHILE | NUMVAR | BOOLVAR | ACTIVE | DEACTIVE | STRINGVAR )

"""-----------------DEF----------------------------"""
# DEF = Group().setResultsName( "DEF" ) # TODO

"""-----------------MAIN----------------------------"""
MAIN = Group( Suppress( Literal( "main" ) ) + COLONS + LINES.setResultsName( 'content' ) ).setResultsName( "MAIN" )
LB = MAIN | ZeroOrMore(BLOQUEWHENCOND)
LB.ignore( pythonStyleComment )




def parserFromFile(file):
    with open(file) as f:
        text = f.read()
        return parserFromString(text)

def parserFromString(text):
    try:
        return LB.parseString(text)
    except Exception as e:
        print bcolors.FAIL + e
        print("line: {}".format(e.line))
        print("    "+" "*e.col+"^") + bcolors.ENDC
        exit(-1)

def generatePy(lines):
    list_var = []
    # print "-------------------\n", lines, "\n-------------------"
    text = ""
    for x in lines:
        if x.getName() is 'WHEN':
            list_var.append(x.name[0])
    for x in lines:
        text = process(x,list_var,text)
    if len( list_var ) is not 0:
        text += "while True:\n"
        for x in list_var:
            text += "\twhen_" + x + "()\n"
    # print "-----Final text------\n", text
    return text

def process(line, list_var=[], text="", index=0):
    # print "------------Procesando ",line
    TYPE = line.getName()
    # print "\t",TYPE, index

    if TYPE is 'MAIN':
        for cLine in line.content:
            text += process(cLine, [], "",0)
    elif TYPE is 'WHEN':
        text = processWHEN(line, list_var, text)
    elif TYPE is 'WHILE':
        text = processWHILE(line,text,index)
    elif TYPE is 'IF':
        text = processIF(line,text,index)
    elif TYPE is 'ELIF':
        text = processELIF(line,text,index)
    elif TYPE is 'ELSE':
        text = processELSE(line,text,index)
    elif TYPE is 'ACTIVE':
        text = processACTIVE(line, text, index)
    elif TYPE is 'DEACTIVE':
        text = processDEACTIVE(line, text, index)
    elif TYPE in ['NUMVAR', 'BOOLVAR', 'STRINGVAR']:
        text = processASSIG(line, text, index)
    elif TYPE is 'OPERATION':
        text = processOP(line, text, index)
    elif TYPE is 'FUNCTION':
        text = processFUNCTION(line, text, index)
    elif TYPE is 'CONDITION':
        text = processCONDITION(line, text, index)
    elif TYPE is 'ASSIGSTRING':
        text = processASSIGSTRING(line, text, index)
    elif TYPE in ['FALSE','TRUE','IDENTIFIER', 'SRMD']:
        text = line[0]
    elif TYPE is 'SIMPLECONDITION':
        text = processSIMPLECONDITION(line, text, index)
    return text

def processFUNCTION(line, text="", index=0):
    if text is not "":
        text += "\t"*index
    text += "functions.get(" + line.name[0] + ")(lbot"
    for x in line.args:
        text += ", "+ x[0]
    text += ")"
    return text

# ---------------------------------------
# Process NUMVAR, BOOLVAR, STRINGVAR
# ---------------------------------------

def processASSIG(line, text="", index=0):
    # print "------------------------processASSIG-----", line[1]
    text += "\t"*index + line.name[0] + " = " + process(line[1])
    return text

def processASSIGSTRING(line, text="", index=0):
    for field in line:
        if field.getName() is 'STRING':
            text += "\"" + field[0] + "\" "
        elif field.getName() is 'NUMBER':
            text += "str(" + field[0] + ") "
        else:
            text += field[0] + " "
    return text

def processACTIVE(line, text="", index=0):
    text += "\t"*index + line.name[0] + " = True\n"
    return text

def processDEACTIVE(line, text="", index=0):
    text += "\t"*index + line.name[0] + " = False\n"
    return text

def processWHILE(line, text="", index=0):
    text += "\t"*index + "while "
    for c in line.condition:
        text += process(line.condition[0])
    text += ":\n"

    index+=1
    for field in line.content:
        text = process(field, [], text, index) + "\n"

    index-=1
    return text

def processWHEN(line, list_var, text="", index=0):
    text += "def when_" + str(line.name[0]) + "():\n"
    index += 1
    for x in list_var:
        text += "\t"*index + "global " + x + "\n"
    text += "\t"*index + "if " + str(line.name[0]) + ":\n"
    index += 1
    for cline in line.content:
        # print "\n\n------------------------ \n",cline "\n\n\n---------------------------------\n\n\n"
        text = process(cline, [], text, index) + "\n"
    index-=1
    ini = line.name[0] + " = "
    if line.condition is not "":
        ini += process(line.condition[0])
    else:
        ini += "False"
    ini +="\n"

    text = ini + text
    return text

def processOP(line, text="", index=0):
    # print "------------------------processOP------------"
    for field in line:
        text += field[0] + " "
    # print "-----------------------end-processOP------------"
    return text

def processCOMPOP(line, text="", index=0):
    for field in line:
        TYPE = field.getName()
        if TYPE is 'OPERATION':
            text += process(field)
        elif TYPE is 'COMP':
            text += field[0] + " "
    return text

def processSIMPLECONDITION(line, text="", index=0):
    # print "------------------------", line
    for field in line:
        TYPE = field.getName()
        if TYPE is 'NOT':
            text += "not "
        elif TYPE in ['IDENTIFIER','FUNCTION','TRUE','FALSE']:
            text += process(field)
        elif TYPE is "COMPOP":
            text += processCOMPOP(field)
        # else:
            # text += field
    return text

def processCONDITION(line, text="", index=0):
    for field in line:
        if field.getName() is 'SIMPLECONDITION':
            text += process(field) + " "
        elif field.getName() is 'ORAND':
            text += field[0] + " "
    return text

def processELIF(line, text="", index=0):
    text += "\t"*index + "elif "
    for c in line.condition:
        text += process(line.condition[0])
    text += ":\n"
    index+=1
    for field in line.content:
        text = process(field, [], text, index) + "\n"
    return text

def processELSE(line, text="", index=0):
    text += "\t"*index + "else:\n"
    index+=1
    for field in line.content:
        text = process(field, [], text, index) + "\n"
    return text

def processIF(line, text="", index=0):
    text += "\t"*index + "if "
    for c in line.condition:
        text += process(line.condition[0])
    text += ":\n"

    index+=1
    for field in line.content:
        text = process(field, [], text, index) + "\n"

    index-=1
    for field in line.OPTIONAL:
        text = "\t"*index + process(field, [], text, index)
    return text

if __name__ == "__main__":
    argv = sys.argv[1:]
    if len( argv ) is not 2:
        print bcolors.FAIL + "You must give 2 arguments"
        print "\timputfile\tFile to parser"
        print "\toutputfile\tFile to parser" + bcolors.ENDC
        exit(-1)
    if argv[0] == argv[1]:
        print bcolors.FAIL + "Imputfile must be different to outputfile" + bcolors.ENDC
        exit(-1)
    print bcolors.OKGREEN + "Generating file " + argv[1] + bcolors.ENDC
    text = generatePy( parserFromFile( argv[0] ) )
    print bcolors.OKGREEN + "Generating file " + argv[1] + "\t[100%]" + bcolors.ENDC
    with open( argv[1] ,'w') as f:
        f.write( header )
        f.write( text )
