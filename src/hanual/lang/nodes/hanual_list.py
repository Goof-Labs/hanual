from __future__ import annotations


from hanual.compile.instruction import new_heap
from hanual.compile.constant import Constant
from hanual.compile.instruction import *
from typing import TYPE_CHECKING, List
from .base_node import BaseNode

if TYPE_CHECKING:
    from .arguments import Arguments


class HanualList(BaseNode):
    def __init__(self: BaseNode, args: Arguments) -> None:
        self._elements = args

    @property
    def elements(self) -> List:
        return self._elements.children

    def get_constants(self) -> list[Constant]:
        return self._elements.get_constants()

    def find_priority(self) -> list[BaseNode]:
        return self._elements.find_priority()

    def get_names(self) -> list[str]:
        return self._elements.get_names()

    def compile(self) -> None:
        data = []

        for e in self._elements:
            if issubclass(type(e), Constant):
                data.append(MOV_HC[new_heap(), e])

    def execute(self):
        return super().execute()
