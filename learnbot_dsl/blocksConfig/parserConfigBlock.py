# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import
import os,inspect
from pyparsing import *
from learnbot_dsl.blocksConfig.blocks import pathBlocks as pathImgBlocks
pathConfig = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

semicolon = Suppress( Word( ";" ) )
quote     = Suppress( Word( "\"" ) )
op        = Suppress( Word( "{" ) )
cl        = Suppress( Word( "}" ) )
opp       = Suppress( Word( "(" ) )
clp       = Suppress( Word( ")" ) )

e = CaselessLiteral('E')
point = Literal('.')
plusorminus = Literal('+') | Literal('-')
number = Word(nums)
integer = Combine( Optional(plusorminus) + number )
# identifier = Word( alphas+"_-+*/=><()", alphanums+"/-_.+*/=><()" )

reserved_words = ( Keyword( "block" ) | Keyword( "type" ) | Keyword( "name" ) | Keyword( "file" ) | Keyword( "img" ) | Keyword( "blocktype" ) | Keyword( "languages" ) )
iden = Word( alphas+"_-+*/=><()", alphanums+"/-_.+*/=><()" )
identifier = ~reserved_words + iden


# -------------------------TYPE--------------------
TYPE = Group( Suppress( Word( "type" ) ) + identifier ).setResultsName( "type" )

# -------------------------LANGUAGE--------------------
languages = Literal( "ES" ).setResultsName( 'ES' ) | Literal( "FR" ).setResultsName( 'FR' ) | Literal( "EN" ).setResultsName( 'EN' ) | Literal( "P" ).setResultsName( 'P' )
translation  = Group( languages.setResultsName( "language" ) + Suppress( Literal( ":" ) ) + QuotedString( '"' ).setResultsName( "translation" ) )
translations = Group( Suppress( Literal( "languages" ) ) + translation + ZeroOrMore( Suppress( "," ) + translation ) ).setResultsName( 'translations' )
tooltip = Group( Suppress( Literal( "tooltip" ) ) + translation + ZeroOrMore( Suppress( "," ) + translation ) ).setResultsName( 'tooltip' )


# -------------------------IMG--------------------
img = Group( Suppress( Word( "img" ) ) + identifier + ZeroOrMore( Suppress( "," ) + identifier ) ).setResultsName( "img" )

# -------------------------name--------------------
name = Group( Suppress( Word( "name" ) ) + identifier ).setResultsName( "name" )

# -------------------------blocktype--------------------
# typeblock = Group( Suppress( Word( "blocktype" ) ) + identifier )

floatnumber = Combine( integer +
                       Optional( point + Optional(number) )
                       # +
                       # Optional( e + integer )
                     )

# -------------------------variables--------------------
var = identifier.setResultsName( "type" )+identifier.setResultsName( "varName" ) + floatnumber.setResultsName( "defaultValue" )


variables = Suppress( Word( "variables" ) )+op+ Group( var )+ZeroOrMore( Group( var ) )+cl

block = Group( Suppress( Literal( "block" ) ) + op +  TYPE + name + Optional( variables ).setResultsName("variables") + img + Optional( translations ) + Optional( tooltip ) + cl )

parser = block + ZeroOrMore( block )
parser.ignore(pythonStyleComment)

def parserConfigBlock( file ):
    fh = open( file, "r" )
    text = fh.read()
    fh.close()
    r =[]
    try:
        r=parser.parseString( text )
    except ParseException as pe:
        print( pe )
        print("line: {}".format(pe.line))
        print("    "+" "*pe.col+"^")
    return r

def reload_functions():
    functions = parserConfigBlock(os.path.join(pathConfig, "configMotor"))
    functions += parserConfigBlock(os.path.join(pathConfig, "configOthers"))
    functions += parserConfigBlock(os.path.join(pathConfig, "configControl"))
    functions += parserConfigBlock(os.path.join(pathConfig, "configPerceptual"))
    functions += parserConfigBlock(os.path.join(pathConfig, "configPropriopercetive"))
    functions += parserConfigBlock(os.path.join(pathConfig, "configOperators"))
    functions += parserConfigBlock(os.path.join(pathConfig, "configExpressions"))
    for f in functions:
        for i in range(len(f.img)):
            f.img[i] = os.path.join(pathImgBlocks, f.img[i])
    return functions
