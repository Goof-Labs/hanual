# This file is for a using statement that has an alternative name, to accommodate
# the following syntax `using std::test::name as std_test_name`
from __future__ import annotations

from typing import TYPE_CHECKING, Generator

from .base_node import BaseNode
from hanual.util import Reply, Request

if TYPE_CHECKING:
    from hanual.lang.util.line_range import LineRange
    from .namespace_acessor import NamespaceAccessor
    from hanual.lang.token import Token


class UsingStatementWithAltName(BaseNode):
    __slots__ = (
        "_path",
        "_name",
        "_lines",
        "_line_no",
    )

    def __init__(self, path: NamespaceAccessor, name: Token) -> None:
        self._path: NamespaceAccessor = path
        self._name: Token = name

    @property
    def using(self) -> NamespaceAccessor:
        return self._path

    @property
    def name(self) -> Token:
        return self._name

    def gen_code(self):
        raise NotImplementedError

    def prepare(self) -> Generator[Request[object], Reply[object] | None, None]:
        raise NotImplementedError
