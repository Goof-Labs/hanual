from __future__ import annotations

from typing import Callable, Union, Any, Generator, TYPE_CHECKING, List, LiteralString
from hanual.lang.nodes import Arguments


if TYPE_CHECKING:
    from hanual.exec.scope import Scope, _H
    from hanual.exec.result import Result


class HlWrapperFunction:
    def __init__(self, name: str, arguments: List[LiteralString], func: Callable[[Scope, _H], Result]) -> None:
        # hanual arguments
        self.args = Arguments(arguments)
        self.args.function_def = True

        # hanual functions
        self.func = func

        # name
        self.name = name

    @property
    def arguments(self) -> Arguments:
        return self.args

    def __call__(self, scope: Scope):
        return self.func(scope.parent, scope.locals())


def hl_builtin(f_args: LiteralString, name: LiteralString = ""):
    def decor(cls):
        cls.builtin_data = {
            "args": f_args.split(" "),
            "name": name,
        }
        return cls

    return decor


class BaseBuiltinLibrary:
    @staticmethod
    def create_builtin(method_name: str, method: Callable[[Scope, _H], Result]) -> HlWrapperFunction:
        assert hasattr(method, "builtin_data")
        args: List[str] = method.builtin_data["args"]
        name: str = method.builtin_data.get("name", None)

        return HlWrapperFunction(name=name or method_name, arguments=args, func=method)

    def get_builtins(self) -> Generator[HlWrapperFunction, None, None]:
        for method_name in dir(self):
            method: Union[Callable, Any] = getattr(self, method_name)

            # skip anything with an underscore or non-callable
            if not callable(method) or method_name[0] == "_":
                continue

            # ignore
            if not hasattr(method, "builtin_data"):
                continue

            yield self.create_builtin(method_name, method)
