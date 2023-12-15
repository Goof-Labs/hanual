from __future__ import annotations

from typing import TYPE_CHECKING

from hanual.util import Reply, Request

if TYPE_CHECKING:
    from hanual.compile.bytecode_instruction import ByteCodeInstruction
    from hanual.lang.nodes.base_node import BaseNode


class Compiler:
    def __init__(self):
        self._instructions: list[ByteCodeInstruction] = []
        self._constants: set[int | str] = set()
        self._names: set[str] = set()

    def compile_code(self, node: BaseNode):
        self.prepare_nodes(node)
        self.compile_body(node)

    def prepare_nodes(self, node: BaseNode):
        reply: Reply | None = None
        pipe = node.prepare()

        while True:
            try:
                req: Request = pipe.send(reply)

            except StopIteration:
                break

            reply = Reply(self._satisfy_request(req))

    def _satisfy_request(self, request: Request) -> list:
        req = iter(request.params)
        reply = []

        while True:
            req_type = next(req, None)

            if req_type is None:
                break

            if req_type == Request.ADD_CONSTANT:
                const = next(req)
                self._constants.add(const)
                reply.append(Reply.SUCCESS)

            elif req_type == Request.ADD_NAME:
                name = next(req)
                self._names.add(name)
                reply.append(Reply.SUCCESS)

            else:
                raise NotImplementedError(f"{req_type}")

        return reply

    def compile_body(self, nodes: BaseNode):
        ...
