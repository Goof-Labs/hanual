from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Self

from bytecode import Instr, Label

from hanual.lang.lexer import Token
from hanual.lang.nodes.base_node import BaseNode
from hanual.lang.util.type_objects import GENCODE_RET, PREPARE_RET
from hanual.util import Request, Response
from hanual.lang.util.node_utils import Intent

if TYPE_CHECKING:
    pass


class BreakStatement(BaseNode):
    __slots__ = ("_token", "_context", "_line_range", "_lines")

    def __init__(
        self: Self,
        node: Token,
        ctx: Optional[Token] = None,
    ) -> None:
        self._token = node
        self._context = ctx

    def gen_code(self, *intents: Intent, **options) -> GENCODE_RET:
        context = yield Request(Request.GET_CONTEXT)

        assert context is not None

        end_lbl: Label = context.response.get("end_label", recursive=True)[0]
        yield Response(Instr("JUMP_FORWARD", end_lbl, location=self.get_location()))

    def prepare(self) -> PREPARE_RET:
        yield from ()
