from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING

from .base_node import BaseNode

if TYPE_CHECKING:
    from .namespace_acessor import NamespaceAccessor


class UsingStatement(BaseNode, ABC):
    __slots__ = ("_nsa", "_lines", "_line_no")

    def __init__(
        self: BaseNode, nsa: NamespaceAccessor, lines: str, line_no: int
    ) -> None:
        self._nsa = nsa

        self._lines = lines
        self._line_no = line_no

    @property
    def path(self):
        return self._nsa

    def compile(self, **kwargs):
        return super().compile(**kwargs)
