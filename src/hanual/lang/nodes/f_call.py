from __future__ import annotations

from hanual.compile.instruction import Instruction, InstructionEnum
from hanual.compile import GlobalState
from hanual.lang.lexer import Token
from .arguments import Arguments
from .base_node import BaseNode
from typing import Any


class FunctionCall(BaseNode):
    def __init__(self: BaseNode, name: Token, arguments: Arguments) -> None:
        self._args: Arguments = arguments
        self._name: Token = name

    def compile(self, global_state: GlobalState) -> Any:
        args = self._args.compile(global_state)
        f_idx = global_state.references.add_ref(self._name)

        if len(args) == 0:
            pshrgs = Instruction(InstructionEnum.PK1)

        elif len(args) == 1:
            pshrgs = Instruction(InstructionEnum.PK1)

        elif len(args) == 2:
            pshrgs = Instruction(InstructionEnum.PK1)

        elif len(args) == 3:
            pshrgs = Instruction(InstructionEnum.PK1)

        elif len(args) == 4:
            pshrgs = Instruction(InstructionEnum.PK1)

        elif len(args) == 5:
            pshrgs = Instruction(InstructionEnum.PK1)

        else:
            pshrgs = Instruction(InstructionEnum.PKN, len(args))

        return (
            *args,
            pshrgs,
            Instruction(InstructionEnum.PGA, f_idx),
            Instruction(InstructionEnum.CAL),
        )

    @property
    def name(self) -> Token:
        return self._name

    @property
    def args(self) -> Arguments:
        return self._args

    def __str__(self: FunctionCall, level=0) -> str:
        return f"{type(self).__name__}(\n{' '.rjust(level)}name = {self.name.__str__(level+1) if issubclass(type(self.name), BaseNode) else str(self.name)}\n{' '.rjust(level)}args = {self.args.__str__(level+1) if issubclass(type(self.args), BaseNode) else str(str(self.args))})\n"
