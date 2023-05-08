from __future__ import annotations

from hanual.compile.instruction import Instruction, InstructionEnum
from typing import Any, Dict, Self, Optional, TYPE_CHECKING
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

    def compile(self, global_state: Assembler) -> Any:
        # This is another builtin function, range

        # push the starting value to the top
        if self._from.type == "ID":
            global_state.pull_value(self._from.value)

        elif self._from.type == "NUM":
            idnt = global_state.add_constant(self._from.value)
            global_state.add_instructions(Instruction(InstructionEnum.PGC, idnt))

        # push end value to top, if there is no end value we just push infinity
        raise NotImplementedError

    def as_dict(self) -> Dict[str, Any]:
        return {
            "from": self._from,
            "to": self._to,
        }
