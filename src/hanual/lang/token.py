from __future__ import annotations

from hanual.util.protocalls import Reply, Response, Request
from hanual.lang.util.line_range import LineRange


class Token[T]:
    def __init__(self,
                 token_type: str,
                 value: T,
                 line_range: LineRange,
                 colm: int,
                 lines: str) -> None:
        self._token_type: str = token_type
        self._value: T = value
        self._line_range: LineRange = line_range
        self._colm: int = colm
        self._lines: str = lines

    def prepare(self):
        if self._token_type == "ID":
            yield Request(Request.ADD_NAME, self._value)

        elif self._token_type == "STR":
            yield Request(Request.ADD_CONSTANT, self._value)

        elif self._token_type == "NUM":
            yield Request(Request.ADD_CONSTANT, self._value)

        else:
            raise NotImplementedError

    @property
    def token_type(self):
        return self._token_type

    @property
    def value(self):
        return self._value

    @property
    def line_range(self):
        return self._line_range

    @property
    def colm(self):
        return self._colm

    @property
    def lines(self):
        return self._lines
