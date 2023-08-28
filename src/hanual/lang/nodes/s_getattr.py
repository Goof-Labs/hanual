from __future__ import annotations

from typing import TypeVar

from hanual.compile.constants.constant import Constant
from hanual.lang.lexer import Token
from .hanual_list import HanualList
from .f_call import FunctionCall
from .dot_chain import DotChain
from .base_node import BaseNode

_O = TypeVar("_O", Token, DotChain, FunctionCall)
P = TypeVar("P", HanualList, ...)


class SGetattr(BaseNode):
    def __init__(self: BaseNode, obj: _O, part: P) -> None:
        self._prt: P = part
        self._obj: _O = obj

    def execute(self):
        return super().execute()

    def compile(self):
        return super().compile()

    def find_priority(self) -> list[BaseNode]:
        return []

    def get_names(self) -> list[str]:
        names = []

        if isinstance(self._obj, Token):
            if self._obj.type == "ID":
                names.append(self._obj.value)

        else:
            names.extend(self._obj.get_names())

        names.extend(self._prt.get_names())

        return names

    def get_constants(self) -> list[Constant]:
        constants = []

        if isinstance(self._obj, Token):
            if self._obj.type in ("NUM", "STR"):
                constants.append(self._obj.value)

        else:
            constants.extend(self._obj.get_constants())

        constants.extend(self._prt.get_constants())

        return constants
