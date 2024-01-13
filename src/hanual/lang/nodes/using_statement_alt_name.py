# This file is for a using statement that has an alternative name, to accommodate
# the following syntax `using std::test::name as std_test_name`
from __future__ import annotations

from typing import TYPE_CHECKING

from hanual.lang.util.type_objects import GENCODE_RET, PREPARE_RET

from .base_node import BaseNode

if TYPE_CHECKING:
    from hanual.lang.token import Token

    from .namespace_acessor import NamespaceAccessor


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

    def gen_code(self) -> GENCODE_RET:
        raise NotImplementedError

    def prepare(self) -> PREPARE_RET:
        raise NotImplementedError
