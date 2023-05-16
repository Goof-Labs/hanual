from __future__ import annotations

from hanual.lang.nodes import (
    AlgebraicExpression,
    FunctionDefinition,
    AnonymousFunction,
    NamespaceAccessor,
    ReturnStatement,
    UsingStatement,
    AssignmentNode,
    WhileStatement,
    BreakStatement,
    AlgebraicFunc,
    FunctionCall,
    IfStatement,
    FreezeNode,
    BinOpNode,
    Condition,
    CodeBlock,
    Arguments,
    RangeNode,
    AnonArgs,
)

from hanual.lang.productions import DefaultProduction
from hanual.lang.builtin_lexer import Token
from hanual.lang.pparser import PParser

par = PParser()

###########################
# BINARY OPERATIONS
###########################


@par.rule("NUM OP NUM")
def expr(ts: DefaultProduction[Token, Token, Token]) -> BinOpNode:
    return BinOpNode(op=ts[1], left=ts[0], right=ts[2])


@par.rule("expr OP NUM")
def expr(ts: DefaultProduction[BinOpNode, Token, Token]) -> BinOpNode:
    return BinOpNode(op=ts[1], left=ts[0], right=ts[2])


@par.rule("ID OP NUM")
def expr(ts: DefaultProduction[Token, Token, Token]) -> BinOpNode:
    return BinOpNode(ts[1], ts[0], ts[2])


###########################
# NAME SPACES
###########################


@par.rule("NSA ID")
def namespace_accessor(ts: DefaultProduction[Token, Token]) -> NamespaceAccessor:
    return NamespaceAccessor(ts[1])


@par.rule("ID namespace_accessor")
def namespace_accessor(ts: DefaultProduction[Token, NamespaceAccessor]):
    return ts[1].add_child(ts[0])


###########################
# ARGUMENTS
###########################


@par.rule("COM NUM", "COM expr", "COM f_call", "COM ID", "COM STR")
def arg(ts: DefaultProduction[Token, any]):
    return Arguments(ts[1])


@par.rule(
    "ID arg",
    "expr arg",
    "f_call arg",
    "STR arg",
    "NUM arg",
    "arg arg",
)
def arg(ts: DefaultProduction[any, Arguments]):
    return ts[1].add_child(ts[0])


###########################
# FUNCTION CALLS
###########################


@par.rule(
    "ID LPAR expr RPAR",
    "ID LPAR ID RPAR",
    "ID LPAR STR RPAR",
    "ID LPAR NUM RPAR",
    "ID LPAR arg RPAR",
    "ID LPAR RPAR",
    types={"ID LPAR RPAR": True},
)
def f_call(ts: DefaultProduction[Token, Token, any, Token], no_args: bool):
    if no_args:
        return FunctionCall(name=ts[0], arguments=Arguments([]))

    if isinstance(ts[2], Token):
        return FunctionCall(name=ts[0], arguments=Arguments(ts[2]))

    return FunctionCall(name=ts[0], arguments=Arguments(ts[2]))


###########################
# ALGEBRAIC OPERATIONS
###########################


@par.rule(
    # ALG
    "ADT OP ADT",
    "ADT OP NUM",
    "ADT OP expr",
    "ADT OP algebraic_op",
    # NUM
    "NUM OP ADT",
    "NUM OP algebraic_op",
    # algebraic_op
    "algebraic_op OP ADT",
    "algebraic_op OP NUM",
    "algebraic_op OP algebraic_op",
    "algebraic_op OP expr",
    # expr
    "expr OP ADT",
    "expr OP NUM",
    "expr OP algebraic_op",
)
def algebraic_op(ts: DefaultProduction):
    return AlgebraicExpression(operator=ts[1], left=ts[0], right=ts[2])


@par.rule("LET ID EQ algebraic_op")
def algebraic_fn(ts):
    return AlgebraicFunc(ts[1], ts[3])


###########################
# ASSIGHNMENT
###########################


@par.rule("LET ID EQ NUM", "LET ID EQ f_call", "LET ID EQ STR", unless=["DOT"])
def assignment(ts: DefaultProduction):
    return AssignmentNode(target=ts[1], value=ts[3])


@par.rule("LET ID EQ h_range")
def assignment(ts: DefaultProduction):
    return AssignmentNode(target=ts[1], value=ts[3])


###########################
# FREEZING
###########################


@par.rule("FREEZE ID")
def freeze(ts: DefaultProduction):
    return FreezeNode(ts[1])


###########################
# RETURNING
###########################


@par.rule("RET", unless=["ID"])
def ret(ts: DefaultProduction):
    return ReturnStatement(None)


@par.rule("RET ID", "RET NUM", unless=["LPAR"])
def ret(ts: DefaultProduction):
    return ReturnStatement(ts[1])


@par.rule("RET f_call")
def ret(ts: DefaultProduction):
    return ReturnStatement(ts[1])


###########################
# BREAKING
###########################


@par.rule("BREAK", unless=["CTX"])
def break_stmt(ts: DefaultProduction):
    return BreakStatement(ts[0])


@par.rule("BREAK CTX")
def break_stmt(ts: DefaultProduction):
    return BreakStatement(ts[0], ts[1])


###########################
# EQUALITY
###########################


@par.rule(
    # ID
    "ID EL f_call",
    "ID EL expr",
    "ID EL NUM",
    "ID EL STR",
    "ID EL ID",
    # NUM
    "NUM EL f_call",
    "NUM EL expr",
    "NUM EL NUM",
    "NUM EL STR",
    "NUM EL ID",
    # f_call
    "f_call EL f_call",
    "f_call EL expr",
    "f_call EL NUM",
    "f_call EL STR",
    "f_call EL ID",
)
def condition(ts: DefaultProduction):
    return Condition(op=ts[1], left=ts[0], right=ts[2])


###########################
# IF SATTEMENTS
###########################


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
def if_statement(ts: DefaultProduction, type_: int):
    if type_ == 1:
        return IfStatement(condition=ts[2], if_true=ts[4])

    elif type_ == 2:
        return IfStatement(condition=ts[2], if_true=CodeBlock([]))

    elif type_ == 3:
        return IfStatement(condition=ts[1], if_true=ts[2])

    elif type_ == 4:
        return IfStatement(condition=ts[1], if_true=CodeBlock([]))


###########################
# WHILE LOOPS
###########################


@par.rule(
    "WHL LPAR condition RPAR line END",
    "WHL LPAR condition RPAR lines END",
    "WHL cond_f_call line END",
    "WHL cond_f_call lines END",
    # nobody
    "WHL LPAR condition RPAR END",
    "WHL cond_f_call END",
    types={
        "WHL LPAR condition RPAR END": False,
        "WHL cond_f_call END": False,
    },
)
def while_stmt(ts: DefaultProduction, no_body: bool = True):
    if no_body:
        return WhileStatement(ts[2], CodeBlock([]))

    con = None
    blk = None

    for t in ts:
        if isinstance(t, Condition):
            con = t

        if isinstance(t, CodeBlock):
            blk = t

    return WhileStatement(condition=con, body=blk)


###########################
# MARKERS
###########################


@par.rule("FN f_call")
def function_marker(ts: DefaultProduction):
    # If the args is part of a function definition it should behave differently from when it is not
    ts[1].function_def = True
    return ts[1]


@par.rule("LPAR f_call")
def par_f_mark(ts):
    return ts[1]


@par.rule("par_f_mark RPAR")
def cond_f_call(ts):
    return ts[0]


###########################
# FUNCTION DEF
###########################


# NO CONTEXT
@par.rule(
    "function_marker END",
    "function_marker line END",
    "function_marker lines END",
    types={
        "function_marker END": False,
    },
    unless=["AS"],
)
def function_definition(ts: DefaultProduction, has_end: bool):
    if has_end is False:
        return FunctionDefinition(name=ts[0].name, args=ts[0].args, inner=CodeBlock([]))

    if not isinstance(ts[1], CodeBlock):
        return FunctionDefinition(
            name=ts[0].name, args=ts[0].args, inner=CodeBlock(ts[1])
        )

    return FunctionDefinition(name=ts[0].name, args=ts[0].args, inner=ts[1])


# WITH CONTEXT
@par.rule(
    "function_marker AS CTX END CTX",
    "function_marker AS CTX line END CTX",
    "function_marker AS CTX lines END CTX",
    types={
        "function_marker AS CTX END CTX": False,
    },
)
def function_definition(ts: DefaultProduction, has_end: bool):
    if has_end is False:
        return FunctionDefinition(name=ts[0].name, args=ts[0].args, inner=CodeBlock([]))

    if not isinstance(ts[1], CodeBlock):
        return FunctionDefinition(
            name=ts[0].name, args=ts[0].args, inner=CodeBlock(ts[1])
        )

    return FunctionDefinition(name=ts[0].name, args=ts[0].args, inner=ts[1])


###########################
# USE STATEMENT
###########################


@par.rule("USE namespace_accessor")
def using(ts: DefaultProduction):
    return UsingStatement(ts[1])


###########################
# ANONEMOUS FUNCTIONS ARGS
###########################


@par.rule(
    "LSB args RSB",
    "LSB ID RSB",
    types={"LSB ID RSB": True},
)
def anon_func_args(
    ts: DefaultProduction[Token, Arguments, Token], _1arg: bool
) -> AnonArgs:
    if _1arg:
        return AnonArgs(Arguments(ts[1]))

    return AnonArgs(ts[1])


###########################
# ANONEMOUS FUNCTIONS
###########################


@par.rule(
    "anon_func_args do line end",
    "anon_func_args do lines end",
)
def anon_function(
    ts: DefaultProduction[AnonArgs, Token, CodeBlock, Token]
) -> AnonymousFunction:
    return AnonymousFunction(args=ts[0], inner=ts[2])


# Anonemous functions can return stuff. The last statement is expected to be
# the return value so that is what we return. Of corse `lines` or `line` does
# not capute this case and probably shouldn't, because this wold break stuff
@par.rule(
    # last statement is a binop
    "anon_func_args do line expr end",
    "anon_func_args do lines expr end",
    # last statement is a ID
    "anon_func_args do line ID end",
    "anon_func_args do lines ID end",
    # last statement is a range
    "anon_func_args do line h_range end",
    "anon_func_args do lines h_range end",
)
def anon_function(
    ts: DefaultProduction[AnonArgs, Token, CodeBlock, Token]
) -> AnonymousFunction:
    return AnonymousFunction(args=ts[0], inner=ts[2], retrn=ts[3])


###########################
# RANGES
###########################


# ranges `x..`
@par.rule(
    "NUM DOT DOT",
    "ID DOT DOT",
)
def h_range(ts: DefaultProduction):
    return RangeNode(from_=ts[0], to_=None)


###########################
# CODE BLOCKS
###########################


@par.rule(
    "function_definition",
    "if_statement",
    "assignment",
    "while_stmt",
    "break_stmt",
    "freeze",
    "f_call",
    "using",
    "ret",
)
def line(ts):
    return CodeBlock(ts[0])


@par.rule("line line", "line lines", "lines line")
def lines(ts: DefaultProduction):
    return ts[0].add_child(ts[1])


###########################
# END
###########################


def get_parser():
    return par
