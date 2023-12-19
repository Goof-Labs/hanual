from __future__ import annotations

from typing import Any, Literal, Union

from hanual.lang.builtin_lexer import Token
from hanual.lang.nodes import (
    AlgebraicExpression,
    AlgebraicFunc,
    AnonymousFunction,
    Arguments,
    AssignmentNode,
    BinOpNode,
    BreakStatement,
    CodeBlock,
    Condition,
    DotChain,
    ElifStatement,
    ElseStatement,
    ForLoop,
    FunctionCall,
    FunctionDefinition,
    HanualList,
    IfChain,
    IfStatement,
    ImplicitBinOp,
    ImplicitCondition,
    LoopLoop,
    NamespaceAccessor,
    NewStruct,
    Parameters,
    RangeNode,
    ReturnStatement,
    SGetattr,
    ShoutNode,
    StrongField,
    StrongFieldList,
    StructDefinition,
    UsingStatement,
    UsingStatementWithAltName,
    VarChange,
    WhileStatement,
)
from hanual.lang.pparser import PParser
from hanual.lang.productions import DefaultProduction
from hanual.lang.util.line_range import LineRange

par = PParser()


###########################
# STRUCTS
###########################


@par.rule("ID COL ID")
def strong_field(
        ts: DefaultProduction[Token, Token, Token], lines: str = "", line_range: int = 0
) -> StrongField:
    return StrongField(ts[0], ts[2], lines=lines, line_range=line_range)


@par.rule(
    "SCT ID",
    "SCT ID COL ID",
    "SCT ID COL args",
    unless_ends=["COL"],
)
def struct_header(
        ts: DefaultProduction[Token, Token], lines: str = "", line_range: int = 0
) -> DefaultProduction[Token, Token]:
    # This header exists to provide the `struct NAME` part of the
    # struct, we want to not do this if the following character is
    # a `:` colon, this means that we want to inherit from another
    # struct. This rule just makes the actuall
    return ts


@par.rule("strong_field strong_field")
def strong_fields(
        ts: DefaultProduction[StrongField, StrongField],
        lines: str = "",
        line_range: int = 0,
) -> StrongFieldList:
    return (
        StrongFieldList(lines=lines, line_range=line_range)
        .add_field(ts[0])
        .add_field(ts[1])
    )


@par.rule("strong_fields strong_field")
def strong_fields(
        ts: DefaultProduction[StrongFieldList, StrongField],
        lines: str = "",
        line_range: int = 0,
) -> StrongFieldList:
    return ts[0].add_field(ts[1])


@par.rule("struct_header LCB strong_field RCB", "struct_header LCB strong_fields RCB")
def struct_def(
        ts: DefaultProduction[
            DefaultProduction[Token, Token],  # struct header
            Union[StrongField, StrongFieldList],  # struct fields
            Token,  # end token
        ],
        lines: str = "",
        line_range: int = 0,
) -> StructDefinition:
    return StructDefinition(ts[0][1], ts[2], lines=lines, line_range=line_range)


###########################
# [LISTS, FOR, ELEMENTS]
###########################


@par.rule("LSB args RSB")
def h_list(
        ts: DefaultProduction[Token, Arguments, Token], lines: str = "", line_range: int = 0
) -> HanualList:
    return HanualList(ts[1], lines=lines, line_range=line_range)


@par.rule("LSB ID RSB", "LSB NUM RSB")
def h_list(
        ts: DefaultProduction[Token, Token, Token], lines: str = "", line_range: int = 0
) -> HanualList:
    return HanualList(
        Arguments(ts[1], lines=lines, line_range=line_range),
        lines=lines,
        line_range=line_range,
    )


@par.rule("ID h_list")
def s_getattr(
        ts: DefaultProduction[Token, HanualList], lines: str = "", line_range: int = 0
):
    return SGetattr(ts[0], ts[1], lines=lines, line_range=line_range)


###########################
# FOR LOOPS
###########################


@par.rule(
    "FOR assignment COM impl_condition COM impl_binop LCB RCB",
    "FOR assignment COM impl_condition COM impl_binop LCB line RCB",
    "FOR assignment COM impl_condition COM impl_binop LCB lines RCB",
    types={
        "FOR assignment COM impl_condition COM impl_binop LCB RCB": True,
        "_": False
    },
)
def for_loop(
        ts,
        no_body: Union[Literal[True], Literal[None]],
) -> ForLoop:
    if no_body is True:
        return ForLoop(
            ts[3],
            ts[1],
            ts[5],
            CodeBlock([]),
        )

    return ForLoop(ts[3], ts[1], ts[5], ts[7])


###########################
# LOOP LOOPS
###########################


@par.rule(
    "LOOP LCB line RCB",
    "LOOP LCB lines RCB",
    "LOOP LCB RCB",
    types={"LOOP LCB RCB": True},
)
def loop_loop(
        ts: DefaultProduction, no_inner: bool = False, lines: str = "", line_range: int = 0
):
    if no_inner:
        return LoopLoop(
            CodeBlock([], lines=lines, line_range=line_range),
            lines=lines,
            line_range=line_range,
        )

    return LoopLoop(ts[2], lines=lines, line_range=line_range)


###########################
# DOT NOTATION.YAY()
###########################


@par.rule("DOT ID")
def dot_id(
        ts: DefaultProduction[Token, Token], lines: str = "", line_range: int = 0
) -> DotChain:
    return DotChain(lines=lines, line_range=line_range).add_name(ts[1])


@par.rule("iwith_dot dot_id")
def iwith_dot(
        ts: DefaultProduction[DotChain, DotChain], lines: str = "", line_range: int = 0
) -> DotChain:
    return ts[0].add_name(ts[1])


@par.rule("ID dot_id", unless_starts=["DOT"])
def iwith_dot(
        ts: DefaultProduction[Token, DotChain], lines: str = "", line_range: int = 0
) -> DotChain:
    return ts[1].add_name(ts[0])


###########################
# BINARY OPERATIONS
###########################


@par.rule(
    "NUM OP NUM",
    "expr OP NUM",
    "expr OP expr",
    "expr OP ID",
    "expr OP STR",
    "ID OP NUM",
    "ID OP expr",
    "ID OP ID",
    "ID OP STR",
    "STR OP STR",
    "STR OP ID",
    "STR OP expr",
)
def expr(
        ts: DefaultProduction[Token, Token, Token], lines: str = "", line_range: int = 0
) -> BinOpNode:
    return BinOpNode(
        op=ts[1], left=ts[0], right=ts[2], lines=lines, line_range=line_range
    )


###########################
# IMPLICIT CONDITIONS
###########################


@par.rule(
    "EL NUM",
    "EL STR",
    "EL ID",
    "EL f_call",
    unless_starts=["NUM", "ID", "f_call", "STR"],
)
def impl_condition(ts: DefaultProduction[Token, Token | FunctionCall]):
    return ImplicitCondition(ts[0], ts[1])


###########################
# IMPLICIT BINOP
###########################


@par.rule("OP OP NUM", "OP OP ID", "OP OP f_call", unless_ends=["LPAR"])
def impl_binop(ts: DefaultProduction[Token, Token, Token | FunctionCall]):
    return ImplicitBinOp(ts[0], ts[2])


###########################
# NAME SPACES
###########################


@par.rule("NSA ID")
def namespace_accessor(
        ts: DefaultProduction[Token, Token], lines: str = "", line_range: int = 0
) -> NamespaceAccessor:
    return NamespaceAccessor(ts[1], lines=lines, line_range=line_range)


@par.rule("namespace_accessor namespace_accessor")
def namespace_accessor(
        ts: DefaultProduction[NamespaceAccessor, NamespaceAccessor],
        lines: str = "",
        line_range: int = 0,
):
    return ts[0].add_child(ts[1])


@par.rule("ID namespace_accessor")
def namespace_accessor(
        ts: DefaultProduction[Token, NamespaceAccessor],
        lines: str = "",
        line_range: int = 0,
):
    return ts[1].add_child(ts[0])


###########################
# ARGUMENTS
###########################


@par.rule(
    "COM NUM",
    "COM expr",
    "COM f_call",
    "COM ID",
    "COM STR",
    "COM args",
    "COM s_getattr",
    "COM args_",
)
def args_(ts: DefaultProduction[Token, Any]):
    return Arguments(ts[1])


@par.rule(
    "ID args_",
    "expr args_",
    "f_call args_",
    "STR args_",
    "NUM args_",
    "args args_",
    "s_getattr args_",
)
def args(ts: DefaultProduction[any, Arguments], lines: str = "", line_range: int = 0):
    return ts[1].add_child(ts[0])


@par.rule("args_ args_")
def args_(
        ts: DefaultProduction[Arguments, Arguments], lines: str = "", line_range: int = 0
) -> Arguments:
    return ts[0].add_child(ts[1])


@par.rule(
    "LPAR args RPAR",
    "LPAR ID RPAR",
    "LPAR expr RPAR",
    "LPAR f_call RPAR",
    "LPAR STR RPAR",
    "LPAR NUM RPAR",
    "LPAR s_getattr RPAR",
)
def par_args(ts, lines: str = "", line_range: int = 0):
    return Arguments(ts[1])


###########################
# FUNCTION CALLS
###########################


@par.rule(
    "ID LPAR expr RPAR",
    "ID LPAR ID RPAR",
    "ID LPAR STR RPAR",
    "ID LPAR NUM RPAR",
    "ID LPAR f_call RPAR",
    "ID LPAR s_getattr RPAR",
    "ID LPAR iwith_dot RPAR",
    "ID LPAR RPAR",
    "ID par_args",
    types={"ID LPAR RPAR": 1, "ID par_args": 2},
)
def f_call(
        ts: DefaultProduction[Token, Token, any, Token],
        mode: int,
):
    if mode == 1:
        return FunctionCall(
            name=ts[0],
            arguments=Arguments([]),
        )

    if mode == 2:
        return FunctionCall(
            name=ts[0],
            arguments=Arguments(ts[1]),
        )

    raise NotImplementedError


@par.rule(
    "namespace_accessor LPAR expr RPAR",
    "namespace_accessor LPAR ID RPAR",
    "namespace_accessor LPAR STR RPAR",
    "namespace_accessor LPAR NUM RPAR",
    "namespace_accessor LPAR f_call RPAR",
    "namespace_accessor LPAR RPAR",
    "namespace_accessor par_args",
    types={"namespace_accessor LPAR RPAR": 1, "namespace_accessor par_args": 2},
)
def f_call(
        ts: DefaultProduction[Token, Token, any, Token],
        mode: int,
        lines: str = "",
        line_range: int = 0,
):
    if mode == 1:
        return FunctionCall(
            name=ts[0],
            arguments=Arguments([], lines=lines, line_range=line_range),
            lines=lines,
            line_range=line_range,
        )

    if mode == 2:
        return FunctionCall(
            name=ts[0],
            arguments=Arguments(ts[1], lines=lines, line_range=line_range),
            lines=lines,
            line_range=line_range,
        )

    if isinstance(ts[2], Token):
        return FunctionCall(
            name=ts[0],
            arguments=Arguments(ts[2], lines=lines, line_range=line_range),
            lines=lines,
            line_range=line_range,
        )

    return FunctionCall(
        name=ts[0],
        arguments=Arguments(ts[2], lines=lines, line_range=line_range),
        lines=lines,
        line_range=line_range,
    )


@par.rule(
    "iwith_dot LPAR expr RPAR",
    "iwith_dot LPAR ID RPAR",
    "iwith_dot LPAR STR RPAR",
    "iwith_dot LPAR NUM RPAR",
    "iwith_dot LPAR f_call RPAR",
    "iwith_dot LPAR RPAR",
    "iwith_dot par_args",
    types={"iwith_dot LPAR RPAR": 1, "iwith_dot par_args": 2},
)
def f_call(
        ts: DefaultProduction[Token, Token, any, Token],
        mode: int,
        lines: str = "",
        line_range: int = 0,
):
    if mode == 1:
        # ( )
        return FunctionCall(
            name=ts[0],
            arguments=Arguments([], lines=lines, line_range=line_range),
            lines=lines,
            line_range=line_range,
        )

    if mode == 2:
        # automatic params
        return FunctionCall(
            name=ts[0],
            arguments=Arguments(ts[1], lines=lines, line_range=line_range),
            lines=lines,
            line_range=line_range,
        )

    if isinstance(ts[2], Token):
        return FunctionCall(
            name=ts[0],
            arguments=Arguments(ts[2], lines=lines, line_range=line_range),
            lines=lines,
            line_range=line_range,
        )

    return FunctionCall(
        name=ts[0],
        arguments=Arguments(ts[2], lines=lines, line_range=line_range),
        lines=lines,
        line_range=line_range,
    )


###########################
# NEW STRUCT
###########################
@par.rule("NEW f_call")
def new_struct(
        ts: DefaultProduction[Token, FunctionCall], lines: str = "", line_range: int = 0
) -> NewStruct:
    return NewStruct(ts[1], lines=lines, line_range=line_range)


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
    "expr OP algebraic_op",
)
def algebraic_op(ts: DefaultProduction, lines: str = "", line_range: int = 0):
    return AlgebraicExpression(
        operator=ts[1], left=ts[0], right=ts[2], lines=lines, line_range=line_range
    )


@par.rule("LET ID EQ algebraic_op")
def algebraic_fn(ts, lines: str = "", line_range: int = 0):
    return AlgebraicFunc(ts[1], ts[3], lines=lines, line_range=line_range)


###########################
# ASSIGHNMENT
###########################


@par.rule(
    "LET ID EQ NUM",
    "LET ID EQ f_call",
    "LET ID EQ STR",
    "LET ID EQ new_struct",
    "LET ID EQ h_list",
    "LET ID EQ anon_function",
    unless_ends=["DOT"],
)
def assignment(ts: DefaultProduction):
    return AssignmentNode(target=ts[1], value=ts[3])


@par.rule("LET ID EQ h_range")
def assignment(ts: DefaultProduction, lines: str = "", line_range: int = 0):
    return AssignmentNode(target=ts[1], value=ts[3], lines=lines, line_range=line_range)


###########################
# CHANGING AND MODDING VARS
###########################


@par.rule(
    "ID EQ NUM",
    "ID EQ f_call",
    "ID EQ STR",
    "ID EQ expr",
    "ID EQ ID",
    "ID EQ iwith_dot",
    "iwith_dot EQ NUM",
    "iwith_dot EQ f_call",
    "iwith_dot EQ STR",
    "iwith_dot EQ expr",
    "iwith_dot EQ ID",
    "iwith_dot EQ iwith_dot",
    unless_ends=["DOT", "LPAR", "OP"],
)
def var_change(ts: DefaultProduction, lines: str = "", line_range: int = 0):
    return VarChange(ts[0], ts[2], lines=lines, line_range=line_range)


###########################
# RETURNING
###########################


@par.rule("RET", unless_ends=["ID", "NUM", "STR"])
def ret(ts: DefaultProduction, lines: str = "", line_range: LineRange = 0):
    return ReturnStatement(None, lines=lines, line_range=line_range)


@par.rule("RET ID", "RET NUM", "RET f_call", "RET expr", unless_ends=["LPAR", "OP"])
def ret(ts: DefaultProduction, lines: str = "", line_range: LineRange = 0):
    return ReturnStatement(ts[1], lines=lines, line_range=line_range)


###########################
# BREAKING
###########################


@par.rule("BREAK", unless_ends=["CTX"])
def break_stmt(
        ts: DefaultProduction[Token], lines: str = "", line_range: LineRange = 0
):
    return BreakStatement(ts[0], lines=lines, line_range=line_range)


@par.rule("BREAK CTX")
def break_stmt(ts: DefaultProduction, lines: str = "", line_range: LineRange = 0):
    return BreakStatement(ts[0], ts[1], lines=lines, line_range=line_range)


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
    unless_ends=["LPAR"],
)
def condition(ts: DefaultProduction):
    return Condition(op=ts[1], left=ts[0], right=ts[2])


###########################
# IF SATTEMENTS
###########################


@par.rule(
    "IF condition LCB lines RCB",
    "IF condition LCB line RCB",
    "IF condition LCB RCB",
    types={
        "IF condition LCB line RCB": 1,
        "IF condition LCB lines RCB": 1,
        "IF condition LCB RCB": 2,
    },
)
def if_statement(ts: DefaultProduction, type_: int):
    if type_ == 1:
        return IfStatement(ts[1], ts[3])

    elif type_ == 2:
        return IfStatement(
            ts[1],
            CodeBlock([]),
        )

    else:
        raise Exception



@par.rule(
    "IF condition LCB line RCB EIF",
    "IF condition LCB lines RCB EIF",
    "IF condition LCB lines RCB EIF",
    "IF condition LCB EIF RCB",
    "if_statement EIF",
    types={
        "IF condition LCB line RCB EIF": 1,
        "IF condition LCB lines RCB EIF": 1,
        "IF condition LCB EIF RCB": 2,
        "if_statement EIF": 3,
    },
)
def if_chain_start(
        ts: DefaultProduction, type_: int, lines: str = "", line_range: LineRange = 0
):
    chain = IfChain(lines=lines, line_range=line_range)

    if type_ == 1:
        return chain.add_node(
            IfStatement(ts[1], ts[3], lines=lines, line_range=line_range)
        )

    elif type_ == 2:
        return chain.add_node(
            IfStatement(
                ts[1],
                CodeBlock([], lines=lines, line_range=line_range),
                lines=lines,
                line_range=line_range,
            )
        )

    elif type_ == 3:
        return chain.add_node(ts[0])

    raise Exception


@par.rule(
    "if_chain_start ELS LCB line RCB",
    "if_chain_start ELS LCB lines RCB",
    "if_chain ELS LCB line RCB",
    "if_chain ELS LCB lines RCB",
)
def if_chain(ts: DefaultProduction, lines: str = "", line_range: int = 0) -> IfChain:
    return ts[0].add_else(ElseStatement(ts[3], lines=lines, line_range=line_range))


@par.rule(
    "if_chain_start condition LCB line RCB",
    "if_chain_start condition LCB lines RCB",
    "if_chain_start condition LCB RCB",
    types={
        "if_chain_start condition LCB lines RCB": 1,
        "if_chain_start condition LCB RCB": 2,
        "if_chain_start condition LCB line RCB": 3,
    },
)
def if_chain(
        ts: DefaultProduction, type_: int, lines: str = "", line_range: int = 0
) -> IfChain:
    if type_ == 1:
        return ts[0].add_node(
            ElifStatement(ts[1], ts[3], lines=lines, line_range=line_range)
        )

    elif type_ == 2:
        return ts[0].add_node(
            ElifStatement(
                ts[1],
                CodeBlock([], lines=lines, line_range=line_range),
                lines=lines,
                line_range=line_range,
            )
        )

    elif type_ == 3:
        return ts[0].add_node(
            ElifStatement(ts[1], ts[3], lines=lines, line_range=line_range),
            lines=lines,
            line_range=line_range,
        )

    raise Exception


###########################
# WHILE LOOPS
###########################


@par.rule(
    "WHL condition LCB line RCB",
    "WHL condition LCB lines RCB",
    # nobody
    "WHL condition LCB RCB",
    types={
        "WHL condition LCB RCB": True,
    },
)
def while_stmt(
        ts: DefaultProduction, no_body: bool = True, lines: str = "", line_range: int = 0
):
    if no_body:
        return WhileStatement(
            ts[1],
            CodeBlock([], lines=lines, line_range=line_range),
            lines=lines,
            line_range=line_range,
        )

    return WhileStatement(
        condition=ts[1], body=ts[3], lines=lines, line_range=line_range
    )


###########################
# SHOUT
###########################


@par.rule("SHOUT")
def shout(ts: DefaultProduction[Token], lines: str, line_range: LineRange) -> ShoutNode:
    return ShoutNode(ts[0], lines=lines, line_range=line_range)


###########################
# MARKERS
###########################


@par.rule("FN f_call")
def function_marker(
        ts: DefaultProduction[FunctionCall], lines: str = "", line_range: int = 0
):
    # If the params is part of a function definition it should behave differently from when it is not
    return ts[1]


###########################
# FUNCTION DEF
###########################


# NO CONTEXT
@par.rule(
    "function_marker LCB RCB",
    "function_marker LCB line RCB",
    "function_marker LCB lines RCB",
    types={
        "function_marker LCB RCB": False,
        "*": True
    },
    unless_ends=["AS"],
)
def function_definition(
        ts: DefaultProduction[FunctionCall, Token, CodeBlock, Token],
        has_end: bool,
):
    if has_end is False:
        return FunctionDefinition(
            name=ts[0].name,
            params=Parameters(ts[0].args.children),
            inner=CodeBlock([]),
        )

    if not isinstance(ts[2], CodeBlock):
        return FunctionDefinition(
            name=ts[0].name,
            params=Parameters(ts[0].args.children),
            inner=CodeBlock(ts[2]),
        )

    return FunctionDefinition(
        name=ts[0].name,
        params=Parameters(ts[0].args.children),
        inner=ts[2],
    )


###########################
# USE STATEMENT
###########################


@par.rule(
    "USE namespace_accessor",
    unless_ends=["AS", "NSA"],
)
def using(ts: DefaultProduction, lines: str = "", line_range: int = 0):
    return UsingStatement(ts[1], lines=lines, line_range=line_range)


@par.rule("USE namespace_accessor AS ID")
def using(
        ts: DefaultProduction[Token, NamespaceAccessor, Token, Token],
        lines: str = "",
        line_range: int = 0,
):
    return UsingStatementWithAltName(ts[1], ts[3], lines=lines, line_range=line_range)


@par.rule("USE ID", unless_ends=["NSA"])
def using(
        ts: DefaultProduction[Token, Token], lines: str = "", line_range: int = 0
) -> UsingStatement:
    return UsingStatement(
        NamespaceAccessor(ts[1], lines=lines, line_range=line_range),
        lines=lines,
        line_range=line_range,
    )


###########################
# ANONEMOUS FUNCTIONS
###########################


@par.rule(
    # nothing
    "par_args LCB line RCB",
    "par_args LCB lines RCB",
    # expr
    "par_args LCB expr RCB",
    "par_args LCB line expr RCB",
    "par_args LCB lines expr RCB",
)
def anon_function(
        ts: DefaultProduction, lines: str = "", line_range: int = 0
) -> AnonymousFunction:
    return AnonymousFunction(
        args=ts[0], inner=ts[2], lines=lines, line_range=line_range
    )


###########################
# RANGES
###########################


# ranges `x..`
@par.rule(
    "NUM DOT DOT",
    "ID DOT DOT",
)
def h_range(ts: DefaultProduction, lines: str = "", line_range: int = 0):
    return RangeNode(from_=ts[0], to_=None, lines=lines, line_range=line_range)


###########################
# CODE BLOCKS
###########################


@par.rule(
    "function_definition",
    "if_statement",
    "assignment",
    "while_stmt",
    "break_stmt",
    "loop_loop",
    "var_change",
    "struct_def",
    "for_loop",
    "if_chain",
    "freeze",
    "f_call",
    "shout",
    "using",
    "ret",
    unless_ends=["RPAR", "COM", "BAR", "EIF", "ELS", "DOT"],
)
def line(ts, lines: str = "", line_range: int = 0):
    return CodeBlock(ts[0], lines=lines, line_range=line_range)


@par.rule("line line", "line lines", "lines line")
def lines(ts: DefaultProduction, lines: str = "", line_range: int = 0):
    return ts[0].add_child(ts[1])


###########################
# END
###########################


def get_parser():
    return par
