from __future__ import annotations


def takes_param(cls, num_params=1):
    assert hasattr(cls, "_num_params"), f"{type(cls).__name__!r} must have a '_num_params' attr"
    cls._num_params = num_params
    return cls


def no_param[C: BaseIrInstruction](cls: C) -> C:
    assert hasattr(cls, "_num_params"), f"{type(cls).__name__!r} must have a '_num_params' attr"
    cls._num_params = 0
    return cls


class BaseIrInstruction:
    __slots__ = "_params", "_reg", "_num_params"

    def __init__(self, *params):
        if self._num_params != len(params):
            raise ValueError(f"params should be of length {self._num_params} got {len(params)}")

        self._params = params

    def __class_getitem__(cls, register):
        cls._reg = register
        return cls
