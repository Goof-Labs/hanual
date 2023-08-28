from __future__ import annotations

from typing import List, Generator, Optional, LiteralString, Callable
from abc import ABC, abstractmethod
from .hook import GenericHook


def new_preprocessor(skip: Optional[List[LiteralString]]) -> Callable[[PreProcessorHook], PreProcessorHook]:
    def decor(cls: PreProcessorHook) -> PreProcessorHook:
        cls._skip = skip
        return cls

    return decor


class PreProcessorHook(GenericHook, ABC):
    @abstractmethod
    def scan_lines(self, lines: Generator[str, None, None]) -> Generator[str, None, None]:
        """
        This method is called once if `scan_line` has not been implemented. This
        generator yields what the code aught to be. This is much more pythonic compared
        to the `scan_line` implementation.
        """
        yield from lines
