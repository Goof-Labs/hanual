from __future__ import annotations

from typing import Tuple, TypeVar, Any
from abc import ABC, abstractmethod


T = TypeVar("T")
N = TypeVar("N", bound="BaseNode")


class BaseNode(ABC):
    def __init__(self: BaseNode, *nodes: Tuple[T]) -> None:
        """
        This method should take n amount of arguments,
        these are either more nodes, or raw tokens.
        """
        raise NotImplementedError

    @abstractmethod
    def eval(self: BaseNode, context) -> Any:
        """
        This method takes the current context which is
        the program state. The
        """
        raise NotImplementedError

    @abstractmethod
    def compile(self) -> Any:
        """
        This method is called if the node needs to be
        compiled, this should return a stream of bytes,
        that corresponds to valid hanual bytecode.
        """
        raise NotImplementedError

    @abstractmethod
    def nice_print(self, __indent: int) -> str:
        """
        A nice way of printing the node | class instance
        """
        raise NotImplementedError

    @abstractmethod
    def __str__(self) -> str:
        """
        represent class as string.
        """
        raise NotImplementedError

    def __repr__(self) -> str:
        return str(self)
