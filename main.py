from __future__ import annotations

from hanual.lang.nodes import (
    FunctionDefinition,
    AssighnmentNode,
    FunctionCall,
    IfStatement,
    FreezeNode,
    BinOpNode,
    Condition,
    CodeBlock,
    Arguments,
)

from hanual.lang.preprocess.preprocesser import PrePeoccesser
from hanual.lang.productions import DefaultProduction
from hanual.lang.builtin import HanualLexer
from hanual.lang.pparser import PParser
from typing import Any

pre = PrePeoccesser()
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
    "ID LPAR RPAR",  # NO ARGS
    "ID LPAR expr RPAR",
    "ID LPAR ID RPAR",
    "ID LPAR STR RPAR",
    "ID LPAR arg RPAR",
    types={"ID LPAR args RPAR": 1, "ID LPAR RPAR": 2},
)
def f_call(ts: DefaultProduction, case):
    if case is None:  # single arg
        return FunctionCall(ts[0], Arguments(ts[2]))

    elif case == 1:  # multiple args
        return FunctionCall(ts[0], ts[2])

    elif case == 2:  # no args
        return FunctionCall(ts[0], None)


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


@par.rule("FN f_call")
def function_marker(ts: DefaultProduction):
    return ts[1]


@par.rule(
    "function_marker END",
    "function_marker line END",
    "function_marker lines END",
    types={
        "function_marker END": False,
    },
)
def function_definition(ts: DefaultProduction[FunctionCall], hasend: bool):
    if hasend is False:
        return FunctionDefinition(name=ts[0].name, args=ts[0].args, inner=None)

    return FunctionDefinition(name=ts[0].name, args=ts[0].args, inner=ts[1])


@par.rule("f_call", "assighnment", "if_statement", "freeze", "function_definition")
def line(ts):
    return CodeBlock(ts[0])


@par.rule("line line", "line lines", "lines line")
def lines(ts: DefaultProduction[CodeBlock, Any]):
    return ts[0].add_child(ts[1])


print(par.parse(lex.tokenize(pre.process(...))))
