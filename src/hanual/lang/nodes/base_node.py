from __future__ import annotations

from hanual.compile import GlobalState
from typing import Tuple, TypeVar, Any
from abc import ABC, abstractmethod


T = TypeVar("T")
N = TypeVar("N", bound="BaseNode")


class BaseNode(ABC):
    @abstractmethod
    def __init__(self: BaseNode, *nodes: Tuple[T]) -> None:
        """
        This method should take n amount of arguments,
        these are either more nodes, or raw tokens.
        """
        raise NotImplementedError

    @abstractmethod
    def compile(self, global_state: GlobalState) -> Any:
        """
        This method is called if the node needs to be
        compiled, this should return a stream of bytes,
        that corresponds to valid hanual bytecode.
        """
        raise NotImplementedError

    @abstractmethod
    def __str__(self, *args, **kwargs) -> str:
        """
        represent class as string.
        """
        raise NotImplementedError

    def __repr__(self) -> str:
        return str(self)
