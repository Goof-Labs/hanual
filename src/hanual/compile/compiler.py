from __future__ import annotations

from typing import TYPE_CHECKING, Any

from bytecode import Bytecode, Instr, Label

from hanual.util import Reply, Request, Response
from hanual.lang.util.type_objects import GENCODE_RET, PREPARE_RET, REQUEST_TYPE

if TYPE_CHECKING:
    from hanual.lang.nodes.base_node import BaseNode


class Compiler:
    def __init__(self):
        self._instructions = []
        self._constants: list[Any] = []
        self._names: list[str] = []
        self._context: list = []

    def prepare_nodes(self, node: BaseNode):
        reply: Reply[list] | None = None
        pipe: PREPARE_RET = node.prepare()

        while True:
            try:
                req: Request = pipe.send(reply)

            except StopIteration:
                break

            reply: Reply[list] | None = self._satisfy_prepare_request(req)

    def _satisfy_prepare_request(self, request: Request) -> Reply[list] | None:
        req = iter(request.params)
        reply: list = []

        while True:
            req_type = next(req, None)

            if req_type is None:
                break

            if req_type == Request.ADD_CONSTANT:
                const = next(req)
                self._constants.append(const)
                reply.append(Reply.SUCCESS)

            elif req_type == Request.ADD_NAME:
                name = next(req)
                self._names.append(name)
                reply.append(Reply.SUCCESS)

            else:
                raise NotImplementedError(f"{req_type}")

        return Reply(reply)

    def compile_body(self, nodes: BaseNode):
        instructions: GENCODE_RET = nodes.gen_code()
        reply: Reply | None = None

        while True:
            try:
                val: Response[Instr] | Response[Label] | Request[REQUEST_TYPE] = (
                    instructions.send(reply)
                )

            except StopIteration:
                break

            if isinstance(val, Response):
                self._instructions.append(val.response)
                reply = Reply(True)  # accepted

            else:
                raise NotImplementedError(val)

    @property
    def instructions(self):
        return self._instructions

    def gen_code(self, block):
        self._instructions.append(Instr("RESUME", 0))
        self.prepare_nodes(block)
        self.compile_body(block)
        self._instructions.append(Instr("LOAD_CONST", 1))
        self._instructions.append(Instr("RETURN_CONST", 1))
        return Bytecode(self._instructions)
