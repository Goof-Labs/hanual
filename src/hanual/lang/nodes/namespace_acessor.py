from __future__ import annotations

from typing import TYPE_CHECKING, Generator, Self

from .base_node import BaseNode
from hanual.util import Reply, Response, Request

if TYPE_CHECKING:
    from hanual.lang.util.line_range import LineRange

    from hanual.lang.builtin_lexer import Token


class NamespaceAccessor[C: (Token, "NamespaceAccessor")](BaseNode):
    __slots__ = ("_path", "_lines", "_line_range")

    def __init__(self, first: Token, lines: str, line_range: LineRange) -> None:
        self._path: list[C] = []
        self.add_child(first)

        self._lines = lines
        self._line_range = line_range

    def add_child(self, child: C) -> Self:
        if isinstance(child, NamespaceAccessor):
            self._path.extend(child.path)

        else:
            self._path.append(child)
        return self

    @property
    def full_path(self) -> str:
        return "/".join(map(lambda x: x.value, self._path))

    @property
    def path(self):
        return self._path

    def compile(self) -> Generator[Response | Request, Reply, None]:
        raise NotImplementedError
