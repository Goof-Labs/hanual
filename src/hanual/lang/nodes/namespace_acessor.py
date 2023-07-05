from __future__ import annotations


from typing import List, Union, TYPE_CHECKING
from hanual.compile.constant import Constant
from typing_extensions import Self
from .base_node import BaseNode
from abc import ABC

if TYPE_CHECKING:
    from hanual.lang.builtin_lexer import Token


class NamespaceAccessor(BaseNode, ABC):
    def __init__(self: BaseNode, first: Token) -> None:
        self._path: List[Token] = [first]

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

    def execute(self):
        raise NotImplementedError

    def get_constants(self) -> list[Constant]:
        return []

    def get_names(self) -> list[str]:
        return [self._path[-1].value]
