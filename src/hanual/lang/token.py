from __future__ import annotations

from bytecode.instr import Instr, InstrLocation

from hanual.lang.util.compileable_object import CompilableObject
from hanual.lang.util.line_range import LineRange
from hanual.lang.util.type_objects import GENCODE_RET, PREPARE_RET
from hanual.util.protocalls import Request, Response


class Token(CompilableObject):
    def __init__(self, token_type: str, value: str | int | float, line_range: LineRange, colm: int, lines: str) -> None:
        self._value: str | int | float = value
        self._line_range: LineRange = line_range
        self._token_type: str = token_type
        self._colm: int = colm
        self._lines: str = lines

    def prepare(self) -> PREPARE_RET:
        if self._token_type == "ID":
            yield Request(Request.ADD_NAME, str(self._value))

        elif self._token_type == "STR":
            yield Request(Request.ADD_CONSTANT, str(self._value))

        elif self._token_type == "NUM":
            yield Request(Request.ADD_CONSTANT, int(self._value))

        else:
            raise NotImplementedError

    def gen_code(self) -> GENCODE_RET:
        if self._token_type == "ID":
            reply = yield Request(Request.GET_CONTEXT)
            assert reply is not None

            store = reply.response.get("store")

            if store is True:
                yield Response[Instr](
                    Instr("STORE_FAST", str(self._value), location=self.get_location())
                )

            elif store is False:
                yield Response[Instr](Instr("LOAD_FAST", str(self._value)))

            else:
                raise Exception(
                    f"{type(self).__name__} {self._token_type} {self.value} {store}"
                )

        elif self._token_type == "STR":
            yield Response[Instr](Instr("LOAD_CONST", str(self._value)))

        elif self._token_type == "NUM":
            yield Response[Instr](Instr("LOAD_CONST", int(self._value)))

        else:
            raise NotImplementedError

    def get_location(self) -> InstrLocation:
        return InstrLocation(
            lineno=int(self._line_range.start),
            end_lineno=int(self._line_range.end),
            col_offset=None,
            end_col_offset=None,
        )

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
