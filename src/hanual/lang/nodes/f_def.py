from __future__ import annotations


from bytecode import Instr, Label, Bytecode

from typing import TYPE_CHECKING
from types import FunctionType

from hanual.lang.nodes.base_node import BaseNode
from hanual.lang.util.node_utils import Intent
from hanual.util import Response
from hanual.util import Reply, Request, Response
from hanual.lang.util.type_objects import GENCODE_RET, PREPARE_RET, REQUEST_TYPE


if TYPE_CHECKING:
    from hanual.lang.lexer import Token
    from hanual.lang.util.node_utils import Intent

    from .block import CodeBlock
    from .parameters import Parameters


class FunctionDefinition(BaseNode):
    __slots__ = (
        "_name",
        "_parameters",
        "_inner",
        "_lines",
        "_line_range",
    )

    def __init__(
        self,
        name: Token,
        params: Parameters,
        inner: CodeBlock,
    ) -> None:
        self._name: Token = name
        self._parameters = params
        self._inner = inner

    @property
    def name(self) -> Token:
        return self._name

    @property
    def parameters(self) -> Parameters:
        return self._parameters

    @property
    def inner(self) -> CodeBlock:
        return self._inner

    def gen_code(self, *intents: Intent, **options) -> GENCODE_RET:
        yield Response(Instr("RESUME", 0))

        yield from self.inner.gen_code(*intents, **options)

        yield Response(Instr("LOAD_CONST", 0))
        yield Response(Instr("RETURN_CONST", 1))

    def gen_py_code(self):
        pipe: GENCODE_RET = self.gen_code()
        reply: Reply | None = None
        instructions = []

        while True:
            try:
                val: Response[Instr] | Response[Label] | Request[REQUEST_TYPE] = (
                    pipe.send(reply)
                )

            except StopIteration:
                break

            if isinstance(val, Response):
                instructions.append(val.response)
                reply = Reply(True)  # accepted

            else:
                raise NotImplementedError(val)
        
        co_code = Bytecode(instructions).to_code()

        return self, FunctionType(co_code, globals={}, name=self.name.value)

    def prepare(self) -> PREPARE_RET:
        raise NotImplementedError
