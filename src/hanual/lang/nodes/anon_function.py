from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING, Generator, Optional, Union

from hanual.lang.lexer import Token

from .base_node import BaseNode
from .block import CodeBlock

if TYPE_CHECKING:
    from hanual.lang.nodes.binop import BinOpNode
    from hanual.lang.nodes.range_node import RangeNode
    from hanual.lang.util.line_range import LineRange

    from .parameters import Parameters


class AnonymousFunction(BaseNode, ABC):
    __slots__ = ("_args", "_inner", "fn_name", "_lines", "_line_no", "_return")

    def __init__(
        self: BaseNode,
        args: Parameters,
        inner: CodeBlock,
        ret: Optional[Union[Token, BinOpNode, RangeNode]] = None,
        lines: str = "",
        line_range: LineRange = 0,
    ) -> None:
        self._inner = inner
        self._args = args
        self._return = ret

        self._line_range = line_range
        self._lines = lines

    def compile(self) -> None:
        raise NotImplementedError
