from __future__ import annotations

from typing import TYPE_CHECKING, Generator

from hanual.lang.nodes.base_node import BaseNode

from hanual.util import Reply, Request

if TYPE_CHECKING:
    from hanual.lang.util.line_range import LineRange
    from hanual.lang.lexer import Token


class StrongField[T](BaseNode):
    __slots__ = (
        "_name",
        "_type",
        "_lines",
        "_line_range",
    )

    def __init__(
        self, name: Token, type_: T, lines: str, line_range: LineRange
    ) -> None:
        self._name: Token = name
        self._type: T = type_

        self._line_range = line_range
        self._lines = lines

    @property
    def name(self) -> Token:
        return self._name

    @property
    def type(self) -> T:
        return self._type

    def gen_code(self):
        raise NotImplementedError

    def prepare(self) -> Generator[Request[object], Reply[object] | None, None]:
        raise NotImplementedError
