from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict

from hanual.compile.instruction import RET
from hanual.compile.label import Label
from hanual.exec.hl_builtin.base_builtin import HlWrapperFunction
from hanual.exec.result import Result
from hanual.exec.scope import Scope
from hanual.lang.errors.trace_back import Frame

from .base_node import BaseNode

if TYPE_CHECKING:
    from hanual.compile.compile_manager import CompileManager
    from hanual.compile.constants.constant import BaseConstant
    from hanual.lang.lexer import Token

    from .block import CodeBlock
    from .parameters import Parameters


class FunctionDefinition(BaseNode):
    __slots__ = "_name", "_parameters", "_inner", "_lines", "_line_no",

    def __init__(
        self: FunctionDefinition,
        name: Token,
        params: Parameters,
        inner: CodeBlock,
        lines: str,
        line_no: int,
    ) -> None:
        self._name: Token = name
        self._parameters = params
        self._inner = inner

        self._line_no = line_no
        self._lines = lines

    @property
    def name(self) -> Token:
        return self._name

    @property
    def arguments(self) -> Parameters:
        return self._parameters

    @property
    def inner(self) -> CodeBlock:
        return self._inner

    def compile(self, cm: CompileManager):
        jp = Label(self._name.value)

        cm.add_function(self.name.value, jp)

        return [
            jp,  # jump to point
            *self._parameters.compile(cm),  # put arguments into namespace
            *self._inner.compile(cm),  # compile block
            RET(None),  # return
        ]

    def get_names(self) -> list[str]:
        return [
            self._name.value,
            *self._parameters.get_names(),
            *self._inner.get_names(),
        ]

    def get_constants(self) -> list[BaseConstant]:
        yield from self._inner.get_constants()

    def execute(self, scope: Scope) -> Result:
        func_wrapper = HlWrapperFunction(
            self._name.value, self._parameters, self.execute_body
        )
        scope.set(self._name.value, func_wrapper)
        return Result().success(None)

    def execute_body(self, scope: Scope, args: Dict[str, Any]) -> Result[Any, Any]:
        res = Result()

        f_scope = Scope(
            parent=scope,
            frame=Frame(name=str(self._name.value), line_num=self._name.line),
        )
        f_scope.extend(args)
        res.inherit_from(self._inner.execute(scope=f_scope))

        return res
