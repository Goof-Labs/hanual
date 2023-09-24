from __future__ import annotations

from typing import Callable, Union, Any, Generator, TYPE_CHECKING, List, LiteralString


if TYPE_CHECKING:
    from hanual.lang.nodes.parameters import Parameters
    from hanual.exec.scope import Scope, _H
    from hanual.exec.result import Result


class HlWrapperFunction:
    def __init__(self, name: str, params, func: Callable[[Scope, _H], Result]) -> None:
        from hanual.lang.nodes.parameters import Parameters

        # params
        if isinstance(params, Parameters):
            self.params = params

        else:
            self.params = Parameters(params, line_no=-1, lines="")

        # hanual functions
        self.func = func

        # name
        self.name = name

    @property
    def arguments(self) -> Parameters:
        return self.params

    def __call__(self, scope: Scope):
        return self.func(scope.parent, scope.locals())


def hl_builtin(f_args: LiteralString, name: LiteralString = ""):
    def decor(cls):
        cls.builtin_data = {
            "params": f_args.split(" "),
            "name": name,
        }
        return cls

    return decor


class BaseBuiltinLibrary:
    @staticmethod
    def create_function(method_name: str, method: Callable[[Scope, _H], Result]) -> HlWrapperFunction:
        assert hasattr(method, "builtin_data")
        args: List[str] = method.builtin_data["params"]
        name: str = method.builtin_data.get("name", None)

        return HlWrapperFunction(name=name or method_name, params=args, func=method)

    def get_builtins(self) -> Generator[HlWrapperFunction, None, None]:
        for method_name in dir(self):
            method: Union[Callable, Any] = getattr(self, method_name)

            # skip anything with an underscore or non-callable
            if not callable(method) or method_name[0] == "_":
                continue

            # ignore
            if not hasattr(method, "builtin_data"):
                continue

            yield self.create_function(method_name, method)
