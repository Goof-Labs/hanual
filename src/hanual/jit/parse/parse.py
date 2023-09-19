from __future__ import annotations

from parse.file_format import FileFormat
from typing import Generator, List, TYPE_CHECKING, Dict, Any
from dataclass import dataclass
from io import BytesIO

if TYPE_CHECKING:
    from hanual.jit.constant import Constant


class CompileParser:
    def __init__(self):
        ...

    def parse_buffer(self, buffer: BytesIO) -> None:
        header = self.parse_header(buffer)
        constants = self.read_constants(buffer)
        file_deps = self.read_file_deps(buffer)
        fn_header = self.read_fn_header(buffer)
        instructions = self.read_instructions(buffer)

        return FileFormat(
            **header, file_deps=file_deps, fn_table=fn_header, instructions=instructions
        )

    def parse_header(self, buffer: BytesIO) -> Dict[str, Any]:
        magic = buffer.read(4).decode()  # b"LMAO"
        src_hash = buffer.read(48).decode()  # a base 64 sha256 hash of the source code
        # read the version number
        major = int.from_bytes(buffer.read(1))
        minor = int.from_bytes(buffer.read(1))
        micro = int.from_bytes(buffer.read(1))
        return {
            "magic": magic,
            "hash": src_hash,
            "major": major,
            "minor": minor,
            "micro": micro,
        }

    def parse_constants(self, buffer: BytesIO) -> List[Constant]:
        constants: List[Constant] = []
        constant_bytes = BytesIO()

        # a 00 00 byte pattern signifies the end of the constant pool, `end` is a flag
        end = False

        while True:
            byte = buffer.read(1)

            # end of constant pool
            if byte == b"\x00" and end:
                break

            # reset end
            end = False

            if byte == b"\x00":
                constants.append(Constant.from_bytes(constant_bytes.getvalue()))
                # 'better' for whatever reason :|
                constant_bytes = BytesIO()
                end = True
                continue

            constant_bytes.write(byte)

        return constants
