from __future__ import annotations

from .namespace_acessor import NamespaceAccessor
from typing import TYPE_CHECKING
from .base_node import BaseNode
from abc import ABC


if TYPE_CHECKING:
    from hanual.compile.ir import IR


class UsingStatement(BaseNode, ABC):
    __slots__ = ("_nsa",)

    def __init__(self: BaseNode, nsa: NamespaceAccessor) -> None:
        self._nsa = nsa

    @property
    def path(self):
        return self._nsa

    def compile(self, ir: IR) -> None:
        ir.dep(self.path)

    def as_dict(self):
        super().as_dict()
