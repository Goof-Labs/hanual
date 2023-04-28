from __future__ import annotations

from abc import ABC

from typing import TypeVar, List, Any, Self, Dict
from hanual.lang.builtin_lexer import Token
from hanual.compile import Assembler
from .base_node import BaseNode

T = TypeVar("T", Token, ...)


class NamespaceAcessor(BaseNode, ABC):
    def __init__(self: BaseNode, first: T) -> None:
        self._path: List[Token] = [first]

    def add_child(self, child: T) -> Self:
        self._path.append(child)
        return self

    def compile(self, global_state: Assembler) -> Any:
        # we don't need to load any moduals because they are packed with the final runnable
        global_state.add_file_dep(self._path)
        return ()

    def as_dict(self) -> Dict[str, Any]:
        return {"lib-path": self._path}
