from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING

from .base_node import BaseNode

if TYPE_CHECKING:
    from .arguments import Arguments


class AnonArgs(BaseNode, ABC):
    __slots__ = ("_args",)

    def __init__(self: BaseNode, args: Arguments) -> None:
        self._args = args

    def compile(self) -> None:
        raise NotImplementedError
