from __future__ import annotations

from hanual.compile.instruction import Instruction, InstructionYNK
from hanual.lang.types.singelton import Singleton
from hanual.lang.errors import NameNotFoundError
from typing import TypeVar, List, Union
from hanual.lang.lexer import Token

T = TypeVar("T")


class Stack(Singleton):
    def __init__(self) -> None:
        self.__stk: List[T] = []

    def push(self, name: T) -> None:
        self.__stk.append(name)

    def pop(self) -> T:
        return self.__stk.pop()

    def push_item_to_top(self, token: Union[T, Token]) -> Instruction:
        if isinstance(token, Token):
            name = token.value

        else:
            name = token

        for idx, item in enumerate(self.__stk):
            if item == name:
                # yank nth element to top of stack
                return InstructionYNK(idx)

        assert False, isinstance(token, Token)

        NameNotFoundError().be_raised(
            token.line_val,
            token.line,
            token.colm,
            f"The name '{name}' could not be found",
        )

    @property
    def stack_size(self) -> int:
        return len(self.__stk)
