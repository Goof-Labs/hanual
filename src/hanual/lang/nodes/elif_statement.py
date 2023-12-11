from __future__ import annotations

from typing import TYPE_CHECKING, Generator

from hanual.lang.nodes.base_node import BaseNode

from hanual.util import Reply, Response, Request

if TYPE_CHECKING:
    from .block import CodeBlock
    from .conditions import Condition

    from hanual.lang.util.line_range import LineRange


class ElifStatement(BaseNode):
    __slots__ = (
        "_condition",
        "_block",
        "_lines",
        "_line_no",
    )

    def __init__(
            self, condition: Condition, block: CodeBlock, lines: str, line_no: LineRange
    ) -> None:
        self._condition = condition
        self._block = block

        self._line_no = line_no
        self._lines = lines

    @property
    def condition(self) -> Condition:
        return self._condition

    @property
    def block(self) -> CodeBlock:
        return self._block

    def gen_code(self):
        raise NotImplementedError

    def prepare(self) -> Generator[Response | Request, Reply, None]:
        raise NotImplementedError
