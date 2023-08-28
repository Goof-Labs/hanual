from __future__ import annotations

from typing import TYPE_CHECKING

from hanual.compile.constants.constant import BaseConstant

from .base_node import BaseNode

if TYPE_CHECKING:
    from .block import CodeBlock


class ElseStatement(BaseNode):
    __slots__ = "_body",

    def __init__(self: BaseNode, body: CodeBlock) -> None:
        self._body = body

    @property
    def body(self) -> CodeBlock:
        return self._body

    def execute(self):
        return super().execute()

    def compile(self):
        return self._body.compile()

    def find_priority(self) -> list[BaseNode]:
        return self._body.find_priority()

    def get_constants(self) -> list[BaseConstant]:
        return self._body.get_constants()

    def get_names(self) -> list[str]:
        return self._body.get_names()
