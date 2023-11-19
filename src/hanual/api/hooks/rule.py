from __future__ import annotations

import re
from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    LiteralString,
    Optional,
    Type,
    overload,
)

from hanual.lang.productions import DefaultProduction
from hanual.lang.util.proxy import HookProxy, Proxy

from .hook import GenericHook


def new_rule(
    *pattern: LiteralString,
    prod: Optional[Type] = DefaultProduction,
    unless_starts: Optional[Iterable[LiteralString]] = None,
    unless_ends: Optional[Iterable[LiteralString]] = None,
    types: Optional[Dict[LiteralString, Any]] = None,
    name: Optional[str] = "",
) -> Callable[[Type[RuleHook]], Type[RuleHook]]:
    def decor(cls: Type[RuleHook]):
        cls._proxy = HookProxy(cls, types, prod, unless_starts, unless_ends)
        cls._pattern = pattern
        cls._name = name
        return cls

    return decor


class RuleHook(GenericHook):
    __slots__ = "_proxy", "_pattern", "_name"

    @overload
    def create_rule(self, ts: DefaultProduction, types):
        ...

    @overload
    def create_rule(self, ts: DefaultProduction):
        ...

    def create_rule(self, *args, **kwargs):
        raise NotImplementedError

    @property
    def proxy(self) -> Proxy:
        return self._proxy

    @property
    def patterns(self):
        return self._pattern

    @property
    def name(self):
        # SET A NAME, OR YOU WILL FEEL PAIN
        # also if the name is empty, the default if one is not given, then the class name is converted to snake case
        # and that is used. THX to: vvvvvvv
        # <https://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-snake-case>
        return (
            self._name
            or re.sub(r"(?<!^)(?=[A-Z])", "_", self.__class__.__name__).lower()
        )
