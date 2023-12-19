from __future__ import annotations

from typing import Protocol, Generator

from hanual.util.protocalls import Reply, Response, Request
from hanual.lang.util.line_range import LineRange


class CompilableObject(Protocol):
    def prepare(self) -> Generator[Response | Request, Reply, None]:
        raise Exception

    def gen_code(self) -> Generator[Response | Request, Reply, None]:
        raise Exception

    @property
    def lines(self) -> str:
        raise Exception

    @lines.setter
    def lines(self, new: str) -> None:
        raise Exception

    @property
    def line_range(self) -> LineRange:
        raise Exception

    @line_range.setter
    def line_range(self, new: LineRange) -> None:
        raise Exception

    @property
    def is_token(self) -> bool:
        raise Exception
