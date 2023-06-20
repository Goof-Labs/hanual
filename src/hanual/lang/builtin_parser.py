from __future__ import annotations

from hanual.lang.nodes import (
    UsingStatementWithAltName,
    AlgebraicExpression,
    FunctionDefinition,
    AnonymousFunction,
    NamespaceAccessor,
    ImplicitCondition,
    StructDefinition,
    StrongFieldList,
    ReturnStatement,
    UsingStatement,
    AssignmentNode,
    WhileStatement,
    BreakStatement,
    ImplicitBinop,
    AlgebraicFunc,
    ElifStatement,
    FunctionCall,
    IfStatement,
    StrongField,
    FreezeNode,
    HanualList,
    BinOpNode,
    Condition,
    NewStruct,
    CodeBlock,
    Arguments,
    RangeNode,
    VarChange,
    ShoutNode,
    DotChain,
    AnonArgs,
    IfChain,
    ForLoop,
)
from hanual.lang.productions import DefaultProduction
from hanual.lang.builtin_lexer import Token
from hanual.lang.pparser import PParser
from typing import Union, Literal

par = PParser()

###########################
# STRUCTS
###########################


@par.rule("ID COL ID")
def strong_field(ts: DefaultProduction[Token, Token, Token]) -> StrongField:
    return StrongField(ts[0], ts[2])


@par.rule(
    "SCT ID",
    "SCT ID COL ID",
    "SCT ID COL args",
    unless_ends=["COL"],
)
def struct_header(
    ts: DefaultProduction[Token, Token]
) -> DefaultProduction[Token, Token]:
    # This header exists to provide the `struct NAME` part of the
    # struct, we want to not do this if the following character is
    # a `:` colon, this means that we want to inherit from another
    # struct. This rule just makes the actuall
    return ts


@par.rule("strong_field strong_field")
def strong_fields(ts: DefaultProduction[StrongField, StrongField]) -> StrongFieldList:
    return StrongFieldList().add_field(ts[0]).add_field(ts[1])


@par.rule("strong_fields strong_field")
def strong_fields(
    ts: DefaultProduction[StrongFieldList, StrongField]
) -> StrongFieldList:
    return ts[0].add_field(ts[1])


@par.rule("struct_header LCB strong_field RCB", "struct_header LCB strong_fields RCB")
def struct_def(
    ts: DefaultProduction[
        DefaultProduction[Token, Token],  # struct header
        Union[StrongField, StrongFieldList],  # struct fields
        Token,  # end token
    ]
) -> StructDefinition:
    return StructDefinition(ts[0][1].value, ts[2])


###########################
# [LISTS, FOR, ELEMENTS]
###########################


@par.rule("LSB args RSB")
def h_list(ts: DefaultProduction[Token, Arguments, Token]) -> HanualList:
    return HanualList(ts[1])


###########################
# FOR LOOPS
###########################


@par.rule(
    "FOR assignment COM impl_condition COM impl_binop LCB RCB",
    "FOR assignment COM impl_condition COM impl_binop LCB line RCB",
    "FOR assignment COM impl_condition COM impl_binop LCB lines RCB",
    types={"FOR assignment COM impl_condition COM impl_binop LCB RCB": True},
)
def for_loop(
    ts: Union[
        # for if the code block is non existant
        DefaultProduction[
            Token,
            AssignmentNode,
            Token,
            ImplicitCondition,
            Token,
            ImplicitBinop,
            Token,
        ],
        # if we have lines or a line of code
        DefaultProduction[
            Token,
            AssignmentNode,
            Token,
            ImplicitCondition,
            Token,
            ImplicitBinop,
            CodeBlock,
            Token,
        ],
    ],
    no_body: Union[Literal[True], Literal[None]],
) -> ForLoop:
    if no_body:
        return ForLoop(ts[3], ts[1], ts[5], CodeBlock([]))

    return ForLoop(ts[3], ts[1], ts[5], ts[6])


###########################
# DOT NOTATION.YAY()
###########################


@par.rule("DOT ID")
def dot_id(ts: DefaultProduction[Token, Token]) -> DotChain:
    dc = DotChain()
    return dc.add_name(ts[1])


@par.rule("iwith_dot dot_id")
def iwith_dot(ts: DefaultProduction[DotChain, DotChain]) -> DotChain:
    return ts[0].add_name(ts[1])


@par.rule("ID dot_id", unless_starts=["DOT"])
def iwith_dot(ts: DefaultProduction[Token, DotChain]) -> DotChain:
    return ts[1].add_name(ts[0])


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


@par.rule("ID OP ID")
def expr(ts: DefaultProduction[Token, Token, Token]) -> BinOpNode:
    return BinOpNode(ts[1], ts[0], ts[2])


###########################
# IMPLICIT CONDITIONDS
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
    return ImplicitBinop(ts[0], ts[2])


###########################
# NAME SPACES
###########################


@par.rule("NSA ID")
def namespace_accessor(ts: DefaultProduction[Token, Token]) -> NamespaceAccessor:
    return NamespaceAccessor(ts[1])


@par.rule("namespace_accessor namespace_accessor")
def namespace_accessor(ts: DefaultProduction[NamespaceAccessor, NamespaceAccessor]):
    return ts[0].add_child(ts[1])


@par.rule("ID namespace_accessor")
def namespace_accessor(ts: DefaultProduction[Token, NamespaceAccessor]):
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
    "COM args_",
)
def args_(ts: DefaultProduction[Token, any]):
    return Arguments(ts[1])


@par.rule(
    "ID args_",
    "expr args_",
    "f_call args_",
    "STR args_",
    "NUM args_",
    "args args_",
)
def args(ts: DefaultProduction[any, Arguments]):
    return ts[1].add_child(ts[0])


@par.rule("args_ args_")
def args_(ts: DefaultProduction[Arguments, Arguments]) -> Arguments:
    return ts[0].add_child(ts[1])


@par.rule("LPAR args RPAR")
def par_args(ts):
    return ts[1]


###########################
# FUNCTION CALLS
###########################


@par.rule(
    "ID LPAR expr RPAR",
    "ID LPAR ID RPAR",
    "ID LPAR STR RPAR",
    "ID LPAR NUM RPAR",
    "ID LPAR f_call RPAR",
    "ID LPAR RPAR",
    "ID par_args",
    types={"ID LPAR RPAR": 1, "ID par_args": 2},
)
def f_call(ts: DefaultProduction[Token, Token, any, Token], mode: int):
    if mode == 1:
        return FunctionCall(name=ts[0], arguments=Arguments([]))

    if mode == 2:
        return FunctionCall(name=ts[0], arguments=ts[1])

    if isinstance(ts[2], Token):
        return FunctionCall(name=ts[0], arguments=Arguments(ts[2]))

    return FunctionCall(name=ts[0], arguments=Arguments(ts[2]))


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
def f_call(ts: DefaultProduction[Token, Token, any, Token], mode: int):
    if mode == 1:
        return FunctionCall(name=ts[0], arguments=Arguments([]))

    if mode == 2:
        return FunctionCall(name=ts[0], arguments=ts[1])

    if isinstance(ts[2], Token):
        return FunctionCall(name=ts[0], arguments=Arguments(ts[2]))

    return FunctionCall(name=ts[0], arguments=Arguments(ts[2]))


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
def f_call(ts: DefaultProduction[Token, Token, any, Token], mode: int):
    if mode == 1:
        # ( )
        return FunctionCall(name=ts[0], arguments=Arguments([]))

    if mode == 2:
        # automatic args
        return FunctionCall(name=ts[0], arguments=ts[1])

    if isinstance(ts[2], Token):
        return FunctionCall(name=ts[0], arguments=Arguments(ts[2]))

    return FunctionCall(name=ts[0], arguments=Arguments(ts[2]))


###########################
# NEW STRUCT
###########################
@par.rule("NEW f_call")
def new_struct(ts: DefaultProduction[Token, FunctionCall]) -> NewStruct:
    return NewStruct(ts[1])


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


@par.rule(
    "LET ID EQ NUM",
    "LET ID EQ f_call",
    "LET ID EQ STR",
    "LET ID EQ new_struct",
    unless_ends=["DOT"],
)
def assignment(ts: DefaultProduction):
    return AssignmentNode(target=ts[1], value=ts[3])


@par.rule("LET ID EQ h_range")
def assignment(ts: DefaultProduction):
    return AssignmentNode(target=ts[1], value=ts[3])


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
def var_change(ts: DefaultProduction):
    return VarChange(ts[0], ts[2])


###########################
# FREEZING
###########################


@par.rule("FREEZE ID")
def freeze(ts: DefaultProduction):
    return FreezeNode(ts[1])


###########################
# RETURNING
###########################


@par.rule("RET", unless_ends=["ID"])
def ret(ts: DefaultProduction):
    return ReturnStatement(None)


@par.rule("RET ID", "RET NUM", "RET f_call", "RET expr", unless_ends=["LPAR", "OP"])
def ret(ts: DefaultProduction):
    return ReturnStatement(ts[1])


###########################
# BREAKING
###########################


@par.rule("BREAK", unless_ends=["CTX"])
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
    unless_ends=["LPAR"],
)
def condition(ts: DefaultProduction):
    return Condition(op=ts[1], left=ts[0], right=ts[2])


###########################
# IF SATTEMENTS
###########################


@par.rule(
    "IF condition LCB line RCB",
    "IF condition LCB lines RCB",
    "IF condition LCB lines RCB",
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
        return IfStatement(ts[1], CodeBlock([]))

    elif type_ == 4:
        return IfStatement(ts[1], CodeBlock([]))


@par.rule(
    "IF condition LCB line RCB EIF",
    "IF condition LCB lines RCB EIF",
    "IF condition LCB lines RCB EIF",
    "IF condition LCB EIF RCB",
    types={
        "IF condition LCB line RCB EIF": 1,
        "IF condition LCB lines RCB EIF": 1,
        "IF condition LCB EIF RCB": 2,
    },
)
def if_chain_start(ts: DefaultProduction, type_: int):
    chain = IfChain()

    if type_ == 1:
        return chain.add_node(IfStatement(ts[1], ts[3]))

    elif type_ == 2:
        return chain.add_node(IfStatement(ts[1], CodeBlock([])))


@par.rule(
    "if_chain_start condition line EIF",
    "if_chain_start condition lines EIF",
)
def condition_chain(ts: DefaultProduction[IfChain, Token, Condition, Token]) -> IfChain:
    return ts[0].add_node(ElifStatement(ts[1], ts[2]))


@par.rule(
    "if_chain_start condition line ELS line END",
    "if_chain_start condition lines ELS line END",
    "if_chain_start condition line ELS lines END",
    "if_chain_start condition lines ELS lines END",
)
def if_chain(
    ts: DefaultProduction[
        IfChain,  # original elif chain
        Token,  # lpar
        Condition,  # condition
        Token,  # RPAR
        CodeBlock,  # block
        Token,  # ELSE
        CodeBlock,  # line(s)
        Token,  # END
    ]
) -> IfChain:
    return ts[0].add_node(ElifStatement(ts[1], ts[2])).add_else(ts[4])


@par.rule(
    "if_chain_start condition line END",
    "if_chain_start condition lines END",
)
def if_chain(
    ts: DefaultProduction[
        IfChain,
        Token,
        Condition,
        Token,
        CodeBlock,
        Token,
    ]
) -> IfChain:
    return ts[0]


@par.rule("condition_chain END")
def if_chain(ts: DefaultProduction[IfChain]) -> IfChain:
    return ts


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
def while_stmt(ts: DefaultProduction, no_body: bool = True):
    if no_body:
        return WhileStatement(ts[1], CodeBlock([]))

    return WhileStatement(condition=ts[1], body=ts[3])


###########################
# SHOUT
###########################


@par.rule("SHOUT")
def shout(ts: DefaultProduction[Token]) -> ShoutNode:
    return ShoutNode(ts[0])


###########################
# MARKERS
###########################


@par.rule("FN f_call")
def function_marker(ts: DefaultProduction):
    # If the args is part of a function definition it should behave differently from when it is not
    ts[1].function_def = True
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
    },
    unless_ends=["AS"],
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
    "function_marker AS CTX LCB RCB CTX",
    "function_marker AS CTX LCB line RCB CTX",
    "function_marker AS CTX LCB lines RCB CTX",
    types={
        "function_marker AS CTX LCB RCB CTX": False,
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


@par.rule(
    "USE namespace_accessor",
    unless_ends=["AS", "NSA"],
)
def using(ts: DefaultProduction):
    return UsingStatement(ts[1])


@par.rule("USE namespace_accessor AS ID")
def using(ts: DefaultProduction[Token, NamespaceAccessor, Token, Token]):
    return UsingStatementWithAltName(ts[1], ts[3])


@par.rule("USE ID", unless_ends=["NSA"])
def using(ts: DefaultProduction[Token, Token]) -> UsingStatement:
    return UsingStatement(NamespaceAccessor(ts[1]))


###########################
# ANONEMOUS FUNCTIONS
###########################


@par.rule(
    "args do line end",
    "args do lines end",
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
    "var_change",
    "struct_def",
    "for_loop",
    "if_chain",
    "freeze",
    "f_call",
    "shout",
    "using",
    "ret",
    unless_ends=["RPAR", "COM", "BAR"],
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
