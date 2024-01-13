from __future__ import annotations

from typing import TYPE_CHECKING

from hanual.lang.nodes.base_node import BaseNode
from hanual.lang.util.type_objects import GENCODE_RET, PREPARE_RET

if TYPE_CHECKING:
    from hanual.lang.util.line_range import LineRange

    from .arguments import Arguments


class HanualList(BaseNode):
    __slots__ = "_elements", "_lines", "_line_range"

    def __init__(self, args: Arguments, lines: str, line_range: LineRange) -> None:
        self._elements = args

        self._line_range = line_range
        self._lines = lines

    @property
    def elements(self) -> list:
        return self._elements.children

    def gen_code(self) -> GENCODE_RET:
        raise NotImplementedError

    def prepare(self) -> PREPARE_RET:
        raise NotImplementedError
