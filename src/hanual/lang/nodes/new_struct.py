from __future__ import annotations

from typing import TYPE_CHECKING, Union

from hanual.compile.constants.constant import Constant
from hanual.exec.result import Result
from hanual.exec.scope import Scope
from hanual.lang.errors import ErrorType, Frame, HanualError, TraceBack

from .base_node import BaseNode

if TYPE_CHECKING:
    from hanual.exec.wrappers.hl_struct import HlStruct
    from hanual.lang.lexer import Token

    from .arguments import Arguments
    from .f_call import FunctionCall


class NewStruct(BaseNode):
    __slots__ = "_args", "_name", "_line_no", "_lines"

    def __init__(self: BaseNode, call: FunctionCall, lines: str, line_no: int) -> None:
        self._args: Arguments = call.args
        self._name: Token = call.name

        self._line_no = line_no
        self._lines = lines

    @property
    def name(self) -> Token:
        return self._name

    @property
    def args(self) -> Arguments:
        return self._args

    def compile(self) -> None:
        raise NotImplementedError

    def get_constants(self) -> list[Constant]:
        yield from self._args.get_constants()

    def get_names(self) -> list[str]:
        return [self._name, *self._args.get_names()]

    def execute(self, scope: Scope) -> Result:
        res = Result()

        struct: Union[HlStruct, None] = scope.get(self._name.value, None)

        if struct is None:
            return res.fail(
                HanualError(
                    pos=(
                        self._name.line,
                        self._name.colm,
                        self._name.colm + len(self._name.value),
                    ),
                    line=self._name.line_val,
                    name=ErrorType.unresolved_name,
                    reason=f"Couldn't resolve reference to {self._name.value!r}",
                    tb=TraceBack().add_frame(Frame("new struct")),
                    tip="Did you make a typo?",
                )
            )

        return res.success(struct.make_instance(name=struct.name, fields=struct.fields))
