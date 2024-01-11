from __future__ import annotations

from typing import TYPE_CHECKING, Generator

from hanual.util import Reply, Response, Request


from hanual.lang.nodes.algebraic_expr import AlgebraicExpression
from hanual.lang.nodes.base_node import BaseNode

if TYPE_CHECKING:
    from hanual.lang.util.line_range import LineRange


class AlgebraicFunc(BaseNode):
    def prepare(self) -> Generator[Request, Reply, None]:
        pass

    def gen_code(self) -> Generator[Response | Request, Reply, None]:
        pass

    __slots__ = (
        "_name",
        "_expr",
        "_lines",
        "_line_range",
    )

    def __init__(
        self, name: str, expr: AlgebraicExpression, lines: str, line_range: LineRange
    ) -> None:
        self._name = name
        self._expr = expr

        self._lines = lines
        self._line_range = line_range

    def prepare(self) -> Generator[Request[object], Reply[object] | None, None]:
        raise NotImplementedError
