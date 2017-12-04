


from pyparsing import *

semicolon = Suppress( Word( ";" ) )
quote     = Suppress( Word( "\"" ) )
op        = Suppress( Word( "{" ) )
cl        = Suppress( Word( "}" ) )
opp       = Suppress( Word( "(" ) )
clp       = Suppress( Word( ")" ) )

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


# -------------------------IMG--------------------
img = Group( Suppress( Word( "img" ) ) + identifier + ZeroOrMore( Suppress( "," ) + identifier ) ).setResultsName( "img" )

# -------------------------name--------------------
name = Group( Suppress( Word( "name" ) ) + identifier ).setResultsName( "name" )

# -------------------------blocktype--------------------
# typeblock = Group( Suppress( Word( "blocktype" ) ) + identifier )

# -------------------------variables--------------------
var = identifier.setResultsName( "type" )+identifier.setResultsName( "varName" ) + Word( nums ).setResultsName( "defaultValue" )


variables = Suppress( Word( "variables" ) )+op+ Group( var )+ZeroOrMore( Group( var ) )+cl

block = Group( Suppress( Literal( "block" ) ) + op +  TYPE + name + Optional( variables ).setResultsName("variables") + img + Optional( translations ) + cl )

parser = block + ZeroOrMore( block )

config = """

block{
    type operador
    name +
    file None
    img blocks/block4, blocks/block3
    blocktype simple
    languages
}

block{
    type operador
    name -
    file None
    img blocks/block4, blocks/block3
    blocktype simple
}

block{
    type operador
    name *
    file None
    img blocks/block4, blocks/block3
    blocktype simple
}

block{
    type operador
    name /
    file None
    img blocks/block4, blocks/block3
    blocktype simple
}

block{
    type operador
    name =
    file None
    img blocks/block4, blocks/block3
    blocktype simple
}

"""
#print parser.parseString(config)


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
