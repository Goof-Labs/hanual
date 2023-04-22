from typing import Self, List, Union, Dict
from hanual.lang.lexer import Token
from . import Instruction
from io import BytesIO
import hashlib


class HanualBytecodeFileWriter:
    __slots__ = ("_hash",)

    def __init__(
        self,
        source: str,
        refs: List[Union[Token, str]],
        consts: List[str],
        instructions: List[Instruction],
    ) -> None:
        # get sha256 of file
        self._hash = hashlib.sha256(source.encode("utf-8")).hexdigest()
        self._refs = refs
        self._consts = consts
        self._instructions = instructions

    def make_magic_number(self: Self) -> bytes:
        return b"\x01\x12\x35"

    def create_const_pool(self):
        buffer = BytesIO()
        buffer.write(self.make_magic_number())
        buffer.write(self._hash)
        self.dump_header(buffer)

    def dump_header(self, buffer: BytesIO) -> None:
        for ref in self._refs:
            val = ref if isinstance(ref, str) else ref.value
