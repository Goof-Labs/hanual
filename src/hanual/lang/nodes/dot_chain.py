from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING, Any, List, Union

from hanual.exec.result import Result
from hanual.lang.errors import Frame
from hanual.lang.lexer import Token

from .base_node import BaseNode

if TYPE_CHECKING:
    from typing_extensions import Self

    from hanual.exec.scope import Scope


class DotChain(BaseNode, ABC):
    __slots__ = ("_chain",)

    def __init__(self: BaseNode) -> None:
        self._chain: List[Token] = []

    def add_name(self, name: Union[Token, DotChain]) -> Self:
        if isinstance(name, Token):
            self._chain.insert(0, name)

        elif isinstance(name, DotChain):
            self._chain = [*self._chain, *name.chain]

        else:
            raise Exception

        return self

    @property
    def chain(self) -> List[Token]:
        return self._chain

    def compile(self) -> None:
        raise NotImplementedError

    def execute(self, scope: Scope, set_attr: bool = None) -> Result:
        res = Result()

        prev: Any = None

        last_idx = len(self._chain) - 1

        for i, link in enumerate(self._chain):
            # don't have a starting node, or this is the first one
            if (last_idx == i) and set_attr is not None:
                val, err = res.inherit_from(prev.set_attr(link, set_attr))

                if err:
                    return res.fail(err.add_frame("dot chain"))

                return res.success(val)

            if prev is None:
                if isinstance(link, Token) and link.type == "ID":
                    prev, err = res.inherit_from(scope.get(link.value, None, res=True))

                    if err:
                        return res.fail(err.add_frame(Frame(name="dot chain")))

                elif isinstance(link, Token):
                    prev = link.value

                else:
                    raise Exception

                continue

            curr, err = res.inherit_from(prev.get_attr(attr=link.value, scope=scope))

            if err:
                # Info was not passed so pass it manually
                return res.fail(err.add_frame(Frame("dot chain")))

            prev = curr

        return res.success(prev)

    def get_constants(self):
        ...

    def get_names(self) -> list[str]:
        names = []

        for name in self._chain:
            names.append(name.value)

        return names
