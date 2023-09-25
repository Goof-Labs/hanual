from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING

from hanual.compile.constants.constant import Constant
from hanual.exec.result import Result
from hanual.lang.errors import Frame
from hanual.exec.scope import Scope

from .base_node import BaseNode
from .block import CodeBlock

if TYPE_CHECKING:
    ...


class LoopLoop(BaseNode, ABC):
    __slots__ = ("_inner", "_lines", "_line_no")

    def __init__(self, inner: CodeBlock, lines: str, line_no: int) -> None:
        self._inner: CodeBlock = inner

        self._lines = lines
        self._line_no = line_no

    @property
    def inner(self) -> CodeBlock:
        return self._inner

    def get_names(self) -> list[str]:
        return self._inner.get_names()

    def get_constants(self) -> list[Constant]:
        yield from self._inner.get_constants()

    def compile(self, **kwargs):
        raise NotImplementedError

    def execute(self, scope: Scope) -> Result:
        res = Result()

        while True:
            _, err = res.inherit_from(self._inner.execute(scope))

            if err:
                err.add_frame(Frame(name=type(self).__name__, line=self.lines, line_num=self.line_no))
                return res
