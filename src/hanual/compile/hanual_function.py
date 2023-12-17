from __future__ import annotations

from types import CodeType
from typing import Optional

from hanual.lang.nodes.f_def import FunctionDefinition
from hanual.lang.nodes.parameters import Parameters
from hanual.lang.nodes.block import CodeBlock
from hanual.lang.util.line_range import LineRange

from .compiler import Compiler


class HanualFunction:
    def __init__(self,
                 name: str,
                 line_range: LineRange,
                 params: Optional[Parameters] = None,
                 body: Optional[CodeBlock] = None) -> None:
        if not isinstance(name, str):
            raise TypeError(f"param name nust be str got {type(name).__name__}")

        if not isinstance(line_range, LineRange):
            raise TypeError(f"param line_range must be LineRange got {type(name).__name__}")

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

    def _gen_code(self,
                  code_string: bytes,
                  filename: str,
                  first_line_no: int,
                  locals_: list[str],
                  stack_size: int,
                  names: tuple[str],
                  consts: tuple
                  ) -> CodeType:
        return CodeType(
            len(self._params),  # num args
            0,  # pos only params
            0,  # key word only params
            len(locals_),  # num locals
            stack_size,  # stack size
            3,  # flags
            code_string,  # code
            tuple(consts),  # constants
            tuple(names),  # global names, e.g functions like "print"
            tuple(locals_),  # variable names
            filename,
            self._name,  # func name
            self._name,  # qul name
            first_line_no,  # first line
            b"",
            b""
        )

    def compile(self) -> Compiler:
        com = Compiler()
        com.compile_code(self._body)
        return com

    @classmethod
    def from_func(cls, func: FunctionDefinition):
        if not isinstance(func, FunctionDefinition):
            raise TypeError(f"expected type FunctionDefinition, got {type(func).__name__}")

        instance = cls(func.name.value, func.line_range)
        instance.take_params(func.arguments)
        instance.set_body(func.inner)
        return instance

    def __str__(self):
        return f"{type(self).__name__}({self._name})"

    def __repr__(self):
        return str(self)
