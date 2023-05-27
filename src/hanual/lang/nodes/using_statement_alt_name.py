# This file is for a using statement that has an alternative name, to accomodate
# the following syntax `using std::test::name as std_test_name`
from __future__ import annotations


from typing import TYPE_CHECKING, Any, Dict

from .base_node import BaseNode


if TYPE_CHECKING:
    from .namespace_acessor import NamespaceAccessor
    from hanual.lang.lexer import Token


class UsingStatementWithAltName(BaseNode):
    def __init__(self: BaseNode, path: NamespaceAccessor, name: Token) -> None:
        self._path: NamespaceAccessor = path
        self._name: Token = name

    @property
    def using(self) -> NamespaceAccessor:
        return self._path

    @property
    def name(self) -> Token:
        return self._name

    def compile(self) -> None:
        raise NotImplementedError

    def as_dict(self) -> Dict[str, Any]:
        return super().as_dict()
