from __future__ import annotations

from typing import List, Generator, LiteralString, Tuple, Optional, Type, Iterable, Dict, Any, Callable, overload
from hanual.lang.productions import DefaultProduction
from hanual.lang.proxy import Proxy, HookProxy
from hanual.lang.lexer import Token
import re


def props(**kwargs):
    def decor(cls):
        cls._props = kwargs
        return cls

    return decor


class GenericHook:
    __slots__ = "_props",

    @property
    def props(self):
        return self._props


class PreProcessorHook(GenericHook):
    def scan_lines(self, lines: List[str]) -> Generator[str, None, None]:
        """
        This method is called once if `scan_line` has not been implemented. This
        generator yields what the code aught to be. This is much more pythonic compared
        to the `scan_line` implementation.
        """
        yield from lines


def new_token(regex: Tuple[str, LiteralString], name: LiteralString):
    def decor(cls):
        cls._regex = regex[0]
        cls._type = regex[1]
        cls._name = name
        return cls

    return decor


class TokenHook(GenericHook):
    __slots__ = "_regex", "_name", "_type"

    @property
    def regex(self):
        return self._regex

    @property
    def name(self):
        return self._name

    @property
    def type(self):
        return self._type

    def gen_token(self, kind: str, value: str, line_no: int, col: int, line: str) -> Token:
        return Token(kind, value, line_no, col, line)


def new_rule(*pattern: LiteralString,
             prod: Optional[Type] = DefaultProduction,
             unless_starts: Optional[Iterable[LiteralString]] = None,
             unless_ends: Optional[Iterable[LiteralString]] = None,
             types: Optional[Dict[LiteralString, Any]] = None,
             name: Optional[str] = ""
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
    def create_rule(self, ts: DefaultProduction, types): ...

    @overload
    def create_rule(self, ts: DefaultProduction): ...

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
        return self._name or re.sub(r"(?<!^)(?=[A-Z])", "_", self.__class__.__name__).lower()
