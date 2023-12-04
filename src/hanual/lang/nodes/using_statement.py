from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING
from hanual.util import Reply, Response, Request

from .base_node import BaseNode

if TYPE_CHECKING:
    from hanual.lang.util.line_range import LineRange
    from .namespace_acessor import NamespaceAccessor


class UsingStatement(BaseNode, ABC):
    __slots__ = ("_nsa", "_lines", "_line_no")

    def __init__(self, nsa: NamespaceAccessor, lines: str, line_no: LineRange) -> None:
        self._nsa = nsa

        self._lines = lines
        self._line_no = line_no

    @property
    def path(self) -> NamespaceAccessor:
        return self._nsa

    def compile(self) -> Generator[Reply | Request, Response, None]:
        raise NotImplementedError
