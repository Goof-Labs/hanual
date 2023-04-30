from __future__ import annotations

from hanual.lang.nodes import (
    FunctionDefinition,
    NamespaceAcessor,
    ReturnStatement,
    AssignmentNode,
    WhileStatement,
    FunctionCall,
    IfStatement,
    FreezeNode,
    BinOpNode,
    Condition,
    CodeBlock,
    Arguments,
)

from hanual.lang.productions import DefaultProduction
from hanual.lang.builtin_lexer import Token
from hanual.lang.pparser import PParser
from typing import Any, Union

par = PParser()


@par.rule("NUM OP NUM")
def expr(ts: DefaultProduction):
    return BinOpNode(op=ts[1], left=ts[0], right=ts[2])


@par.rule("expr OP NUM")
def expr(ts: DefaultProduction):
    return BinOpNode(op=ts[1], left=ts[0], right=ts[2])


@par.rule("NSA ID")
def namespace_accessor(ts: DefaultProduction):
    return NamespaceAcessor(ts[1])


@par.rule("ID namespace_accessor")
def namespace_accessor(ts: DefaultProduction):
    return ts[1].add_child(ts[0])


@par.rule("COM NUM", "COM expr", "COM f_call", "COM ID", "COM STR")
def arg(ts: DefaultProduction):
    return Arguments(ts[1])


@par.rule(
    "ID arg",
    "expr arg",
    "f_call arg",
    "STR arg",
    "NUM arg",
    "arg arg",
)
def arg(ts: DefaultProduction):
    return ts[1].add_child(ts[0])


@par.rule(
    "ID LPAR expr RPAR",
    "ID LPAR ID RPAR",
    "ID LPAR STR RPAR",
    "ID LPAR NUM RPAR",
    "ID LPAR arg RPAR",
    "ID LPAR RPAR",
    types={"ID LPAR RPAR": True},
)
def f_call(ts: DefaultProduction, no_args: bool):
    if no_args:
        return FunctionCall(name=ts[0], arguments=Arguments([]))

    if isinstance(ts[2], Token):
        return FunctionCall(name=ts[0], arguments=Arguments(ts[2]))

    return FunctionCall(name=ts[0], arguments=Arguments(ts[2]))


@par.rule("LET ID EQ NUM", "LET ID EQ f_call", "LET ID EQ STR")
def assighnment(ts: DefaultProduction):
    return AssignmentNode(target=ts[1], value=ts[3])


@par.rule("FREEZE ID")
def freeze(ts: DefaultProduction):
    return FreezeNode(ts[1])


@par.rule("RET ID", unless=["LPAR"])
def ret(ts: DefaultProduction) -> ReturnStatement:
    return ReturnStatement(ts[1])


@par.rule("RET f_call")
def ret(ts: DefaultProduction) -> ReturnStatement:
    return ReturnStatement(ts[1])


@par.rule("ID EL NUM", "ID EL f_call", "ID EL expr", "ID EL ID", "ID EL STR")
def condition(ts: DefaultProduction):
    return Condition(op=ts[1], left=ts[0], right=ts[2])


@par.rule(
    "IF LPAR condition RPAR line END",
    "IF LPAR condition RPAR lines END",
    "IF LPAR condition RPAR lines END",
    "IF LPAR condition RPAR END",
    "IF cond_f_call line END",
    "IF cond_f_call lines END",
    "IF cond_f_call lines END",
    "IF cond_f_call END",
    types={
        "IF LPAR condition RPAR line END": 1,
        "IF LPAR condition RPAR lines END": 1,
        "IF LPAR condition RPAR END": 2,
        "IF cond_f_call line END": 3,
        "IF cond_f_call lines END": 3,
        "IF cond_f_call END": 4,
    },
)
def if_statement(ts: DefaultProduction, type: int):
    if type == 1:
        return IfStatement(condition=ts[2], if_true=ts[4])

    elif type == 2:
        return IfStatement(condition=ts[2], if_true=CodeBlock([]))

    elif type == 3:
        return IfStatement(condition=ts[1], if_true=ts[2])

    elif type == 4:
        return IfStatement(condition=ts[1], if_true=CodeBlock([]))


@par.rule(
    "WHL condition line END",
    "WHL condition lines END",
    "WHL cond_f_call line END",
    "WHL cond_f_call lines END",
    # no body
    "WHL condition END",
    "WHL cond_f_call END",
    types={
        "WHL condition END": False,
        "WHL cond_f_call END": False,
    },
)
def while_stmt(ts: DefaultProduction, no_body: bool = True):
    if no_body:
        return WhileStatement(ts[1], CodeBlock([]))
    return WhileStatement(ts[1], ts[2])


@par.rule("FN f_call")
def function_marker(ts: DefaultProduction):
    # If the args is part of a function definition it should behave differentelly from when it is not
    ts[1].function_def = True
    return ts[1]


@par.rule("LPAR f_call")
def par_f_mark(ts):
    return ts[1]


@par.rule("par_f_mark RPAR")
def cond_f_call(ts):
    return ts[0]


@par.rule(
    "function_marker END",
    "function_marker line END",
    "function_marker lines END",
    types={
        "function_marker END": False,
    },
)
def function_definition(ts: DefaultProduction, hasend: bool):
    if hasend is False:
        return FunctionDefinition(name=ts[0].name, args=ts[0].args, inner=CodeBlock([]))

    return FunctionDefinition(name=ts[0].name, args=ts[0].args, inner=ts[1])


@par.rule("USE namespace_accessor")
def using(ts: DefaultProduction):
    return ts[1]


@par.rule(
    "f_call",
    "assighnment",
    "if_statement",
    "freeze",
    "function_definition",
    "using",
    "ret",
    "while_stmt",
)
def line(ts):
    return CodeBlock(ts[0])


@par.rule("line line", "line lines", "lines line")
def lines(ts: DefaultProduction):
    return ts[0].add_child(ts[1])


def get_parser():
    return par
