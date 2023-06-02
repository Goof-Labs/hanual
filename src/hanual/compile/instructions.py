from abc import ABC, abstractmethod
from typing import Union
from io import BytesIO


_records = {}


def instruction(
    *,
    load_next4: bool = False,
    load_next_8: bool = False,
    change_heap: bool = False,
    may_jump: bool = False,
):
    opcode = _records.get((load_next4, load_next_8, change_heap, may_jump), 0)

    def decor(cls):
        cls.opcode = (
            load_next4
            << 8 + load_next_8
            << 7 + change_heap
            << 6 + may_jump
            << 5 + opcode
        )

    _records[(load_next4, load_next_8, change_heap, may_jump)] = opcode + 1
    return decor


class BaseInstruction(ABC):
    opcode: int = 0

    @abstractmethod
    def serialize(self) -> bytes:
        raise NotImplementedError


@instruction(
    load_next4=True,
    load_next_8=False,
    change_heap=True,
    may_jump=False,
)
class InstructionMOV(BaseInstruction):
    def __init__(self, to, val) -> None:
        self.val: Union[int, str] = val
        self.to: Union[int, str] = to

    def serialize(self):
        bytes_ = BytesIO()

        if isinstance(self.to, str):  # register
            # 0x00 means register
            bytes_.write(b"\x00")
            bytes_.write(
                ["A", "B", "C", "D", "E", "FL", "G", "FP", "FA"]
                .index(self.to)
                .to_bytes()
            )

        else:  #  a heap addr
            bytes_.write(b"\xFF")
            bytes_.write(self.to.to_bytes())

        if isinstance(self.val, str):  # register
            bytes_.write(b"\x00")
            bytes_.write(
                ["A", "B", "C", "D", "E", "FL", "G", "FP", "FA"]
                .index(self.val)
                .to_bytes()
            )

        else:  #  a heap addr
            bytes_.write(b"\xFF")
            bytes_.write(self.val.to_bytes())
