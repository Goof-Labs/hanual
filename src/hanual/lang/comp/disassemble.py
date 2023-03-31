from __future__ import annotations

from typing import Union, TextIO, NamedTuple, Tuple, List
from .instructions import Instructions
from io import BytesIO, StringIO


class _ConstantMettaData(NamedTuple):
    primitive: bool
    from_user: bool
    identity: int
    # either the index of the user defined type in the pool or the id of the primitive type


class Disassembeler:
    def __init__(self, code: Union[str, bytes, TextIO]) -> None:
        self._bytes: BytesIO = None

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
        magic: bytes = self._bytes.read(3)  # should be 4C 4F 4C

        major: bytes = self._bytes.read(1)  # majour version 0 to 255
        minor: bytes = self._bytes.read(1)  # minor version o to 255
        # 65,536 possible versions

        num_constants: int = self._bytes.read(2)
        constants = []

        escape: bool = False
        for _ in range(num_constants):

            value: List[int] = []

            metta: _ConstantMettaData = self._parse_constant_metta_data(
                self._bytes.read(1)
            )

            while True:
                byte = self._bytes.read(1)

                as_int = int.from_bytes(byte)

                if as_int == 0x00 and not escape:
                    break

                elif as_int == 0x00 and escape:
                    value.append(0x00)

                elif (
                    as_int != 0x00 and escape
                ):  # have an escape sequence without an escapeable byte
                    value.append(0xFF)

                else:
                    value.append(as_int)

            if metta.primitive:
                constants.append(
                    self._interprate_bytes_primitive(value, metta.identity)
                )

            else:
                constants.append(self._interperate_bytes_complex(value, metta.identity))

        self._bytes.read(1)  # padding byte
        # Constant tabel
        self._bytes.read(1)  # padding byte

    def _parse_constant_metta_data(self, byte) -> _ConstantMettaData:
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
            primitive=bool(raw_bin[0]), from_user=bool(raw_bin[1]), identity=nibble
        )

    def _interprate_bytes_primitive(
        self, byte_list: Tuple[int], use_as
    ) -> Union[str, int]:
        """
        This method takes in a BytesIO object to interprate bytes
        in a specific way. The form of interpratation is defined
        through the use_as.
        """

        escape: bool = False

        if use_as == "str":
            str_io = StringIO()

            for byte in byte_list:
                str_io.write(chr(byte))

            return str_io.getvalue()

        else:
            raise NotImplementedError(
                "'%s' is not recognised as an interpratation type, one of str , int",
                use_as,
            )

    def _interperate_bytes_complex(self):
        """
        This method will create a complex datatype such as
        a struct. This is verry diffeent to the primitive
        types because we need to take care of custom
        attributes and so on.
        """
        raise NotImplementedError
