from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING

from hanual.compile.constant import Constant
from hanual.lang.nodes.base_node import BaseNode

from .base_node import BaseNode

if TYPE_CHECKING:
    from .block import CodeBlock
    from .conditions import Condition


class ElifStatement(BaseNode, ABC):
    def __init__(self: BaseNode, condition: Condition, block: CodeBlock) -> None:
        self._condition = condition
        self._block = block

    @property
    def condition(self) -> Condition:
        return self._condition

    @property
    def block(self) -> CodeBlock:
        return self._block

    def compile(self) -> None:
        raise NotImplementedError

    def find_priority(self) -> list[BaseNode]:
        return []

    def get_constants(self) -> list[Constant]:
        consts = []

        consts.extend(self._condition.get_constants())
        consts.extend(self._block.get_constants())

        return consts

    def get_names(self) -> list[Constant]:
        names = []

        names.extend(self._condition.get_names())
        names.extend(self._block.get_names())

        return names

    def execute(self):
        raise NotImplementedError
