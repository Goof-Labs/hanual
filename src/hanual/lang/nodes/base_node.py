from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, Generator
from hanual.exec.scope import Scope
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from hanual.compile.constants.constant import BaseConstant
    from hanual.exec.result import Result


T = TypeVar("T")
N = TypeVar("N", bound="BaseNode")


class BaseNode(ABC):
    @abstractmethod
    def __init__(self, *args, **kwargs) -> None:
        """
        This method should take n number of arguments,
        these are either more nodes, or raw tokens.
        """
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

    @property
    def line_no(self) -> int:
        return self._line_no

    @abstractmethod
    def execute(self, scope: Scope) -> Result:
        raise NotImplementedError

    @abstractmethod
    def get_names(self) -> list[str]:
        raise NotImplementedError

    @abstractmethod
    def get_constants(self) -> Generator[BaseConstant]:
        raise NotImplementedError
