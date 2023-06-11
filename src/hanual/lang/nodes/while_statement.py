from __future__ import annotations

from hanual.compile.state_fragment import Fragment, MOV, JNZ
from hanual.lang.nodes.base_node import BaseNode
from typing import Any, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from hanual.runtime.runtime import RuntimeEnvironment
    from hanual.runtime.status import ExecStatus, Error
    from hanual.lang.nodes.conditions import Condition
    from hanual.lang.nodes.block import CodeBlock


class WhileStatement(BaseNode):
    def __init__(self: BaseNode, condition: Condition, body: CodeBlock) -> None:
        self._while: Condition = condition
        self._body: CodeBlock = body

    @property
    def condition(self) -> Condition:
        return self._while

    @property
    def body(self) -> CodeBlock:
        return self._body

    def compile(self) -> None:
        raise NotImplementedError

    def execute(self, rte: RuntimeEnvironment) -> ExecStatus[Error, Any]:
        return super().execute(rte)

    def as_dict(self) -> Dict[str, Any]:
        return {
            "condition": self._while.as_dict()
            if hasattr(self._while, "as_dict")
            else self._while,
            "inner": self._body.as_dict()
            if hasattr(self._body, "as_dict")
            else self._body,
        }
