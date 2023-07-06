from __future__ import annotations

from colorama import init, Fore, Back
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hanual.lang.builtin_lexer import Token


class Error:
    def __init__(self, token: Token, hint: str, level: int) -> None:
        ...

    @property
    def levels(self):
        return {}

    def execute(self):
        init(autoreset=True)
