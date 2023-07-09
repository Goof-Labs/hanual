from __future__ import annotations

from typing import TypeVar, Union, NoReturn, TYPE_CHECKING

if TYPE_CHECKING:
    from hanual.lang.nodes import BaseNode

_N = TypeVar("_N", bound=BaseNode)


def verifiy(ast: list[list[str, _N]]) -> Union[None, NoReturn]:
    # it's fine
    if len(ast) == 1:
        return

    problem = []

    for line in ast:
        if not (line[0] in ("line", "lines")):
            problem.append(line[0])
