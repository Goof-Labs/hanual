from __future__ import annotations

from typing import TYPE_CHECKING, Generator

from hanual.compile.bytecode_instruction import ByteCodeInstruction

from hanual.lang.lexer import Token
from hanual.lang.nodes.base_node import BaseNode
from hanual.lang.nodes.dot_chain import DotChain

from hanual.util import Reply, Response, Request


if TYPE_CHECKING:
    from hanual.lang.util.line_range import LineRange
    from .arguments import Arguments


class FunctionCall[N: (Token, DotChain)](BaseNode):
    PRESERVE_RETURN = ...

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
        yield Response(ByteCodeInstruction("LOAD_GLOBAL", self._name.value))
        yield from self._args.gen_code()
        yield Response(ByteCodeInstruction("CALL", len(self._args.children)))

        capture_return: Response = yield Request(Request.GET_LAST_CONTEXT, FunctionCall.PRESERVE_RETURN)

        if capture_return.response is False:
            yield Response(ByteCodeInstruction("POP_TOP"))

    def prepare(self) -> Generator[Response | Request, Reply, None]:
        yield Request(Request.ADD_NAME, self._name.value).make_lazy()
        yield from self._args.prepare()
