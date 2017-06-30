


from pyparsing import Word, alphas, alphanums, nums, OneOrMore, CharsNotIn, Literal, Combine
from pyparsing import cppStyleComment, Optional, Suppress, ZeroOrMore, Group, StringEnd, srange
from pyparsing import nestedExpr, CaselessLiteral

semicolon = Suppress(Word(";"))
quote     = Suppress(Word("\""))
op        = Suppress(Word("{"))
cl        = Suppress(Word("}"))
opp       = Suppress(Word("("))
clp       = Suppress(Word(")"))

identifier = Word( alphas+"_", alphanums+"/-_." )
"""vars = Optional( + ZeroOrMore(Suppress(Word(","))))
Pfunctions = identifier.setResultsName('namefuntion') + opp + vars.setResultsName('vars') + clp

commIdentifier = Group(identifier.setResultsName('identifier'))

code = Group(Suppress(Word("code")) + op + ZeroOrMore(identifier) +cl)
f = Pfunctions+code
"""
config = """
get_distance1{
    type control
    name get_distance
    file learnbot-dsl/funtions/get_distance.py
    variables{
        int distance
    }
    img blocks/block4.png, blocks/block3.png
}
get_distance1{
    type control
    name get_distance
    file learnbot-dsl/funtions/get_distance.py
    variables{
        int distance
    }
    img blocks/block4.png, blocks/block3.png
}
"""
type = Suppress(Word("type")) + identifier
file = Suppress(Word("file")) + identifier
img = Group(Suppress(Word("img")) + identifier + ZeroOrMore(Suppress(",")+identifier))
name = Suppress(Word("name"))+identifier
typeblock = Suppress(Word("blocktype"))+identifier
var = identifier.setResultsName("type")+identifier.setResultsName("varName")
variables = Suppress(Word("variables"))+op+ Group(var)+ZeroOrMore(Group(var))+cl

block = Group(identifier + op + Group(type.setResultsName("type") + name.setResultsName("name") +
                                      file.setResultsName("file") + Optional(variables.setResultsName("variables")) +
                                      img.setResultsName("img") + typeblock.setResultsName("blocktype") + cl))

parser = block + ZeroOrMore(block)



def parserConfigBlock(file):
    fh = open(file, "r")
    text = fh.read()
    fh.close()
    return parser.parseString(text)