from __future__ import annotations


from hanual.compile.instruction import Instruction
from hanual.version import major, minor, micro
from typing import Dict, TypeVar, List, Tuple
from hanual.lang.lexer import Token
from base64 import b64encode
from hashlib import sha256
from io import BytesIO

HanualObject = TypeVar("HanualObject", int, float, str)


class HanualFileSerializer:
    @staticmethod
    def serialize_constants(constants: List[Token]):
        consts_pool = BytesIO()

        consts_pool.write(len(constants).to_bytes(length=1, byteorder="big"))
        consts_pool.write(b"\x00\x00")

        for const in constants:
            if const.type == "NUM": # NUMBERS
                if isinstance(const.value, int):
                    consts_pool.write(b"\x01")
                    consts_pool.write(const.value.to_bytes(length=1, byteorder="big"))

                elif isinstance(const.value, float):
                    consts_pool.write(b"\x02")
                    ratio = const.value.as_integer_ratio()  # this is a fraction
                    consts_pool.write(ratio[0].to_bytes(length=1, byteorder="big"))
                    consts_pool.write(ratio[1].to_bytes(length=1, byteorder="big"))

            elif const.type == "STR":
                consts_pool.write(b"\x03")

                for char in const.value:
                    consts_pool.write(ord(char).to_bytes(length=1, byteorder="big"))

        consts_pool.write(b"\x00\x00")

        return consts_pool.getvalue()

    @staticmethod
    def create_header(source: str) -> bytes:
        header = BytesIO()

        header.write(b"LMAO")  # magic number
        header.write(
            b64encode(sha256(source.encode()).digest(), altchars=b"+=")
        )  # checksum for the code, so we know if there has been a change
        header.write(
            major.to_bytes(length=1, byteorder="big")
        )  # = write version number
        header.write(minor.to_bytes(length=1, byteorder="big"))
        header.write(micro.to_bytes(length=1, byteorder="big"))

        return header.getvalue()

    @staticmethod
    def dump(
        data: Tuple[Dict[str, List[HanualObject]], List[Instruction]], src: str
    ) -> bytes:
        buffer = BytesIO()

        buffer.write(HanualFileSerializer.create_header(src))
        print(data[1])
        buffer.write(HanualFileSerializer.serialize_constants(data[1]["consts"]))

        for instruction in data[0]:
            buffer.write(instruction.opcode.to_bytes(byteorder="big"))

            if not (instruction.next is None):
                buffer.write(instruction.next.to_bytes(byteorder="big"))

        return buffer.getvalue()
