from __future__ import annotations

from hanual.lang.nodes import (
    AssighnmentNode,
    FunctionCall,
    IfStatement,
    FreezeNode,
    BinOpNode,
    Condition,
    CodeBlock,
)

from hanual.lang.productions import DefaultProduction
from hanual.lang.builtin import HanualLexer
from hanual.lang.pparser import PParser
from typing import Any

lex = HanualLexer()
par = PParser()


@par.rule("NUM OP NUM")
def expr(ts: DefaultProduction, case):
    return BinOpNode(op=ts[1], left=ts[0], right=ts[2])


@par.rule("expr OP NUM")
def expr(ts: DefaultProduction, case):
    return BinOpNode(op=ts[1], left=ts[0], right=ts[2])


@par.rule("ID LPAR expr RPAR", "ID LPAR ID RPAR")
def f_call(ts: DefaultProduction, case):
    return FunctionCall(ts[0], ts[2])


@par.rule("LET ID EQ NUM")
def assighnment(ts: DefaultProduction, case):
    return AssighnmentNode(target=ts[1], value=ts[3])


@par.rule("FREEZE ID")
def freeze(ts: DefaultProduction, case):
    return FreezeNode(ts[1])


@par.rule("ID EL NUM")
def condition(ts: DefaultProduction, case):
    return Condition(op=ts[1], left=ts[0], right=ts[2])


@par.rule("IF LPAR condition RPAR")
def if_statement(ts: DefaultProduction, case):
    return IfStatement(condition=ts[2], if_true=None)


@par.rule("f_call", "assighnment", "if_statement", "freeze")
def line(ts, case):
    return CodeBlock(ts[0])


@par.rule("line line", "line lines", "lines line")
def lines(ts: DefaultProduction[CodeBlock, Any], case):
    return ts[0].add_child(ts[1])


print(
    par.parse(
        lex.tokenize(
            """
let x = 100
freeze x

if (x == 100)

print(x)
"""
        )
    )
)
