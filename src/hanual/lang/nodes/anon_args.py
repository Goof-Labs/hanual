from __future__ import annotations

from hanual.compile import Assembler
from .arguments import Arguments
from .base_node import BaseNode
from typing import Any, Dict


class AnonArgs(BaseNode):
    __slots__ = "_args",

    def __init__(self: BaseNode, args: Arguments) -> None:
        self._args = args
        
    def compile(self, global_state: Assembler) -> Any:
        return super().compile(global_state)
    
    def as_dict(self) -> Dict[str, Any]:
        return super().as_dict()
