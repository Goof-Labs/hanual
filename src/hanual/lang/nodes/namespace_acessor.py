from __future__ import annotations

from typing import TYPE_CHECKING, Self

from hanual.lang.nodes.base_node import BaseNode
from hanual.lang.util.compileable_object import CompilableObject
from hanual.lang.util.type_objects import GENCODE_RET, PREPARE_RET

if TYPE_CHECKING:
    from hanual.lang.builtin_lexer import Token


class NamespaceAccessor(BaseNode):
    __slots__ = ("_path", "_lines", "_line_range")

    def __init__(self, first: Token) -> None:
        self._path: list[CompilableObject] = []
        self.add_child(first)

    def add_child(self, child: CompilableObject) -> Self:
        if isinstance(child, NamespaceAccessor):
            self._path.extend(child.path)

        elif isinstance(child, Token):
            self._path.append(child)

        else:
            raise NotImplementedError(f"Child {child} has not been implemented yet")

        return self

    @property
    def full_path(self) -> str:
        raise NotImplementedError

    @property
    def path(self):
        return self._path

    def gen_code(self) -> GENCODE_RET:
        raise NotImplementedError

    def prepare(self) -> PREPARE_RET:
        raise NotImplementedError
