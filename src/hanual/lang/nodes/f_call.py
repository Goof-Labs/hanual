from __future__ import annotations


from typing import Any, Dict, TYPE_CHECKING, Union

from hanual.runtime.runtime import RuntimeEnvironment
from hanual.runtime.status import ExecStatus
from hanual.lang.errors import Error
from .dot_chain import DotChain
from .base_node import BaseNode

if TYPE_CHECKING:
    from hanual.runtime import RuntimeEnvironment, ExecStatus
    from hanual.lang.errors import Error
    from hanual.lang.lexer import Token
    from .arguments import Arguments


class FunctionCall(BaseNode):
    def __init__(self: BaseNode, name: Token, arguments: Arguments) -> None:
        self._name: Union[Token, DotChain] = name
        self._args: Arguments = arguments

    def compile(self, inter_rep) -> None:
        fn_name = self._name.value
        fn_args = self._args

        fn_args.compile()

        id_ = inter_rep.get_mem_ref(fn_name)
        inter_rep.move(Register.FP, id_)

        inter_rep.call_the_funky_function()

        inter_rep.free_mem_ref(id_)

    def execute(self, rte: RuntimeEnvironment) -> ExecStatus[Error, Any]:
        return super().execute(rte)

    @property
    def name(self) -> Token:
        return self._name

    @property
    def args(self) -> Arguments:
        return self._args

    def as_dict(self) -> Dict[str, Any]:
        return {"args": self._args.as_dict(), "name": self._name}
