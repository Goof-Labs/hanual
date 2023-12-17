from __future__ import annotations


class ByteCodeInstruction:
    # refer to https://unpyc.sourceforge.net/Opcodes.html

    def __init__(self, instruction, *args):
        self._instruction = instruction
        self._args = args

    def gen(self):
        raise NotImplementedError

    def __str__(self):
        return f"Instruction({self._instruction} {self._args})"

    def __repr__(self):
        return str(self)
