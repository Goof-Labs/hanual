from __future__ import annotations


class ByteCodeInstruction:
    # refer to https://unpyc.sourceforge.net/Opcodes.html

    def __init__(self, instruction, *args):
        ...

    def gen(self):
        pass
