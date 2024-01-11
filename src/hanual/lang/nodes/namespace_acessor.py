from __future__ import annotations

from bytecode import Instr

from typing import TYPE_CHECKING, Generator, Self, Optional

from hanual.lang.nodes.base_node import BaseNode
from hanual.util import Reply, Request, Response, REQUEST_TYPE
from hanual.lang.util.compileable_object import CompilableObject


if TYPE_CHECKING:
    from hanual.lang.util.line_range import LineRange

    from hanual.lang.builtin_lexer import Token


class NamespaceAccessor(BaseNode):
    __slots__ = ("_path", "_lines", "_line_range")

    def __init__(self, first: Token, lines: str, line_range: LineRange) -> None:
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

    def gen_code(self) -> Generator[Response[Instr] | Request[REQUEST_TYPE], Optional[Reply], None]:
        raise NotImplementedError

    def prepare(self) -> Generator[Request[object], Reply[object] | None, None]:
        raise NotImplementedError
