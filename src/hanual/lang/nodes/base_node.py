from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hanual.lang.util.line_range import LineRange


class BaseNode(ABC):
    __slots__ = (
        "_lines",
        "_line_range",
    )

    @abstractmethod
    def __init__(self, *args, **kwargs) -> None:
        """
        This method should take n number of arguments,
        these are either more nodes, or raw tokens.
        """
        self._lines = None
        self._line_range = None

        raise NotImplementedError

    @abstractmethod
    def compile(self, **kwargs):
        """
        This method is called if the node needs to be
        compiled, this should return a stream of bytes,
        that corresponds to valid hanual bytecode.
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
