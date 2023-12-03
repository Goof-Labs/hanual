from __future__ import annotations

from typing import TYPE_CHECKING, Generator

from hanual.lang.lexer import Token

from hanual.compile.back_end.response import Response
from hanual.compile.back_end.request import Request
from hanual.compile.back_end.reply import Reply

from hanual.compile.instruction.ir_push import PUSH
from hanual.compile.instruction.ir_ld import LD

from .base_node import BaseNode
from .dot_chain import DotChain


if TYPE_CHECKING:
    from hanual.lang.util.line_range import LineRange
    from .arguments import Arguments


class FunctionCall[N: (Token, DotChain)](BaseNode):
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
            lines: str,
            line_range: LineRange,
    ) -> None:
        self._name: N = name
        self._args: Arguments = arguments

        self._line_range = line_range
        self._lines = lines

    @property
    def name(self) -> N:
        return self._name

    @property
    def args(self) -> Arguments:
        return self._args

    def compile(self) -> Generator[Reply | Request, Response, None]:
        res = yield Request(
            Request.MAKE_CONSTANT, self.name,
            Request.MAKE_CONSTANT, len(self._args.children),
            Request.MAKE_REGISTER,
            Request.MAKE_REGISTER,
        )
        r0, r1, name_const, num_children = res.response

        yield Response(LD[r0](name_const))
        yield Response(PUSH[r0]())

        yield Response(LD[r1](num_children))
        yield Response(PUSH[r0]())

        yield from self._args.compile()
