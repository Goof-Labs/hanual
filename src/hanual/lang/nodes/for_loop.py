from __future__ import annotations


from hanual.lang.nodes.base_node import BaseNode
from typing import TYPE_CHECKING, Any, Dict, Union
from .base_node import BaseNode

if TYPE_CHECKING:
    from hanual.runtime.runtime import RuntimeEnvironment
    from .implicit_conditions import ImplicitCondition
    from hanual.compile.constant import Constant
    from hanual.runtime.status import ExecStatus
    from .implicit_binop import ImplicitBinop
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
        return super().compile()

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

    def execute(self, rte: RuntimeEnvironment) -> ExecStatus[Error, Any]:
        return super().execute(rte)

    def as_dict(self) -> Dict[str, Any]:
        return super().as_dict()
