from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING, List, Union

from .base_node import BaseNode

if TYPE_CHECKING:
    from typing_extensions import Self

    from hanual.lang.builtin_lexer import Token


class NamespaceAccessor(BaseNode, ABC):
    __slots__ = ("_path", "_lines", "_line_range")

    def __init__(self: BaseNode, first: Token, lines: str, line_range: int) -> None:
        self._path: List[Token] = [first]

        self._lines = lines
        self._line_range = line_range

    def add_child(self, child: Union[Token, NamespaceAccessor]) -> Self:
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

    def compile(self) -> None:
        raise NotImplementedError
