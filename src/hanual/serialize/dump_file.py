from __future__ import annotations


from typing import List, Dict, TYPE_CHECKING
from hanual.compile.label import Label
from base64 import b64encode
from io import BytesIO

if TYPE_CHECKING:
    from hanual.compile.compile_manager import CompileManager
    from hanual.compile.constant import Constant
    from hanual.compile.instruction import *
    from hashlib import _Hash


class DumpFile:
    def __init__(self) -> None:
        self._bytes = BytesIO()

    def dump_head(
        self,
        major: int,
        minor: int,
        micro: int,
        hash: _Hash,
        append: bool = False,
    ):
        head = BytesIO()
        head.write(b"LMAO")
        head.write(b64encode(hash.hexdigest().encode("utf-8")))
        head.write(major.to_bytes(length=1, byteorder="big"))
        head.write(minor.to_bytes(length=1, byteorder="big"))
        head.write(micro.to_bytes(length=1, byteorder="big"))

        if append:
            self._bytes.write(head.getvalue())

        return head.getvalue()

    def dump_constants(self, constants: List[Constant], append: bool = False) -> bytes:
        data = BytesIO()

        for constant in constants:
            data.write(constant.serialize())
            data.write(b"\x00")

        data.write(b"\x00")

        if append:
            self._bytes.write(data.getvalue())

        return data.getvalue()

    def dump_deps(self, deps: List[str], append: bool = False):
        data = BytesIO()

        for dep in deps:
            data.write(dep.encode("utf-8"))
            data.write(b"\x00")

        data.write(b"\x00")

        if append:
            self._bytes.write(data.getvalue())

        return data.getvalue()

    def dump_func_head(self, funcs: Dict[str, int], append: bool = False):
        fn_table = BytesIO()

        for name, start in funcs.items():
            fn_table.write(name.encode("utf-8"))
            fn_table.write(b"\x00")
            fn_table.write(start.to_bytes(length=4))
            fn_table.write(b"\x00")

        fn_table.write(b"\x00")

        if append:
            self._bytes.write(fn_table.getvalue())

        return fn_table.getvalue()

    def dump_instructions(
        self,
        cm: CompileManager,
        append: bool = False,
    ):
        data = BytesIO()

        for idx, instr in enumerate(cm.instructions):
            if isinstance(instr, Label):
                # lables surve as jump points and don't need to be added to the
                pass

            else:
                print(instr)
                data.write(instr.serialize(consts=cm.consts, names=cm.names))

        if append:
            self._bytes.write(data.getvalue())

        return data.getvalue()

    @property
    def bytes(self):
        return self._bytes.getvalue()
