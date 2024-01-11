from __future__ import annotations


from bytecode import Instr

from abc import ABC
from typing import TYPE_CHECKING, Generator, Optional

from hanual.lang.nodes.base_node import BaseNode
from hanual.lang.nodes.block import CodeBlock
from hanual.lang.lexer import Token
from hanual.util.protocalls import Request, Reply, Response, REQUEST_TYPE

if TYPE_CHECKING:
    from hanual.lang.nodes.range_node import RangeNode
    from hanual.lang.nodes.parameters import Parameters
    from hanual.lang.nodes.binop import BinOpNode

    from hanual.lang.util.line_range import LineRange


class AnonymousFunction(BaseNode, ABC):
    __slots__ = ("_args", "_inner", "fn_name", "_lines", "_line_no", "_return")

    def __init__(
        self: BaseNode,
        args: Parameters,
        inner: CodeBlock,
        ret: Token | BinOpNode | RangeNode,
        lines: str,
        line_range: LineRange,
    ) -> None:
        self._inner = inner
        self._args = args
        self._return = ret

        self._line_range = line_range
        self._lines = lines

    def gen_code(self) -> Generator[Response[Instr] | Request[REQUEST_TYPE], Optional[Reply], None]:
        raise NotImplementedError

    def prepare(self) -> Generator[Request[object], Reply[object] | None, None]:
        raise NotImplementedError
