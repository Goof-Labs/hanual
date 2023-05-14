from __future__ import annotations

from hanual.compile.instruction import Instruction, InstructionEnum
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
        self._function_def = False

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

    @property
    def function_def(self):
        return self._function_def

    def compile(self, global_state: Assembler) -> Any:
        # function definitions and calling is handled differently by args
        if self._function_def:
            for name in self._children:
                assert isinstance(name, Token)

                if name.type == "ID":
                    global_state.pull_value(name)

                else:
                    idx = global_state.add_constant(name.value)
                    global_state.add_instructions(Instruction(InstructionEnum.PGC, idx))

        # calling
        else:
            for obj in self.children:
                if hasattr(obj, "compile"):
                    obj.compile(global_state)

                elif isinstance(obj, Token):
                    # variable ID
                    if obj.type == "ID":
                        global_state.pull_value(obj.value)

                    elif obj.type in ("NUM", "STR"):
                        val = global_state.add_constant(obj)

                        global_state.add_instructions(
                            Instruction(InstructionEnum.PGC, val)
                        )

                    else:
                        raise Exception

                else:
                    raise Exception

    def as_dict(self) -> Dict[str, Any]:
        return {
            "type": type(self).__name__,
            "values": [
                c.as_dict() if hasattr(c, "as_dict") else c for c in self.children
            ],
        }
