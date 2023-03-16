from pparser import Parser
from lexer import MyLex


lex = MyLex()

par = Parser()


@par.rule("SHOUT")
def expr(ts):
    return ("SHOUT",)


@par.rule(
    "NUM",
    "ID",
)
def expr(ts):
    return "dt", ts[0]


@par.rule("expr OP expr", "expr OP NUM", "NUM OP expr", "NUM OP NUM")
def expr(ts):
    return ts


@par.rule(
    "expr OP expr",
)
def expr(ts):
    return ts


stream = lex.tokenize("9.9 + 699 +")


print(par.parse(stream))
