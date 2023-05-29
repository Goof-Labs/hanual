from __future__ import annotations


from typing import TYPE_CHECKING, Any, Dict, List, Optional

from hanual.compile.ir import IR
from .base_node import BaseNode

if TYPE_CHECKING:
    from hanual.lang.lexer import Token
    from .arguments import Arguments


class HanualList(BaseNode):
    def __init__(self: BaseNode, args: Arguments) -> None:
        self._elements = args.children

    @property
    def elements(self) -> List:
        return self._elements

    def compile(self, ir: IR, to: str | None) -> None:
        return super().compile(ir, to)

    def as_dict(self) -> Dict[str, Any]:
        return super().as_dict()
