from pparser import PParser
from lexer import MyLex


lex = MyLex()

par = PParser()
par.tougle_debug_messages(True)


@par.rule("NUM", "ID")
def expr(*ts, **kwargs):
    return ts[0]


@par.rule("expr OP expr")
def expr(*ts):
    return ts


stream = lex.tokenize("9.9 + 699")


print(par.parse(stream))

