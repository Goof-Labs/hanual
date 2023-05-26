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

    def compile(self, global_state: Assembler) -> Any:
        return NotImplementedError
        # This is another builtin function, range

        # push the starting value to the top
        if self._from.type == "ID":
            global_state.pull_value(self._from.value)

        elif self._from.type == "NUM":
            id_ = global_state.add_constant(self._from.value)
            global_state.add_instructions(InstructionPGC(id_))

        # push end value to top, if there is no end value we just push infinity
        if self._to is None:
            id_ = global_state.add_constant("INF")
            global_state.push_value(id_)

        else:  # An upper bound has been defined
            if self._to.type == "ID":
                global_state.pull_value(self._to.value)

            elif self._to.type == "NUM":
                id_ = global_state.add_constant(self._to.value)
                global_state.add_instructions(InstructionPGC(id_))

        global_state.add_instructions(InstructionPK2())
        range_fn = global_state.add_reference("~range")
        global_state.add_instructions(
            (
                InstructionPGA(range_fn),
                InstructionCAL(),
            )
        )

    def as_dict(self) -> Dict[str, Any]:
        return {
            "from": self._from,
            "to": self._to,
        }
