from __future__ import annotations

from typing import Union, TextIO, NamedTuple
from .instruictions import Instructions
from io import BytesIO


class _ConstantMettaData(NamedTuple):
    primitive: bool
    from_user: bool
    identity: int
    # either the index of the user defined type in the pool or the id of the primitive type


class Disassembeler:
    def __init__(self, code: Union[str, bytes, TextIO]) -> None:
        self._bytes = None

        if isinstance(code, str):
            with open(code, "rb") as f:
                self._bytes = f.read()

        elif isinstance(code, bytes):
            self._bytes = code

        elif isinstance(code, TextIO):
            self._bytes = code.read()

        else:
            raise ValueError(
                "Expected one of [str, bytes, TextIO] for '%s'",
                (type(code).__name__),
            )

    def parse(self):
        magic: bytes = self._bytes.read(3) # should be 4C 4F 4C

        major: bytes = self._bytes.read(1) # majour version 0 to 255
        minor: bytes = self._bytes.read(1) # minor version o to 255
        # 65,536 possible versions

        num_constants: int = self._bytes.read(2)

        self._bytes.read(1) # padding byte
        # Constant tabel
        self._bytes.read(1) # padding byte

    def _read_next_constant(self) -> Union[str, int]:
        data = self._parse_constant_metta_data(self._bytes.read(1))

        escape: bool = False
        while True:
            ...

    def _parse_constant_metta_data(self, byte):
        """
        ABXX  C
        vvvv vvvv
        0000 0000

        X => Just 0 , not come up with a meaning yet

        A => If the data is a primitive or complex
        B => If the data is user defined
        C => The last nibble of data, if the data is
             primitive then this is the id of the data
             type, otherwise this is a reference to
             the type that the user has used
        """
        raw_bin = tuple(int(bit) for bit in bin(byte[0])[2:].zfill(8))

        # get value of last nibble as an int
        nibble = 0
        for bit in raw_bin[:4]:
            nibble += bit
            nibble = nibble << 1

        return _ConstantMettaData(
            primitive=bool(raw_bin[0]),
            from_user=bool(raw_bin[1]),
            identity=nibble
        )

