from __future__ import annotations

from types import CodeType, FunctionType
from typing import Optional, Any

from hanual.compile.bytecode_instruction import ByteCodeInstruction
from hanual.compile.bytecode import assemble

from hanual.lang.nodes.f_def import FunctionDefinition
from hanual.lang.nodes.parameters import Parameters
from hanual.lang.nodes.block import CodeBlock
from hanual.lang.util.line_range import LineRange

from hanual.util import Reply, Response, Request


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

        self._name: str = name

        self._names: list[str] = []
        self._params: list[str] = []

        self._consts: list[Any] = []
        self._locals: list[str] = []

        self._file: str = ""

        self._arg_count = len(self._params)
        self._nm_locals = len(self._locals)

        self._line_start: int = line_range.start
        self._stack_size: int = -1

        self._body: CodeBlock | None = None
        self._code: CodeType | None = None

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
                  ) -> CodeType:
        return CodeType(
            len(self._params),  # num args
            0,  # pos only params
            0,  # key word only params
            len(self._locals),  # num locals
            self._stack_size,  # stack size
            3,  # flags
            code_string,  # code
            tuple(self._consts),  # constants
            tuple(self._names),  # global names, e.g functions like "print"
            tuple(self._locals),  # variable names
            filename,
            self._name,  # func name
            self._name,  # qul name
            first_line_no,  # first line
            b"",
            b""
        )

    def gen_code(self) -> list[ByteCodeInstruction]:
        assert self._body is not None

        gen = self._body.prepare()
        response: Response | None = None

        while True:
            try:
                reply: Reply | Request = gen.send(response)

            except StopIteration:
                break

            if response is None:
                response = Response(None)

            # satisfy request
            if isinstance(reply, Request):
                response.response = self._satisfy_request(reply)

            else:
                raise NotImplementedError

        gen = self._body.gen_code()
        response = None
        code: list[ByteCodeInstruction] = []

        while True:
            try:
                reply: Reply[ByteCodeInstruction] | Request = gen.send(response)

            except StopIteration:
                break

            if response is None:
                response = Response(None)

            if isinstance(reply, Request):
                response.response = self._satisfy_request(reply)

            elif isinstance(reply, Response):
                code.append(reply.response)

            else:
                raise Exception

        return self._finalize(code)

    def _satisfy_request(self, reply: Request) -> list[Any]:
        req = iter(reply.params)
        reply = []

        while True:
            req_type = next(req, None)

            if req_type is None:
                break

            if req_type == Request.ADD_CONSTANT:
                const = next(req)
                self._consts.append(const)
                reply.append(Reply.SUCCESS)

            elif req_type == Request.ADD_NAME:
                name = next(req)
                self._names.append(name)

            else:
                raise NotImplementedError(f"{req_type}")

        return reply

    def _finalize(self, code: list[ByteCodeInstruction]) -> list[ByteCodeInstruction]:
        instr = []

        for instruction in code:
            instr.append(instruction.gen())

        return instr

    def compile(self) -> FunctionType:
        return self.gen_code()

        func = FunctionType(
            code=self.gen_code(),
            globals={},
            name=self._name,
        )
        return func

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
