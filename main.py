from __future__ import annotations

from hanual.lang.nodes import (
    AssighnmentNode,
    FunctionCall,
    IfStatement,
    FreezeNode,
    BinOpNode,
    Condition,
    CodeBlock,
    Arguments,
)

from hanual.lang.productions import DefaultProduction
from hanual.lang.builtin import HanualLexer
from hanual.lang.pparser import PParser
from typing import Any

lex = HanualLexer()
par = PParser()


@par.rule("NUM OP NUM")
def expr(ts: DefaultProduction):
    return BinOpNode(op=ts[1], left=ts[0], right=ts[2])


@par.rule("expr OP NUM")
def expr(ts: DefaultProduction):
    return BinOpNode(op=ts[1], left=ts[0], right=ts[2])


@par.rule("COM NUM", "COM expr", "COM f_call", "COM ID")
def arg(ts: DefaultProduction):
    return Arguments(ts[1])


@par.rule("ID arg", "expr arg", "f_call arg", "ID arg")
def arg(ts: DefaultProduction[Any, Arguments]):
    return ts[1].add_child(ts[0])


@par.rule(
    "ID LPAR expr RPAR",
    "ID LPAR ID RPAR",
    "ID LPAR STR RPAR",
    "ID LPAR arg RPAR",
    types={"ID LPAR args RPAR": True},
)
def f_call(ts: DefaultProduction, case):
    if case:  # already an argument
        return FunctionCall(ts[0], ts[2])

    return FunctionCall(ts[0], Arguments(ts[2]))


@par.rule("LET ID EQ NUM")
def assighnment(ts: DefaultProduction):
    return AssighnmentNode(target=ts[1], value=ts[3])


@par.rule("FREEZE ID")
def freeze(ts: DefaultProduction):
    return FreezeNode(ts[1])


@par.rule("ID EL NUM", "ID EL f_call", "ID EL expr")
def condition(ts: DefaultProduction):
    return Condition(op=ts[1], left=ts[0], right=ts[2])


@par.rule(
    "IF LPAR condition RPAR line END",
    "IF LPAR condition RPAR lines END",
    "IF LPAR condition RPAR END",
    types={
        "IF LPAR condition RPAR line END": 1,
        "IF LPAR condition RPAR lines END": 2,
        "IF LPAR condition RPAR END": 3,
    },
)
def if_statement(ts: DefaultProduction, case: int):
    if case == 3:
        return IfStatement(condition=ts[2], if_true=None)

    return IfStatement(condition=ts[2], if_true=ts[4])


@par.rule("f_call", "assighnment", "if_statement", "freeze")
def line(ts):
    return CodeBlock(ts[0])


@par.rule("line line", "line lines", "lines line")
def lines(ts: DefaultProduction[CodeBlock, Any]):
    return ts[0].add_child(ts[1])


print(
    par.parse(
        lex.tokenize(
            """
let x = 100
freeze x

if (x == 100)
    print("HERE")
end


print(x, x)
"""
        )
    )
)
