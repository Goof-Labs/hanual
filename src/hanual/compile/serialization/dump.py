from __future__ import annotations


from hanual.compile.instruction import Instruction
from hanual.version import major, minor, micro
from typing import Dict, TypeVar, List, Tuple
from base64 import b64encode
from hashlib import sha256
from io import BytesIO

HanualObject = TypeVar("HanualObject", int, float, str)


class HanualFileSerializer:
    @staticmethod
    def serialize_constants(constants: List[HanualObject]):
        consts_pool = BytesIO()

        consts_pool.write(len(constants).to_bytes(length=1, byteorder="big"))

        for const in constants:
            consts_pool.write(b"\x00\x00\x00")

            if isinstance(const, int):
                consts_pool.write(b"\x00")
                consts_pool.write(const.to_bytes(length=1, byteorder="big"))

            elif isinstance(const, float):
                consts_pool.write(b"\x01")
                ratio = const.as_integer_ratio()  # this is a fraction
                consts_pool.write(ratio[0])
                consts_pool.write(b"\x00")
                consts_pool.write(ratio[1])

            elif isinstance(const, str):
                consts_pool.write(b"\x02")
                for char in const:
                    consts_pool.write(ord(char).to_bytes(length=1, byteorder="big"))

        consts_pool.write(b"\x00\x00\x00")

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
    def serialize_refs(refs: List[str]) -> None:
        raise NotImplementedError

    @staticmethod
    def dump(
        data: Tuple[Dict[str, List[HanualObject]], List[Instruction]], src: str
    ) -> bytes:
        buffer = BytesIO()

        buffer.write(HanualFileSerializer.create_header(src))
        buffer.write(HanualFileSerializer.serialize_constants(data[0]["consts"]))
        buffer.write(HanualFileSerializer.serialize_refs(data[0]["refs"]))

        for instruction in data[1]:
            buffer.write(instruction.opcode.to_bytes(byteorder="big"))

            if instruction.next is not None:
                buffer.write(instruction.next.to_bytes(byteorder="big"))

        return buffer.getvalue()
