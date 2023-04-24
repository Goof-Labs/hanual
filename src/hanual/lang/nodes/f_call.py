from __future__ import annotations

from hanual.compile.instruction import Instruction, InstructionEnum
from hanual.compile import GlobalState
from hanual.lang.lexer import Token
from .arguments import Arguments
from .base_node import BaseNode
from typing import Any, Dict


class FunctionCall(BaseNode):
    def __init__(self: BaseNode, name: Token, arguments: Arguments) -> None:
        self._args: Arguments = arguments
        self._name: Token = name

    def compile(self, global_state: GlobalState) -> Any:
        res = []

        if self._args is None:
            res.append(Instruction(InstructionEnum.PKN, 0))

        else:  # The function has args
            res.extend(self._args.compile(global_state))  # load args

            if len(self._args.children) == 0:
                res.append(Instruction(InstructionEnum.PKN, 0))

            elif len(self._args.children) == 1:
                res.append(Instruction(InstructionEnum.PK1))

            elif len(self._args.children) == 2:
                res.append(Instruction(InstructionEnum.PK2))

            elif len(self._args.children) == 3:
                res.append(Instruction(InstructionEnum.PK3))

            elif len(self._args.children) == 4:
                res.append(Instruction(InstructionEnum.PK4))

            elif len(self._args.children) == 5:
                res.append(Instruction(InstructionEnum.PK5))

            else:
                res.append(Instruction(InstructionEnum.PKN, len(self._args.children)))

        ref_id = global_state.references.add_ref(self._name)
        res.append(Instruction(InstructionEnum.PGA, ref_id))  # push reference to call

        res.append(Instruction(InstructionEnum.CAL))  # CALL

        return res

    @property
    def name(self) -> Token:
        return self._name

    @property
    def args(self) -> Arguments:
        return self._args

    def as_dict(self) -> Dict[str, ...]:
        return {"args": self._args.as_dict(), "name": self._name}
