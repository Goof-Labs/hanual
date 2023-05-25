from __future__ import annotations

from hanual.compile.instruction import (
    InstructionCFA,
    InstructionAFA,
    InstructionFLG,
    InstructionMVA,
)
from typing import TypeVar, Union, List, Any, Dict, TYPE_CHECKING
from hanual.lang.nodes.base_node import BaseNode
from hanual.lang.builtin_lexer import Token

if TYPE_CHECKING:
    from hanual.compile import Assembler

T = TypeVar("T")


class Arguments(BaseNode):
    __slots__ = "_children", "_function_def"

    def __init__(self, children: Union[List[T], T]) -> None:
        self._children: List[Token]
        self.function_def = False

        if isinstance(children, Token):
            self._children = [children]

        elif isinstance(children, (tuple, list)):  # is iterable
            self._children = [*children]

        else:  # This is just another node that we have chucked into a list
            self._children = [children]

    def add_child(self, child):
        if isinstance(child, Arguments):
            self._children.extend(child.children)

        else:
            self._children.append(child)

        return self

    @property
    def children(self) -> List[T]:
        return self._children

    def compile(self, global_state: Assembler) -> Any:
        # function definitions and calling is handled differently by args
        if self.function_def:
            for name in self._children:
                assert isinstance(name, Token)
                # The bytecode will wrap the arguments into a tuple, so we probably want to unpack them.
                # Yes this is inefficient to pack and then unpack but still
                # TODO

        # calling
        else:
            global_state.instructions.append(InstructionCFA())

            for obj in self.children:
                if hasattr(obj, "compile"):
                    obj.compile(global_state)

                elif isinstance(obj, Token):
                    if obj.type == "ID":
                        # get index of value, move ptr into A register move flag to move A register into function args
                        id_ = global_state.heap.index(obj.value)
                        global_state.instructions.append(InstructionMVA(id_))
                        global_state.instructions.append(InstructionFLG(0b1000_0000))
                        global_state.instructions.append(InstructionAFA(0b0000_0000))

                    elif obj.type == "ID" or obj.type == "":
                        ...

    def as_dict(self) -> Dict[str, Any]:
        return {
            "type": type(self).__name__,
            "values": [
                c.as_dict() if hasattr(c, "as_dict") else c for c in self.children
            ],
        }
