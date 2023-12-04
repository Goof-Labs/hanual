from __future__ import annotations

from typing import TYPE_CHECKING, Generator

from hanual.lang.lexer import Token
from hanual.lang.nodes.base_node import BaseNode

from hanual.util import Reply, Response, Request

if TYPE_CHECKING:
    from hanual.lang.util.line_range import LineRange


class AssignmentNode[T](BaseNode):
    __slots__ = ("_target", "_value", "_lines", "_line_range")

    def __init__(
            self,
            target: Token,
            value: T,
            lines: str,
            line_range: LineRange,
    ) -> None:
        self._target: Token = target
        self._value: T = value

        self._line_range: LineRange = line_range
        self._lines: str = lines

    @property
    def target(self) -> Token:
        return self._target

    @property
    def value(self) -> T:
        return self._value

    def compile(self) -> Generator[Reply | Request, Response, None]:
        raise NotImplementedError
