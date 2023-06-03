from __future__ import annotations

from typing import Union, Tuple, TypeVar, Dict, TYPE_CHECKING, Any
from hanual.lang.builtin_lexer import Token
from hanual.lang.errors import Error
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from hanual.runtime.runtime import RuntimeEnvironment
    from hanual.runtime.status import ExecStatus


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
    def compile(self) -> None:
        """
        This method is called if the node needs to be
        compiled, this should return a stream of bytes,
        that corresponds to valid hanual bytecode.
        """
        raise NotImplementedError

    @abstractmethod
    def execute(self, rte: RuntimeEnvironment) -> ExecStatus[Error, Any]:
        """
        A method that takes in the runtime and will
        evaluate the expression. e.g BioOp("+", 1, 2)
        should return 3.
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

    @staticmethod
    def get_repr(o: T) -> Union[Dict, Token]:
        # Just a convenience function that will call as_dict if it exists
        return o.as_dict() if hasattr(o, "as_dict") else o
