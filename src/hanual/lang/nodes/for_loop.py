from __future__ import annotations


from typing import TYPE_CHECKING, Any, Dict, Union
from .implicit_condition import ImplicitCondition
from hanual.lang.nodes.base_node import BaseNode
from .implicit_binop import ImplicitBinop
from hanual.compile.instruction import *
from hanual.compile.label import Label
from .base_node import BaseNode

if TYPE_CHECKING:
    from hanual.compile.constant import Constant

    from .assignment import AssignmentNode
    from hanual.lang.errors import Error
    from hanual.lang.lexer import Token
    from .conditions import Condition
    from .block import CodeBlock


# for let i=0, < 10, +110
class ForLoop(BaseNode):
    def __init__(
        self: BaseNode,
        condition: Union[ImplicitCondition, Condition],
        init: Union[Token, AssignmentNode],
        action: ImplicitBinop,
        body: CodeBlock,
    ) -> None:
        self._while: Union[ImplicitCondition, Condition] = condition
        self._init: Union[Token, AssignmentNode] = init
        self._action: ImplicitBinop = action
        self._body: CodeBlock = body

    @property
    def condition(self) -> Union[ImplicitCondition, Condition]:
        return self.while_

    @property
    def init(self) -> Union[Token, AssignmentNode]:
        return self._init

    @property
    def action(self) -> ImplicitBinop:
        return self._action

    @property
    def body(self) -> CodeBlock:
        return self._body

    def compile(self):
        """
        For loops follow the format:
        initialize, keep going while, increment
        So I can reperesent a loop as

        INIT-CODE
        LABEL_1
        CONDITION
        JUMP_IF_FALSE LABEL_END
        INCREMENTER

        ...
        ...

        JUMP LABEL_1
        LABEL_END
        """
        instructions = []

        start_lbl = Label("FOR_START", mangle=True)
        end_lbl = Label("FOR_END", mangle=True)

        instructions.extend(self._init.compile())
        instructions.append(start_lbl)

        # Condition part
        if isinstance(self._while, ImplicitCondition):
            instructions.extend(self._while.compile(self._init.target.value))

        else:
            instructions.extend(self._while.compile())

        instructions.append(JIF(end_lbl))

        if isinstance(self._action, ImplicitBinop):
            instructions.extend(self._action.compile(self._init.target.value))

        else:
            instructions.extend(self._action.compile())

        instructions.extend(self._body.compile())

        instructions.append(JMP(start_lbl))

        return instructions

    def get_names(self) -> list[str]:
        names = []

        names.extend(self._action.get_names())
        names.extend(self._while.get_names())
        names.extend(self._init.get_names())
        names.extend(self._body.get_names())

        return names

    def get_constants(self) -> list[Constant]:
        consts = []

        consts.extend(self._action.get_constants())
        consts.extend(self._while.get_constants())
        consts.extend(self._init.get_constants())
        consts.extend(self._body.get_constants())

        return consts

    def find_priority(self):
        return []

    def execute(self):
        raise NotImplementedError

    def as_dict(self) -> Dict[str, Any]:
        return super().as_dict()
