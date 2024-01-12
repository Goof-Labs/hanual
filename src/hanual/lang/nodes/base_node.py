from __future__ import annotations

from abc import abstractmethod

from bytecode.instr import InstrLocation

from hanual.lang.nodes.base_node_meta import _BaseNodeMeta
from hanual.lang.util.line_range import LineRange
from hanual.lang.util.type_objects import GENCODE_RET, PREPARE_RET


class BaseNode(metaclass=_BaseNodeMeta):
    __slots__ = (
        "_lines",
        "_line_range",
    )

    @abstractmethod
    def __init__(self, *args, **kwargs) -> None:
        self._line_range: LineRange | None = None
        self._lines: str | None = None

        raise NotImplementedError

    @abstractmethod
    def prepare(self) -> PREPARE_RET:
        """Used to collect information from the node.

        > Provides all necessary info to the compiler such as variable names and
        > constants.

        @return^Generator[Response | Request, Reply, None]>A gen that provides information to the compiler.
        | This gen takes in a compiler Reply and yields either a Request or a reply.
        | The gen should yield data or a request to the compiler and take a reply
        | in this sense, this gen is bidirectional.
        """
        raise NotImplementedError

    @abstractmethod
    def gen_code(self) -> GENCODE_RET:
        """Generates the code for the compiler to omit."""
        raise NotImplementedError

    def get_location(self) -> InstrLocation:
        if self._line_range is None:
            raise Exception("self._line_range is None (was never set)")

        if self._line_range.start < 1 or self._line_range.end < 1:
            raise Exception(f"LineRange has a range of -1 {self._line_range}")

        # TODO add column offsets and change second `self._line_range.start` to the `self._line_range.end`
        return InstrLocation(
            lineno=int(self._line_range.start),
            end_lineno=int(self._line_range.start),
            col_offset=None,
            end_col_offset=None,
        )

    @property
    def lines(self) -> str:
        if self._lines is None:
            raise Exception("self._lines is None (was never set)")

        return self._lines

    @lines.setter
    def lines(self, new: str) -> None:
        assert isinstance(new, str), "new value for lines must be a str"
        self._lines = new

    @property
    def line_range(self) -> LineRange:
        if self._line_range is None:
            raise Exception("self._line_range is none (was never set)")

        return self._line_range

    @line_range.setter
    def line_range(self, new: LineRange) -> None:
        assert isinstance(new, LineRange), "new value must be a line_range"
        self._line_range = new

    @property
    def is_token(self):
        return True
