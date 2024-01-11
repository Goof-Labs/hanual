from __future__ import annotations

from bytecode import Instr

from typing import TYPE_CHECKING, Generator, Optional

from hanual.lang.nodes.base_node import BaseNode
from hanual.util import Reply, Request, Response, REQUEST_TYPE

if TYPE_CHECKING:
    from .block import CodeBlock
    from .conditions import Condition


class ElifStatement(BaseNode):
    __slots__ = (
        "_condition",
        "_block",
        "_lines",
        "_line_no",
    )

    def __init__(self, condition: Condition, block: CodeBlock) -> None:
        self._condition: Condition = condition
        self._block: CodeBlock = block

    @property
    def condition(self) -> Condition:
        return self._condition

    @property
    def block(self) -> CodeBlock:
        return self._block

    def gen_code(self) -> Generator[Response[Instr] | Request[REQUEST_TYPE], Optional[Reply], None]:
        raise NotImplementedError

    def prepare(self) -> Generator[Request[object], Reply[object] | None, None]:
        raise NotImplementedError
