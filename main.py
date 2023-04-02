from __future__ import annotations

from hanual.lang.nodes import BinOpNode, FunctionCall, AssighnmentNode, FreezeNode

from hanual.lang.productions import DefaultProduction
from hanual.lang.builtin import HanualLexer
from hanual.lang.pparser import PParser

lex = HanualLexer()
par = PParser()


@par.rule("NUM OP NUM")
def expr(ts: DefaultProduction):
    return BinOpNode(op=ts[1], left=ts[0], right=ts[2])


@par.rule("expr OP NUM")
def expr(ts):
    return BinOpNode(ts[1], ts[0], ts[2])


@par.rule("ID LPAR expr RPAR", "ID LPAR ID RPAR")
def f_call(ts):
    return FunctionCall(ts[0], ts[2])


@par.rule("LET ID EQ NUM")
def assighnment(ts):
    return AssighnmentNode(target=ts[1], value=ts[3])


@par.rule("FREEZE ID")
def freeze(ts):
    return FreezeNode(ts[1])


print(
    par.parse(
        lex.tokenize(
            """
let x = 100
freeze x

print(x)
"""
        )
    )
)
