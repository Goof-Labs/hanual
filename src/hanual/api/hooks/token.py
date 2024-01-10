from __future__ import annotations

from typing import LiteralString

from hanual.api.hooks.hook import GenericHook

from hanual.lang.util.line_range import LineRange
from hanual.lang.lexer import Token


def new_token(regex: tuple[str, LiteralString], name: LiteralString):
    """A decorator to define a new token.

    > This decorator is used to decorate a token class, said class must
    > inherit from `TokenHook`. This function doesn't register the token
    > but is a cleaner way to define the class attributes.

    @regex^tuple[str, LiteralString]>
    """

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

    def gen_token(
        self, kind: str, value: str, line_range: LineRange, col: int, line: str
    ) -> Token:
        return Token(kind, value, line_range, col, line)
