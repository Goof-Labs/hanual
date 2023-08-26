from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

if TYPE_CHECKING:
    from hanual.lang.nodes import BaseNode

_N = TypeVar("_N", bound=BaseNode)


class ASTChecker:
    def __init__(self, ast: _N) -> None:
        """
        Similar the the strictness of rust and other static languages hanual
        has a strict type checker and ast checker. If it sees an antipatern
        that can be avoided it will flag it up. This includes flagging up
        depricated symbols and recomending what to replace them with.
        """

        self._ast = ast

    def proof_read(self):
        ...
