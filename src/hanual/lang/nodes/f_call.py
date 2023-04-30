from __future__ import annotations

from hanual.compile.instruction import Instruction, InstructionEnum
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
        self._args.compile(global_state)

        #  we have special instructions that pack N amounts of elements on stack into a tuple, this lets us use them
        n_children = len(self._args.children)

        if n_children == 1:
            global_state.add_instructions(Instruction(InstructionEnum.PK1))

        elif n_children == 2:
            global_state.add_instructions(Instruction(InstructionEnum.PK2))

        elif n_children == 3:
            global_state.add_instructions(Instruction(InstructionEnum.PK3))

        elif n_children == 4:
            global_state.add_instructions(Instruction(InstructionEnum.PK4))

        elif n_children == 5:
            global_state.add_instructions(Instruction(InstructionEnum.PK5))

        else:
            global_state.add_instructions(Instruction(InstructionEnum.PKN, n_children))

        global_state.add_instructions(Instruction(InstructionEnum.PGA, self._name.value))  # push function reference
        global_state.add_instructions(Instruction(InstructionEnum.CAL))  # call function

    @property
    def name(self) -> Token:
        return self._name

    @property
    def args(self) -> Arguments:
        return self._args

    def as_dict(self) -> Dict[str, Any]:
        return {"args": self._args.as_dict(), "name": self._name}
