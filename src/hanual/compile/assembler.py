from __future__ import annotations


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Set, List, Union
    from .instruction import Instruction
    from .label import Label


class Assembler:
    def __init__(self):
        self.constants: Set[Union[str, int]] = set()
        self.instructions: List[Instruction] = []
        self.function_table: Set[Label] = set()
        self.file_deps: Set[str] = set()
        self.fn_deps: Set[str] = set()
        self.labels: List[Label] = []
        self.heap: List[str] = []
        self.index: int = 0

    def add_instruction(self, i: Instruction):
        self.instructions.append(i)
        self.index += 1

    def mov(self, tar: Union[str, int], dest: Union[str, int]) -> None:
        match (tar in ("A", "B", "C", "D", "E"), dest in ("A", "B", "C", "D", "E")):
            case True, True:
                # reg -> reg
                ...

            case False, True:
                # Heap -> reg
                ...

            case True, False:
                # reg -> heap
                ...
