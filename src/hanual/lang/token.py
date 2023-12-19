from __future__ import annotations

from bytecode import Instr
from typing import Generator

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

    def prepare(self) -> Generator[Response | Request, Reply, None]:
        if self._token_type == "ID":
            yield Request(Request.ADD_NAME, self._value)

        elif self._token_type == "STR":
            yield Request(Request.ADD_CONSTANT, self._value)

        elif self._token_type == "NUM":
            yield Request(Request.ADD_CONSTANT, self._value)

        else:
            raise NotImplementedError

    def gen_code(self, **kwargs) -> Generator[Response | Request, Reply, None]:
        if self._token_type == "ID":
            store: bool | None = kwargs.get("store", None)

            if store:
                yield Response(Instr("STORE_FAST", self._value))

            elif store is False:
                yield Response(Instr("LOAD_FAST", self._value))

            else:
                raise Exception(f"{type(self).__name__} {self._token_type} {self.value}")

        elif self._token_type == "STR":
            yield Response(Instr("LOAD_CONST", self._value))

        elif self._token_type == "NUM":
            yield Response(Instr("LOAD_CONST", self._value))

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