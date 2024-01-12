from __future__ import annotations

from typing import TYPE_CHECKING, Self

from hanual.lang.lexer import Token
from hanual.lang.nodes.base_node import BaseNode
from hanual.lang.util.type_objects import GENCODE_RET, PREPARE_RET

if TYPE_CHECKING:
    pass


class Parameters(BaseNode):
    __slots__ = (
        "_children",
        "_lines",
        "_line_range",
    )

    def __init__(
        self,
        children: Token | list[Token],
    ) -> None:
        self._children: list[Token] = []
        self.add_child(children)

    def add_child(self, child: Token | Parameters | list) -> Self:
        if isinstance(child, Parameters):
            self._children.extend(child.children)

        elif isinstance(child, list):
            self._children.extend(child)

        else:
            self._children.append(child)

        return self

    @property
    def children(self) -> list[Token]:
        return self._children

    def gen_code(self) -> GENCODE_RET:
        raise NotImplementedError

    def prepare(self) -> PREPARE_RET:
        raise NotImplementedError
