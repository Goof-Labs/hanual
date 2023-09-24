from __future__ import annotations

from typing import TypeVar

from hanual.compile.constants.constant import Constant
from hanual.lang.lexer import Token

from .base_node import BaseNode
from .dot_chain import DotChain
from .f_call import FunctionCall
from .hanual_list import HanualList

_O = TypeVar("_O", Token, DotChain, FunctionCall)
P = TypeVar("P", HanualList, ...)


class SGetattr(BaseNode):
    __slots__ = "_prt", "_obj", "_lines", "_line_no",

    def __init__(self: BaseNode, obj: _O, part: P, lines: str, line_no: int) -> None:
        self._prt: P = part
        self._obj: _O = obj

        self._line_no = line_no
        self._lines = lines

    def execute(self, env):
        raise NotImplementedError

    def compile(self):
        return super().compile()

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
        if isinstance(self._obj, Token):
            if self._obj.type in ("NUM", "STR"):
                yield self._obj.value

        else:
            yield from self._obj.get_constants()

        yield from self._prt.get_constants()
