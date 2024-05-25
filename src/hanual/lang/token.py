from __future__ import annotations

from bytecode.instr import Instr, InstrLocation

from hanual.lang.util.compileable_object import CompilableObject
from hanual.lang.util.line_range import LineRange
from hanual.lang.util.node_utils import Intent
from hanual.lang.util.type_objects import GENCODE_RET, PREPARE_RET
from hanual.util.equal_list import ItemEqualList
from hanual.util.protocalls import Request, Response


class Token(CompilableObject):
    """Representation of a token; used for lexical analysis and parsing."""
    GET_VARIABLE = Intent("GET_VARIABLE")
    SET_VARIABLE = Intent("SET_VARIABLE")

    def __init__(
        self,
        token_type: str,
        value: str | int | float,
        line_range: LineRange,
        colm: int,
        lines: str,
    ) -> None:
        """Initializer for a new token.

        Args:
            token_type (str): The type of the token.
            value (str | int | float): The value of the token
            line_range (LineRange): The position of the token as line numbers only.
            colm (int): The comumn of the token in the source code.
            lines (str): The lines that contain the token.
        """
        self._value: str | int | float = value
        self._line_range: LineRange = line_range
        self._token_type: str = token_type
        self._colm: int = colm
        self._lines: str = lines

    def prepare(self) -> PREPARE_RET:
        """Prepares the token before it is compiled.

        A token is internally a CompilableObject so it can be compiled. (This is done to reduce code repition.)
        This method needs to be overwritten to allow for this.

        Raises:
            NotImplementedError: If the token is not one of the specified types then the logic has not been implemented yet.

        Yields:
            Iterator[PREPARE_RET]: _description_
        """
        if self._token_type == "ID":
            yield Request(Request.ADD_NAME, str(self._value))

        elif self._token_type == "STR":
            yield Request(Request.ADD_CONSTANT, str(self._value))

        elif self._token_type == "NUM":
            yield Request(Request.ADD_CONSTANT, int(self._value))

        else:
            raise NotImplementedError

    def gen_code(self, *intents, **options) -> GENCODE_RET:
        intents = ItemEqualList(intents)

        if self._token_type == "ID":
            if self.GET_VARIABLE in intents:
                yield Response[Instr](
                    Instr("LOAD_FAST", str(self._value), location=self.get_location())
                )

            elif self.SET_VARIABLE in intents:
                yield Response[Instr](
                    Instr("STORE_FAST", str(self._value), location=self.get_location())
                )

            else:
                raise Exception(
                    f"Neither GET_VARIABLE or SET_VARIABLE was passed as an intent, ( {intents} )"
                )

        elif self._token_type == "STR":
            yield Response[Instr](Instr("LOAD_CONST", str(self._value)))

        elif self._token_type == "NUM":
            yield Response[Instr](Instr("LOAD_CONST", int(self._value)))

        else:
            raise NotImplementedError(self._token_type)

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
    def line_range(self) -> LineRange:
        return self._line_range

    @line_range.setter
    def line_range(self, new: LineRange) -> None:
        assert isinstance(new, LineRange), "new value must be a line_range"
        self._line_range = new

    @property
    def lines(self) -> str:
        return self._lines

    @lines.setter
    def lines(self, new: str) -> None:
        assert isinstance(new, str), "new value for lines must be a str"
        self._lines = new
