from __future__ import annotations

from typing import TypeVar

from hanual.lang.lexer import Token

from .base_node import BaseNode
from .dot_chain import DotChain
from .f_call import FunctionCall
from .hanual_list import HanualList

_O = TypeVar("_O", Token, DotChain, FunctionCall)
P = TypeVar("P", HanualList, ...)


class SGetattr(BaseNode):
    __slots__ = (
        "_prt",
        "_obj",
        "_lines",
        "_line_range",
    )

    def __init__(self: BaseNode, obj: _O, part: P, lines: str, line_range: int) -> None:
        self._prt: P = part
        self._obj: _O = obj

        self._line_range = line_range
        self._lines = lines

    def compile(self):
        raise NotImplementedError
