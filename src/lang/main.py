from pparser import Parser
from lexer import Lexer, MyLex


lex = MyLex()

par = Parser()


@par.rule("SHOUT")
def expr(ts):
    return ("SHOUT",)


# @par.rule("NUM NUM")
def expr(ts):
    return ts


@par.rule("NUM OP NUM", carry=True)
def expr(ts):
    return ts[1].value, ts[0].value, ts[2].value


@par.rule("expr OP NUM", carry=True)
def expr(ts):
    return ts[1].value, ts[0], ts[2].value


stream = lex.tokenize("SHOUT\n9.9 + 699 + 9")

# print(list(stream))

print(par.parse(stream))
