from hanual.compile.instruction import Instruction
from hanual.version import major, minor, micro
from typing import Dict, TypeVar, List
from hanual.lang.lexer import Token
from base64 import b64encode
from hashlib import sha256
from io import BytesIO

HanualObject = TypeVar("HanualObject", int, float, str)


class HanualFileSerializer:
    @staticmethod
    def serialize_constants(constants: List[HanualObject]):
        pass

    @staticmethod
    def create_header(source: str) -> bytes:
        header = BytesIO()

        header.write(b"LMAO")  # magic number
        header.write(
            b64encode(sha256(source.encode()).digest(), altchars=b"/=")
        )  # checksum for the code so we know if there has been a change
        header.write((major).to_bytes("big"))  # = write version number
        header.write((minor).to_bytes("big"))
        header.write((micro).to_bytes("big"))

        return header.getvalue()

    @staticmethod
    def dump(
        constants: Dict[str, HanualObject],
        refs: List[Token],
        instructions: List[Instruction],
        source: str,
    ) -> None:
        file = BytesIO()

        file.write(HanualFileSerializer.create_header(source))
        file.write(HanualFileSerializer.serialize_constants(constants))
