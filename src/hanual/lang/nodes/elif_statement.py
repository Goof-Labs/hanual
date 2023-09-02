from __future__ import annotations

from hanual.compile.constants.constant import Constant
from hanual.exec.result import Result
from hanual.exec.scope import Scope
from typing import TYPE_CHECKING
from .base_node import BaseNode
from abc import ABC

if TYPE_CHECKING:
    from .conditions import Condition
    from .block import CodeBlock


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

    def get_names(self) -> list[str]:
        names = []

        names.extend(self._condition.get_names())
        names.extend(self._block.get_names())

        return names

    def execute(self, scope: Scope) -> Result:
        res = Result()

        should_run, err = res.inherit_from(self.condition.execute(scope=scope))

        if err:
            return res

        if should_run:
            inner_scope = Scope(parent=scope)
            _, err = res.inherit_from(self.block.execute(inner_scope))

            if err:
                return res

            return res.success(should_run)
