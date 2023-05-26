from __future__ import annotations

# from hanual.compile.instruction import (
#    InstructionPK1,
#    InstructionPK2,
#    InstructionPK3,
#    InstructionPK4,
#    InstructionPK5,
#    InstructionPKN,
#    InstructionPGA,
#    InstructionCAL,
# )
from typing import Any, Dict, TYPE_CHECKING
from .base_node import BaseNode

if TYPE_CHECKING:
    from hanual.compile import Assembler
    from hanual.lang.lexer import Token
    from .arguments import Arguments


class FunctionCall(BaseNode):
    def __init__(self: BaseNode, name: Token, arguments: Arguments) -> None:
        self._args: Arguments = arguments
        self._name: Token = name

    def compile(self, global_state: Assembler) -> Any:
        return NotImplementedError
        self._args.compile(global_state)

        #  we have special instructions that pack N amounts of elements on stack into a tuple, this lets us use them
        n_children = len(self._args.children)

        if n_children == 1:
            global_state.add_instructions(InstructionPK1())

        elif n_children == 2:
            global_state.add_instructions(InstructionPK2())

        elif n_children == 3:
            global_state.add_instructions(InstructionPK3())

        elif n_children == 4:
            global_state.add_instructions(InstructionPK4())

        elif n_children == 5:
            global_state.add_instructions(InstructionPK5())

        else:
            global_state.add_instructions(InstructionPKN(n_children))

        fn_addr = global_state.add_reference(self._name.value)
        # push function reference
        global_state.add_instructions(InstructionPGA(fn_addr))
        global_state.add_instructions(InstructionCAL())  # call function

    @property
    def name(self) -> Token:
        return self._name

    @property
    def args(self) -> Arguments:
        return self._args

    def as_dict(self) -> Dict[str, Any]:
        return {"args": self._args.as_dict(), "name": self._name}
