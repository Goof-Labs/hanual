from __future__ import annotations

from bytecode.instr import InstrLocation

from typing import Generator

from hanual.util import Reply, Response, Request
from hanual.lang.util.line_range import LineRange


class CompilableObject:
    def prepare(self) -> Generator[Request[object], Reply[object] | None, None]:
        raise NotImplementedError

    def gen_code(self) -> Generator[Response | Request, Reply | None, None]:
        raise NotImplementedError

    def get_location(self) -> InstrLocation:
        raise NotImplementedError

    @property
    def lines(self) -> str:
        raise NotImplementedError

    @lines.setter
    def lines(self, new: str) -> None:
        raise NotImplementedError

    @property
    def line_range(self) -> LineRange:
        raise NotImplementedError

    @line_range.setter
    def line_range(self, new: LineRange) -> None:
        raise NotImplementedError

    @property
    def is_token(self):
        raise NotImplementedError

    # This property has been implemented because tokens are also compilable objects
    @property
    def token_type(self):
        raise NotImplementedError

    @property
    def children(self):
        raise NotImplementedError
