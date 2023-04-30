from __future__ import annotations

from typing import Tuple, TypeVar, Any, Dict, TYPE_CHECKING
from abc import ABC, abstractmethod


if TYPE_CHECKING:
    from hanual.compile import Assembler


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
    def compile(self, global_state: Assembler) -> Any:
        """
        This method is called if the node needs to be
        compiled, this should return a stream of bytes,
        that corresponds to valid hanual bytecode.
        """
        raise NotImplementedError

    @abstractmethod
    def as_dict(self) -> Dict[str, Any]:
        """
        Instead of having very awkward __str__ methods that
        are impossible to refactor, at least mine where. We
        have an `as_dict` method that will recursively return
        the ast as a dict. This lets us pprint it more
        efficiently.
        """
        raise NotImplementedError
