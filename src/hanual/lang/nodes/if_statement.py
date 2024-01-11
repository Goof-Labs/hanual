from __future__ import annotations


from bytecode import Label, Instr

from typing import TYPE_CHECKING, Generator, Optional

from hanual.lang.nodes.base_node import BaseNode
from hanual.util import Reply, Response, Request, REQUEST_TYPE


if TYPE_CHECKING:
    from .block import CodeBlock
    from .conditions import Condition


class IfStatement(BaseNode):
    __slots__ = "_condition", "_block", "_lines", "_line_range"

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
        false_jump = Label()

        yield from self._condition.gen_code()
        yield Response(
            Instr("POP_JUMP_IF_FALSE", false_jump, location=self.get_location())
        )

        yield from self._block.gen_code()

        yield Response(false_jump)

    def prepare(self) -> Generator[Request[object], Reply[object] | None, None]:
        yield from self._condition.prepare()
        yield from self._block.prepare()
