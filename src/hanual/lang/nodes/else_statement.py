from __future__ import annotations

from bytecode import Instr

from typing import TYPE_CHECKING, Generator, Optional

from hanual.lang.nodes.base_node import BaseNode
from hanual.util import Reply, Request, Response, REQUEST_TYPE

if TYPE_CHECKING:
    from .block import CodeBlock


class ElseStatement(BaseNode):
    __slots__ = (
        "_body",
        "_lines",
        "_line_range",
    )

    def __init__(self, body: CodeBlock) -> None:
        self._body = body

    @property
    def body(self) -> CodeBlock:
        return self._body

    def gen_code(self) -> Generator[Response[Instr] | Request[REQUEST_TYPE], Optional[Reply], None]:
        raise NotImplementedError

    def prepare(self) -> Generator[Request[object], Reply[object] | None, None]:
        raise NotImplementedError
