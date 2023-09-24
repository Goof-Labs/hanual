from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING, Any, Union

from hanual.compile.constants import BaseConstant
from hanual.compile.constants.constant import Constant
from hanual.compile.instruction import *
from hanual.exec.result import Result
from hanual.exec.scope import Scope
from hanual.exec.wrappers import LiteralWrapper
from hanual.lang.errors import ErrorType, Frame, HanualError, TraceBack
from hanual.lang.lexer import Token

from .base_node import BaseNode
from .block import CodeBlock

if TYPE_CHECKING:
    ...


class LoopLoop(BaseNode, ABC):
    __slots__ = ("_inner",)

    def __init__(self, inner: CodeBlock) -> None:
        self._inner: CodeBlock = inner

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
                err.add_frame(Frame("loop"))
                return res
