from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING

from hanual.exec.result import Result

from .base_node import BaseNode

if TYPE_CHECKING:
    from hanual.compile.compile_manager import CompileManager
    from hanual.compile.constants.constant import Constant
    from hanual.exec.scope import Scope

    from .namespace_acessor import NamespaceAccessor


class UsingStatement(BaseNode, ABC):
    __slots__ = ("_nsa", "_lines", "_line_no")

    def __init__(self: BaseNode, nsa: NamespaceAccessor, lines: str, line_no: int) -> None:
        self._nsa = nsa

        self._lines = lines
        self._line_no = line_no

    @property
    def path(self):
        return self._nsa

    def compile(self, cm: CompileManager) -> list[BaseNode]:
        cm.add_import(self._nsa.full_path)
        return []

    def get_constants(self) -> list[Constant]:
        ...

    def get_names(self) -> list[str]:
        return []

    def execute(self, scope: Scope) -> Result[None, None]:
        return Result().success(None)
