from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Self, Generator

from bytecode import Label, Instr

from hanual.util import Request, Response, Reply
from hanual.lang.lexer import Token
from hanual.lang.nodes.base_node import BaseNode


if TYPE_CHECKING:
    from hanual.compile.context import Context


class BreakStatement(BaseNode):
    __slots__ = ("_token", "_context", "_line_range", "_lines")

    def __init__(
        self: Self,
        node: Token,
        ctx: Optional[Token] = None,
    ) -> None:
        self._token = node
        self._context = ctx

    def gen_code(self) -> Generator[Response | Request, Reply, None]:
        # TODO implement contexts
        context: Context = yield Request(Request.GET_CONTEXT)
        end_lbl: Label = context.get("end_label", recursive=True)[0]
        yield Response(Instr("JUMP_FORWARD", end_lbl, location=self.get_location()))

    def prepare(self) -> Generator[Request, Reply, None]:
        yield from ()
