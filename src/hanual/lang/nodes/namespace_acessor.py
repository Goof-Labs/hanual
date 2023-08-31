from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING, List, Union

from hanual.compile.constants.constant import Constant

from .base_node import BaseNode

if TYPE_CHECKING:
    from typing_extensions import Self

    from hanual.lang.builtin_lexer import Token


class NamespaceAccessor(BaseNode, ABC):
    __slots__ = "_path",

    def __init__(self: BaseNode, first: Token) -> None:
        self._path: List[Token] = [first]

    def add_child(self, child: Union[Token, NamespaceAccessor]) -> Self:
        if isinstance(child, NamespaceAccessor):
            self._path.extend(child.path)

        else:
            self._path.append(child)
        return self

    def find_priority(self) -> list[BaseNode]:
        return []

    @property
    def full_path(self) -> str:
        return "/".join(map(lambda x: x.value, self._path))

    @property
    def path(self):
        return self._path

    def compile(self) -> None:
        raise NotImplementedError

    def execute(self, env):
        raise NotImplementedError

    def get_constants(self) -> list[Constant]:
        return []

    def get_names(self) -> list[str]:
        return [self._path[-1].value]
