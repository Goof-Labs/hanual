from __future__ import annotations

from typing import overload, TYPE_CHECKING, Generator, NoReturn, Union, Literal
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from hanual.lang.util.line_range import LineRange

    from ..instruction_parameter import BaseInstructionParameter


def takes_param(num_params=1):
    def inner[C: BaseInstruction](cls: C) -> C:
        assert hasattr(cls, "_num_params"), f"{type(cls).__name__!r} must have a '_num_params' attr"
        cls._num_params = num_params
        return cls

    return inner


def no_param[C: BaseInstruction](cls: C) -> C:
    assert hasattr(cls, "_num_params"), f"{type(cls).__name__!r} must have a '_num_params' attr"
    cls._num_params = 0
    return cls


class BaseInstruction[P: BaseInstructionParameter](ABC):
    __slots__ = "_num_params", "_params", "_lines", "_line_range"

    @overload
    def __init__(self, *, lines: str, line_range: LineRange) -> None:
        ...

    @overload
    def __init__(self, param: P, *, lines: str, line_range: LineRange) -> None:
        ...

    def __init__(self, *args, **kwargs):
        self._line_range: LineRange = kwargs.get("line_range", None)
        if self._line_range is None:
            raise TypeError(f"`line_range` was not passed")

        self._lines: str = kwargs.get("lines", None)
        if self._lines is None:
            raise TypeError(f"`lines` was not passed")

        self._params: list[P] = []

        if self._num_params > 0:
            # Argument lengths
            if len(args) > self._num_params:
                raise ValueError(f"Too manny arguments passed ({len(args)}) must be {self._num_params}")

            if len(args) < self._num_params:
                raise ValueError(f"Too few arguments passed ({len(args)}) must be {self._num_params}")

            for param in args:
                # argument type
                if not issubclass(type(param), BaseInstructionParameter):
                    raise Exception(f"{type(param).__name__!r} should inherit from 'BaseInstructionParameter'")

                self._params.append(param)

        else:
            assert self._num_params == 0

            if len(args) != 0:
                raise ValueError(f"{type(self).__name__!r} does not take any parameters, {len(args)} where given")

        self.validate()

    @property
    def params(self) -> list[P]:
        return self._params

    @abstractmethod
    def compile(self) -> Generator[bytes, None, None]:
        raise NotImplementedError

    @abstractmethod
    def validate(self) -> Union[Literal[None], NoReturn]:
        raise NotImplementedError

    def __str__(self) -> str:
        if self._num_params > 0:
            return f"[{type(self).__name__!r}::{self._params!s}]"

        else:
            return f"[{type(self).__name__!r}]"

    def __repr__(self) -> str:
        return str(self)
