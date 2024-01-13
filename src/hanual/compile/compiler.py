from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

from bytecode import Bytecode, Instr, Label

from hanual.compile.context import Context
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
        reply: Optional[Reply] | Any = None

        while True:
            try:
                val: Response[Instr] | Response[Label] | Request[REQUEST_TYPE] = instructions.send(reply)

            except StopIteration:
                break

            if isinstance(val, Request):
                reply = self._satisfy_compile_request(val)

            elif isinstance(val, Response):
                self._instructions.append(val.response)
                reply = Reply(True)  # accepted

            else:
                raise NotImplementedError(val)

    def _satisfy_compile_request(self, request: Request[REQUEST_TYPE]) -> Reply[list | Any]:
        requests = iter(request.params)
        reply: list[Any] = []

        while True:
            req: Any | None = next(requests, None)

            if req is None:
                break

            if req == Request.GET_MEM_LOCATION:
                raise NotImplementedError

            elif req == Request.GET_CONTEXT:
                reply.append(self._context[-1])

            elif req == Request.CREATE_CONTEXT:
                # create a blank context
                ctx = Context(
                    deleter=self._delete_context,
                    adder=self._add_context,
                    getter=self._get_context,
                )

                self._context.append(ctx)

                if len(request.params) == 1:  # this is the only element
                    return Reply(ctx)

                else:
                    reply.append(ctx)

            else:
                raise Exception

        if len(reply) == 1:
            return Reply(reply[0])

        return Reply(reply)

    def _delete_context(self, ctx):
        self._context.remove(ctx)

    def _add_context(self, ctx):
        self._context.append(ctx)

    def _get_context(self):
        return self._context

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
