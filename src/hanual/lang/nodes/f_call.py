from __future__ import annotations

from typing import TYPE_CHECKING

from bytecode import Instr

from hanual.lang.nodes.base_node import BaseNode
from hanual.lang.nodes.dot_chain import DotChain
from hanual.lang.token import Token
from hanual.lang.util.type_objects import GENCODE_RET, PREPARE_RET
from hanual.lang.util.node_utils import Intent
from hanual.util.equal_list import ItemEqualList
from hanual.util import Response

if TYPE_CHECKING:
    from .arguments import Arguments


class FunctionCall[N: (Token, DotChain)](BaseNode):
    __slots__ = (
        "_name",
        "_args",
        "_lines",
        "_line_range",
    )

    def __init__(
        self,
        name: N,
        arguments: Arguments,
    ) -> None:
        self._name: N = name
        self._args: Arguments = arguments

    @property
    def name(self) -> N:
        return self._name

    @property
    def args(self) -> Arguments:
        return self._args

    def gen_code(self, intents: ItemEqualList[Intent], **options) -> GENCODE_RET:
        yield Response(Instr("PUSH_NULL", location=self.get_location()))

        if isinstance(self._name, DotChain):
            yield from self._name.gen_code()

        else:
            yield Response(Instr("LOAD_NAME", str(self._name.value), location=self._name.get_location()))

        yield from self._args.gen_code()

        yield Response(Instr("CALL", len(self._args), location=self.get_location()))

        if self.CAPTURE_RESULT in intents:
            pass

        elif self.IGNORE_RESULT in intents:
            yield Response(Instr("POP_TOP", location=self.get_location()))

        else:
            raise Exception(f"Intent wasn't provided, either CAPTURE_RESULT or IGNORE_RESULT ( {intents} )")

    def prepare(self) -> PREPARE_RET:
        yield from self._name.prepare()
        yield from self._args.prepare()
