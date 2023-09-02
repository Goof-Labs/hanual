from __future__ import annotations

from hanual.compile.constants.constant import BaseConstant
from hanual.exec.scope import Scope
from typing import TYPE_CHECKING
from .base_node import BaseNode

if TYPE_CHECKING:
    from hanual.exec.result import Result
    from .block import CodeBlock


class ElseStatement(BaseNode):
    __slots__ = "_body",

    def __init__(self: BaseNode, body: CodeBlock) -> None:
        self._body = body

    @property
    def body(self) -> CodeBlock:
        return self._body

    def execute(self, scope: Scope) -> Result:
        return self._body.execute(Scope(scope))

    def compile(self, cm):
        return self._body.compile(cm=cm)

    def find_priority(self) -> list[BaseNode]:
        return self._body.find_priority()

    def get_constants(self) -> list[BaseConstant]:
        return self._body.get_constants()

    def get_names(self) -> list[str]:
        return self._body.get_names()
