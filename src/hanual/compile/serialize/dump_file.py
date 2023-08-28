from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List, Self, Tuple, overload, Generator, Union
from hanual.compile.label import Label
from types import GeneratorType
from base64 import b64encode
from hashlib import sha256
from io import BytesIO

if TYPE_CHECKING:
    from hanual.compile.constants.constant import BaseConstant
    from hanual.compile.compile_manager import CompileManager


class DumpFile:
    def __init__(self) -> None:
        self._bytes = BytesIO()

    def dump_head(self, major: int, minor: int, micro: int, hash_: str, append: bool = False):
        head = BytesIO()
        head.write(b"LMAO")
        head.write(b64encode(hash_.encode("utf-8")))
        head.write(major.to_bytes(length=1, byteorder="big"))
        head.write(minor.to_bytes(length=1, byteorder="big"))
        head.write(micro.to_bytes(length=1, byteorder="big"))

        if append:
            self._bytes.write(head.getvalue())

        return head.getvalue()

    def dump_constants(
            self, constants: List[BaseConstant], append: bool = False
    ) -> bytes:
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

    def dump_func_head(self, funcs: Dict[str, Label], append: bool = False):
        fn_table = BytesIO()

        for name, start in funcs.items():
            fn_table.write(name.encode("utf-8"))
            fn_table.write(b"\x00")
            fn_table.write(start.index.to_bytes(length=4, byteorder="big"))
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
                instr.index = idx

            else:
                data.write(instr.serialize(consts=cm.consts, names=cm.names, cm=cm))

        if append:
            self._bytes.write(data.getvalue())

        return data.getvalue()

    @overload
    def dump_file(self, cm: CompileManager, version: Tuple[int, int, int], src: Generator[str, None, None]) -> Self:
        ...

    @overload
    def dump_file(self, cm: CompileManager, version: Tuple[int, int, int], src: str) -> Self:
        ...

    def dump_file(self, *args, **kwargs):
        ma, mi, mc = kwargs.get("version", args[1])  # unpack into major minor micro
        cm = kwargs.get("cm", args[0])

        # first check to see if the user has passed a hash as a kwargs, default = None
        hash_ = kwargs.get("hash_", None)

        # No hash, create one from either the raw src code or generator, (created when preprocessing, if being lazy)
        if not hash_:
            hash_ = self.hash_src(kwargs.get("src", args[2]))

        self.dump_head(ma, mi, mc, hash_, append=True)
        self.dump_deps(cm.file_deps, append=True)
        self.dump_func_head(cm.fn_table, append=True)
        self.dump_constants(cm.consts, append=True)
        self.dump_instructions(cm, append=True)
        return self

    @staticmethod
    def hash_src(src: Union[str, Generator[str, None, None]]) -> str:
        hash_ = sha256()

        if isinstance(src, GeneratorType):
            for line in src:
                hash_.update(line.encode("utf-8"))

        else:
            hash_.update(src.encode("utf-8"))

        return hash_.hexdigest()

    @property
    def bytes(self):
        return self._bytes.getvalue()
