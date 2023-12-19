from __future__ import annotations

from typing import Generator
from typing import TYPE_CHECKING

from bytecode import Instr
from hanual.compile.context import Context
from hanual.lang.lexer import Token
from hanual.lang.nodes.base_node import BaseNode
from hanual.lang.nodes.base_node import defines_protocols
from hanual.lang.nodes.dot_chain import DotChain
from hanual.util import Reply
from hanual.util import Request
from hanual.util import Response


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
        print("HERE")

        from hanual.lang.nodes.assignment import AssignmentNode

        yield Response(Instr("LOAD_NAME", self._name.value))
        yield from self._args.gen_code()
        yield Response(Instr("CALL", len(self._args) - 1))

        ctx: Context = yield Request(Request.GET_CONTEXT)

        if ctx.assert_instance("parent", AssignmentNode) is False:
            yield Response(Instr("POP_TOP"))

    def prepare(self) -> Generator[Response | Request, Reply, None]:
        yield Request(Request.ADD_NAME, self._name.value).make_lazy()
        yield from self._args.prepare()
