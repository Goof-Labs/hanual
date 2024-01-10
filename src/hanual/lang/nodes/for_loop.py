from __future__ import annotations


from bytecode import Instr, Label
from typing import TYPE_CHECKING, Generator

from .base_node import BaseNode
from .implicit_binop import ImplicitBinOp
from .implicit_condition import ImplicitCondition
from hanual.util import Reply, Response, Request

if TYPE_CHECKING:
    from .assignment import AssignmentNode
    from .block import CodeBlock
    from .conditions import Condition
    from hanual.lang.lexer import Token


# for let i=0, < 10, +110
class ForLoop(BaseNode):
    __slots__ = "_while", "_init", "_action", "_body", "_lines", "_line_range"

    def __init__(
        self,
        condition: Condition | ImplicitCondition,
        init: AssignmentNode,
        action: ImplicitBinOp,
        body: CodeBlock,
    ) -> None:
        self._while: Condition | ImplicitCondition = condition
        self._init: AssignmentNode = init
        self._action: ImplicitBinOp = action
        self._body: CodeBlock = body

    @property
    def condition(self) -> Condition | ImplicitCondition:
        return self._while

    @property
    def init(self) -> AssignmentNode:
        return self._init

    @property
    def action(self) -> ImplicitBinOp:
        return self._action

    @property
    def body(self) -> CodeBlock:
        return self._body

    def gen_code(self) -> Generator[Response | Request, Reply, None]:
        loop_start = Label()
        loop_end = Label()

        yield from self._init.gen_code()

        var: Token = self._init.target

        yield Response(loop_start)
        yield from self._action.gen_code(infer=var)

        yield from self._body.gen_code()

        yield from self._while.gen_code(infer=var)
        yield Response(
            Instr("POP_JUMP_IF_FALSE", loop_end, location=self.get_location())
        )
        yield Response(Instr("JUMP_BACKWARD", loop_start, location=self.get_location()))
        yield Response(loop_end)

    def prepare(self) -> Generator[Request, Reply, None]:
        yield from self._while.prepare()
        yield from self._init.prepare()
        yield from self._action.prepare()
        yield from self._body.prepare()
