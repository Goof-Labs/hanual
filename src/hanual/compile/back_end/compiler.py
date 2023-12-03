from __future__ import annotations

from ..instruction.base_instr import BaseInstruction
from hanual.lang.nodes.block import CodeBlock

from .response import Response
from .request import Request
from .reply import Reply

from typing import Self


class Compiler:
    def __init__(self):
        self._instructions = []
        self._constants = set()

    def compile_ast(self, ast: CodeBlock):
        result = ast.compile()
        response = None

        while True:
            try:
                reply: Reply | Request = result.send(response)

            except StopIteration:
                break

            # change after first iteration
            if not response:
                response = Response(None)

            # satisfy any requests
            if isinstance(reply, Request):
                response.response = self.satisfy_request(reply)

            elif isinstance(reply, Reply):  # code!
                assert issubclass(type(reply.response), BaseInstruction)
                self._instructions.append(response)

    def satisfy_request(self, requests: Request):
        req = (i for i in requests.params)
        reply = []

        while True:
            req_type = next(req, None)

            # nothing else to parse
            if req_type is None:
                break

            if req_type == Request.MAKE_CONSTANT:
                const = next(req)
                reply.append(self._create_const(const))

            elif req_type == Request.MAKE_REGISTER:
                reply.append(self._create_register())

            else:
                raise NotImplementedError(req_type)

        return reply

    def _create_const(self, const):
        ...

    def _create_register(self):
        ...

    @classmethod
    def from_ast(cls, ast) -> Self:
        instance: Compiler = cls()
        instance.compile_ast(ast)
        return instance
