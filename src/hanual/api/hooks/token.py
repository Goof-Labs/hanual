from __future__ import annotations

from typing import Tuple, LiteralString
from hanual.lang.lexer import Token
from .hook import GenericHook


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
