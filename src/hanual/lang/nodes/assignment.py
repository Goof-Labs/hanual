from __future__ import annotations

from typing import TYPE_CHECKING, Generator

from hanual.lang.lexer import Token
from hanual.lang.nodes.base_node import BaseNode

from hanual.util import Reply, Response, Request

if TYPE_CHECKING:
    from hanual.lang.util.line_range import LineRange


class AssignmentNode[T](BaseNode):
    __slots__ = ("_target", "_value", "_lines", "_line_range")

    def __init__(self, target: Token, value: T) -> None:
        self._target: Token = target
        self._value: T = value

    @property
    def target(self) -> Token:
        return self._target

    @property
    def value(self) -> T:
        return self._value

    def gen_code(self, **kwargs):
        raise NotImplementedError

    def prepare(self) -> Generator[Response | Request, Reply, None]:
        yield from self._target.prepare()
        yield from self._value.prepare()
