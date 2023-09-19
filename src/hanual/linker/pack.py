from __future__ import annotations

from typing import Any, Dict, Optional
from zipfile import ZipFile
from pickle import dump


class Pack:
    def __init__(
        self, name: str, *files: tuple[str], **metta_data: Dict[str, Any]
    ) -> None:
        self._files: list[str] = list(*files)
        self._metta = metta_data
        self._name = name

    @property
    def name(self):
        return self._name

    @property
    def metta(self):
        return self._metta

    @property
    def files(self):
        return self._files

    def add_file(self, file: str) -> None:
        self._files.append(file)

    def add_metta(self, name: str, val: Any) -> None:
        self._metta[name] = val

    def dump_pack(self, out_p: Optional[str] = None) -> None:
        with ZipFile((out_p + "/" + self.name or self.name) + ".pk", mode="w") as pack:
            # TODO : parse all files to get the function header
            # coppy all files
            for file in self._files:
                with open(file, "r") as of:
                    with pack.open(file, "w") as zf:
                        zf.write(of.read().encode("utf-8"))

            with open("$master", "wb") as master:
                dump(self._metta, master)
