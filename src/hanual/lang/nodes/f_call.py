from __future__ import annotations

from typing import TYPE_CHECKING, Generator

from hanual.compile.bytecode_instruction import ByteCodeInstruction
from hanual.compile.context import Context

from hanual.lang.lexer import Token
from hanual.lang.nodes.base_node import BaseNode, defines_protocols
from hanual.lang.nodes.dot_chain import DotChain

from hanual.util import Reply, Response, Request


if TYPE_CHECKING:
    from .arguments import Arguments


@defines_protocols
class FunctionCall[N: (Token, DotChain)](BaseNode):
    PRESERVE_RETURN = 0

    __slots__ = (
        "_name",
        "_args",
        "_lines",
        "_line_range",
    )

    def __init__(
            self,
            name: N,
            arguments: Arguments,
    ) -> None:
        self._name: N = name
        self._args: Arguments = arguments

    @property
    def name(self) -> N:
        return self._name

    @property
    def args(self) -> Arguments:
        return self._args

    def gen_code(self) -> Generator[Response | Request, Reply, None]:
        from hanual.lang.nodes.assignment import AssignmentNode

        yield Response(ByteCodeInstruction("LOAD_GLOBAL", self._name.value))
        yield from self._args.gen_code()
        yield Response(ByteCodeInstruction("CALL", len(self._args.children)))

        ctx: Context = yield Request(Request.GET_CONTEXT)

        if ctx.assert_instance("parent", AssignmentNode) is False:
            yield Response(ByteCodeInstruction("POP_TOP"))

    def prepare(self) -> Generator[Response | Request, Reply, None]:
        yield Request(Request.ADD_NAME, self._name.value).make_lazy()
        yield from self._args.prepare()
