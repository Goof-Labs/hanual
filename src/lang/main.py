from nodes.binop import BinOpNode
from lexer import MyLex, Token
from pparser import PParser
from typing import List


lex = MyLex()

par = PParser()
# par.tougle_debug_messages(True)


@par.rule("NUM", "ID")
def expr(t):
    return t[0].value


@par.rule("expr OP expr")
def expr(l: List[Token]):
    return l[1].value, l[0], l[2]


stream = lex.tokenize("9.9 + 699")


print("END ", par.parse(stream))
