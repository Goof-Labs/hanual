from __future__ import annotations

# from hanual.compile.instruction import (
#    InstructionPGC,
#    InstructionPK2,
#    InstructionPGA,
#    InstructionCAL,
# )
from typing import Any, Dict, Optional, TYPE_CHECKING
from typing_extensions import Self
from .base_node import BaseNode


if TYPE_CHECKING:
    from hanual.compile import Assembler
    from hanual.lang.lexer import Token


class RangeNode(BaseNode):
    def __init__(
        self: Self,
        from_: Optional[Token] = None,
        to_: Optional[Token] = None,
    ) -> None:
        self._from = from_
        self._to = to_

    def compile(self) -> None:
        raise NotImplementedError

    def as_dict(self) -> Dict[str, Any]:
        return {
            "from": self._from,
            "to": self._to,
        }
