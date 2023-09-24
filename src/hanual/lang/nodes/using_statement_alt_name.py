# This file is for a using statement that has an alternative name, to accomodate
# the following syntax `using std::test::name as std_test_name`
from __future__ import annotations

from typing import TYPE_CHECKING

from .base_node import BaseNode

if TYPE_CHECKING:
    from hanual.compile.constants.constant import Constant
    from hanual.lang.lexer import Token

    from .namespace_acessor import NamespaceAccessor


class UsingStatementWithAltName(BaseNode):
    __slots__ = "_path", "_name", "_lines", "_line_no",

    def __init__(self: BaseNode, path: NamespaceAccessor, name: Token, lines: str, line_no: int) -> None:
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

    def compile(self) -> None:
        raise NotImplementedError

    def get_constants(self) -> list[Constant]:
        ...

    def get_names(self) -> list[str]:
        return [self._name.value]

    def execute(self, env):
        raise NotImplementedError
