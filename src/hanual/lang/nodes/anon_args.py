from __future__ import annotations

from typing import TYPE_CHECKING
from .arguments import Arguments
from .base_node import BaseNode
from abc import ABC

if TYPE_CHECKING:
    ...


class AnonArgs(BaseNode, ABC):
    __slots__ = ("_args",)

    def __init__(self: BaseNode, args: Arguments) -> None:
        self._args = args

    def compile(self) -> None:
        raise NotImplementedError
