from __future__ import annotations

from typing import TYPE_CHECKING, List

from hanual.compile.constants.constant import Constant
from hanual.compile.instruction import *

from .base_node import BaseNode

if TYPE_CHECKING:
    from .arguments import Arguments

from .arguments import Arguments


class HanualList(BaseNode):
    def __init__(self, args: Arguments) -> None:
        self._elements = args

    @property
    def elements(self) -> List:
        return self._elements.children

    def get_constants(self) -> list[Constant]:
        yield from self._elements.get_constants()

    def get_names(self):
        return self._elements.get_names()

    def compile(self) -> None:
        data = []

        for e in self._elements.children:
            if issubclass(type(e), Constant):
                data.append(MOV_HC[new_heap(), e])

    def execute(self, env):
        raise NotImplementedError
