from __future__ import annotations

from .base_node import BaseNode
from .anon_args import AnonArgs
from .block import CodeBlock
from abc import ABC


class AnonymousFunction(BaseNode, ABC):
    __slots__ = ("_args", "_inner",)

    def __init__(self: BaseNode, args: AnonArgs, inner: CodeBlock) -> None:
        self._inner = inner
        self._args = args
