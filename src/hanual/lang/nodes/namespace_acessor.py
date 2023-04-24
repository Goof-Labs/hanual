from __future__ import annotations

from abc import ABC

from hanual.compile.global_state import GlobalState
from hanual.lang.builtin_lexer import Token
from typing import TypeVar, List, Any, Self
from .base_node import BaseNode

T = TypeVar("T", Token, ...)


class NamespaceAcessor(BaseNode, ABC):
    def __init__(self: BaseNode, first: T) -> None:
        self._path: List[Token] = [first]

    def add_child(self, child: T) -> Self:
        self._path.append(child)
        return self

    def compile(self, global_state: GlobalState) -> Any:
        # we dont need to load any moduals because they are packed with the final runnable
        global_state.external_deps.add_dependancy(self._path)
        return ()
