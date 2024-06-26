from __future__ import annotations

from typing import TYPE_CHECKING

from hanual.lang.util.type_objects import GENCODE_RET, PREPARE_RET
from hanual.lang.nodes.base_node import BaseNode
from hanual.lang.util.node_utils import Intent

if TYPE_CHECKING:
    from .block import CodeBlock


class ElseStatement(BaseNode):
    __slots__ = (
        "_body",
        "_lines",
        "_line_range",
    )

    def __init__(self, body: CodeBlock) -> None:
        self._body = body

    @property
    def body(self) -> CodeBlock:
        return self._body

    def gen_code(self, *intents: Intent, **options) -> GENCODE_RET:
        yield from self._body.gen_code()

    def prepare(self) -> PREPARE_RET:
        yield from self._body.prepare()
