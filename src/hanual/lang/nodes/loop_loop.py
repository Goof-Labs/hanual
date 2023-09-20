from __future__ import annotations


from hanual.lang.errors import HanualError, ErrorType, TraceBack, Frame
from hanual.compile.constants.constant import Constant
from hanual.compile.constants import BaseConstant
from hanual.exec.wrappers import LiteralWrapper
from typing import TYPE_CHECKING, Union, Any
from hanual.compile.instruction import *
from hanual.exec.result import Result
from hanual.exec.scope import Scope
from hanual.lang.lexer import Token
from .base_node import BaseNode
from .block import CodeBlock
from abc import ABC

if TYPE_CHECKING:
    ...


class LoopLoop(BaseNode, ABC):
    __slots__ = "_inner",

    def __init__(self, inner: CodeBlock) -> None:
        self._inner: CodeBlock = inner

    @property
    def inner(self) -> CodeBlock:
        return self._inner

    def get_names(self) -> list[str]:
        return self._inner.get_names()

    def find_priority(self) -> list[BaseNode]:
        return self._inner.find_priority()

    def get_constants(self) -> list[BaseConstant]:
        return super().get_constants()

    def compile(self, **kwargs):
        raise NotImplementedError

    def execute(self, scope: Scope) -> Result:
        res = Result()

        while True:
            _, err = res.inherit_from(self._inner.execute(scope))

            if err:
                err.add_frame(Frame("loop"))
                return res
