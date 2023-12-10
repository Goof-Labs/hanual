from __future__ import annotations

from typing import Generator
from abc import ABC, abstractmethod

from hanual.lang.util.line_range import LineRange

from hanual.util import Reply, Response, Request


class BaseNode(ABC):
    __slots__ = (
        "_lines",
        "_line_range",
    )

    @abstractmethod
    def __init__(self, *args, **kwargs) -> None:
        """
        """
        self._lines = ""
        self._line_range = LineRange(-1, -1)

        raise NotImplementedError

    @abstractmethod
    def prepare(self) -> Generator[Response | Request, Reply, None]:
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
    def gen_code(self):
        """Generates the code for the compiler to omit.

        """
        raise NotImplementedError

    @property
    def lines(self) -> str:
        return self._lines

    @lines.setter
    def lines(self, new: str) -> None:
        assert isinstance(new, str), "new value for lines must be a str"
        self._lines = new

    @property
    def line_range(self) -> LineRange:
        return self._line_range

    @line_range.setter
    def line_range(self, new: LineRange) -> None:
        assert isinstance(new, LineRange), "new value must be a line_range"
        self._line_range = new
