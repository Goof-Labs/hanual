from parser import Parser
from lexer import Lexer, MyLex


lex = MyLex()

par = Parser()


@par.rule("SHOUT")
def expr(ts):
    return "SHOUT",

@par.rule("NUM NUM")
def expr(ts):
    return ts

stream = lex.tokenize("SHOUT\n69.9 69")

#print(list(stream))

print(par.parse(stream))

