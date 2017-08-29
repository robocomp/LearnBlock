


from pyparsing import Word, alphas, alphanums, nums, OneOrMore, CharsNotIn, Literal, Combine
from pyparsing import cppStyleComment, Optional, Suppress, ZeroOrMore, Group, StringEnd, srange
from pyparsing import nestedExpr, CaselessLiteral,ParseException

semicolon = Suppress(Word(";"))
quote     = Suppress(Word("\""))
op        = Suppress(Word("{"))
cl        = Suppress(Word("}"))
opp       = Suppress(Word("("))
clp       = Suppress(Word(")"))

identifier = Word( alphas+"_-+*/=><()", alphanums+"/-_.+*/=><()" )

type = Suppress(Word("type")) + identifier
file = Suppress(Word("file")) + identifier
img = Group(Suppress(Word("img")) + identifier + ZeroOrMore(Suppress(",")+identifier))
name = Suppress(Word("name"))+identifier
typeblock = Suppress(Word("blocktype"))+identifier
var = identifier.setResultsName("type")+identifier.setResultsName("varName") + Word(nums).setResultsName("defaultValue")
variables = Suppress(Word("variables"))+op+ Group(var)+ZeroOrMore(Group(var))+cl

block = Group(CaselessLiteral("block") + op + Group(type.setResultsName("type") + name.setResultsName("name") +
                                      file.setResultsName("file") + Optional(variables.setResultsName("variables")) +
                                      img.setResultsName("img") + cl))

parser = block + ZeroOrMore(block)

config = """

block{
    type operador
    name +
    file None
    img blocks/block4, blocks/block3
    blocktype simple
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


def parserConfigBlock(file):
    fh = open(file, "r")
    text = fh.read()
    fh.close()
    r =[]
    try:
        r=parser.parseString(text)
    except ParseException as pe:
        print(pe)
    return r
