from __future__ import annotations

from .namespace_acessor import NamespaceAccessor
from .base_node import BaseNode
from abc import ABC


class UsingStatement(BaseNode, ABC):
    __slots__ = "_nsa",

    def __init__(self: BaseNode, nsa: NamespaceAccessor) -> None:
        self._nsa = nsa

    @property
    def path(self):
        return self._nsa

    def compile(self):
        super().compile()

    def as_dict(self):
        super().as_dict()
