from hanual.lang.builtin_lexer import HanualLexer
from hanual.lang.pparser import PParser
from hanual.lang.nodes import BinOpNode

lex = HanualLexer()
par = PParser()


@par.rule("NUM OP NUM")
def expr(ts) -> BinOpNode:
    return BinOpNode(op=ts[1], left=ts[0], right=ts[2])


@par.rule("expr OP NUM")
def expr(ts) -> BinOpNode:
    return BinOpNode(op=ts[1], left=ts[0], right=ts[2])


@par.rule("ID LPAR expr RPAR")
def f_call(ts):
    return ts


val = par.parse(lex.tokenize("print(1 + 1)"))
print(val)
