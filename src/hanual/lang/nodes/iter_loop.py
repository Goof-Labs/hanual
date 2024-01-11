from __future__ import annotations

from bytecode import Instr

from typing import TYPE_CHECKING, Generator, Optional

from hanual.lang.nodes.base_node import BaseNode
from hanual.util import Reply, Request, Response, REQUEST_TYPE


if TYPE_CHECKING:
    from hanual.lang.util.line_range import LineRange
    from hanual.lang.lexer import Token

    from .f_call import FunctionCall


class IterLoop[I: (Token, FunctionCall)](BaseNode):
    def __init__(
        self, name: Token, iterator: I, lines: str, line_range: LineRange
    ) -> None:
        self._iterator: I = iterator
        self._name: Token = name

        self._lines = lines
        self._line_range = line_range

    def gen_code(self) -> Generator[Response[Instr] | Request[REQUEST_TYPE], Optional[Reply], None]:
        raise NotImplementedError

    def prepare(self) -> Generator[Request[object], Reply[object] | None, None]:
        raise NotImplementedError
