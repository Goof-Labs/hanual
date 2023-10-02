from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING, Generator

from hanual.compile.constants.constant import Constant
from hanual.exec.result import Result
from hanual.exec.scope import Scope
from hanual.lang.errors.trace_back import Frame

from .base_node import BaseNode

if TYPE_CHECKING:
    from .block import CodeBlock
    from .conditions import Condition


class ElifStatement(BaseNode, ABC):
    __slots__ = "_condition", "_block", "_lines", "_line_no",

    def __init__(self, condition: Condition, block: CodeBlock, lines: str, line_no: int) -> None:
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

    def compile(self) -> None:
        raise NotImplementedError

    def get_constants(self) -> Generator[Constant]:
        yield from self._condition.get_constants()
        yield from self._block.get_constants()

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
            inner_scope = Scope(
                parent=scope, frame=Frame(name=type(self).__name__, line=..., line_num=...)
            )
            _, err = res.inherit_from(self.block.execute(inner_scope))

            if err:
                return res

            return res.success(should_run)
