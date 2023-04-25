from __future__ import annotations


from hanual.compile.instruction import Instruction
from typing import Tuple, Dict, Union, List
from hanual.lang.lexer import Token


class Disasembeler:
    def __init__(self) -> None:
        pass

    @staticmethod
    def disasable(
        self, code: Tuple[Dict[str, Union[str, Token, int]], List[Instruction]]
    ) -> None:
        for instruction in code[1]:
            print(instruction)
