from __future__ import annotations

from typing import Optional

from bytecode import Bytecode

from hanual.lang.nodes.block import CodeBlock
from hanual.lang.nodes.f_def import FunctionDefinition
from hanual.lang.nodes.parameters import Parameters
from hanual.lang.util.line_range import LineRange

from .compiler import Compiler


class HanualFunction:
    def __init__(
        self,
        name: str,
        line_range: LineRange,
        params: Optional[Parameters] = None,
        body: Optional[CodeBlock] = None,
    ) -> None:
        if not isinstance(name, str):
            raise TypeError(f"param name nust be str got {type(name).__name__}")

        if not isinstance(line_range, LineRange):
            raise TypeError(
                f"param line_range must be LineRange got {type(name).__name__}"
            )

        self._params: list = []
        self._name: str = name
        self._body: CodeBlock | None = None

        if body is not None:
            try:
                self.set_body(body)

            except TypeError as e:
                e.add_note("caused by parameter body in HanualFunction.__init__")
                raise

        if params is not None:
            try:
                self.take_params(params)

            except TypeError as e:
                e.add_note("caused by parameter params in HanualFunction.__init__")
                raise

    def set_body(self, body: CodeBlock):
        if not isinstance(body, CodeBlock):
            raise TypeError(f"body must be CodeBlock not {type(body).__name__}")

        self._body = body

    def take_params(self, params: Parameters):
        if not isinstance(params, Parameters):
            raise TypeError(f"body must be Parameters not {type(params).__name__}")

        self._params = [p.value for p in params.children]

    def compile(self) -> Bytecode:
        com = Compiler()
        return com.gen_code(self._body)

    @classmethod
    def from_func(cls, func: FunctionDefinition):
        if not isinstance(func, FunctionDefinition):
            raise TypeError(
                f"expected type FunctionDefinition, got {type(func).__name__}"
            )

        instance = cls(str(func.name.value), func.line_range)
        instance.take_params(func.arguments)
        instance.set_body(func.inner)
        return instance

    def __str__(self):
        return f"{type(self).__name__}({self._name})"

    def __repr__(self):
        return str(self)
