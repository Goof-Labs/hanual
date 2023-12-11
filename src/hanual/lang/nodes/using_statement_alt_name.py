# This file is for a using statement that has an alternative name, to accommodate
# the following syntax `using std::test::name as std_test_name`
from __future__ import annotations

from typing import TYPE_CHECKING

from .base_node import BaseNode
from hanual.util import Reply, Response, Request

if TYPE_CHECKING:
    from hanual.lang.util.line_range import LineRange
    from .namespace_acessor import NamespaceAccessor
    from hanual.lang.lexer import Token


class UsingStatementWithAltName(BaseNode):
    __slots__ = (
        "_path",
        "_name",
        "_lines",
        "_line_no",
    )

    def __init__(
            self, path: NamespaceAccessor, name: Token, lines: str, line_no: LineRange
    ) -> None:
        self._path: NamespaceAccessor = path
        self._name: Token = name

        self._line_no = line_no
        self._lines = lines

    @property
    def using(self) -> NamespaceAccessor:
        return self._path

    @property
    def name(self) -> Token:
        return self._name

    def gen_code(self):
        raise NotImplementedError

    def prepare(self) -> Generator[Response | Request, Reply, None]:
        raise NotImplementedError
