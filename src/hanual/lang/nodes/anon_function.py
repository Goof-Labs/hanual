from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING, Optional, Union

from hanual.lang.lexer import Token

from .anon_args import AnonArgs
from .base_node import BaseNode
from .block import CodeBlock

if TYPE_CHECKING:
    from hanual.lang.nodes.binop import BinOpNode
    from hanual.lang.nodes.range_node import RangeNode


class AnonymousFunction(BaseNode, ABC):
    __slots__ = ("_args", "_inner", "fn_name")

    def __init__(
        self: BaseNode,
        args: AnonArgs,
        inner: CodeBlock,
        retrn: Optional[Union[Token, BinOpNode, RangeNode]] = None,
    ) -> None:
        self._inner = inner
        self._args = args

    def compile(self) -> None:
        raise NotImplementedError
