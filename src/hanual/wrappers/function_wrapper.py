from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from types import FunctionType
    from hanual.lang.nodes.f_def import FunctionDefinition


class FunctionWrapper:
    def __init__(self, code: tuple[FunctionDefinition, FunctionType]) -> None:
        self._func: function | None = None
        self._fn_node, self._co_code = code

    def _create_func(self):
        def _f():
            ...

        _f.__code__ = self._co_code.__code__
        _f.__name__ = self._fn_node.name.value
        self._func = _f

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        if self._func is None:
            self._create_func()

        return self._func(*args, **kwds)

    def __str__(self) -> str:
        return f"[ FN {self._fn_node.name.value}\t{self._fn_node.parameters}\t~{hex(id(self)).capitalize()} ]"

    def __repr__(self) -> str:
        return str(self)

    @property
    def name(self) -> str:
        return self._fn_node.name.value
