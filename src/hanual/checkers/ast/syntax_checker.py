from __future__ import annotations

from typing import TypeVar, Union, NoReturn, TYPE_CHECKING
from hanual.lang.nodes import BaseNode


_N = TypeVar("_N", bound=BaseNode)


def verifiy(ast: list[list[str, _N]]) -> Union[None, NoReturn]:
    """
    We need to verifiy that the ast is a list with one element, a "lines" or
    "line". If it isn't then we have a problem.
    """
    if len(ast) == 1:
        # there is one big node
        return ast

    raise Exception("syntax error")
