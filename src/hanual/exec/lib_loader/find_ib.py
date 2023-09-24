from __future__ import annotations

import zipfile
from typing import Dict, NamedTuple
from pathlib import Path


class FunctionInfo(NamedTuple):
    name: str
    start: int
    origin: str


class HanualLibrary:
    __slots__ = "_path", "_functions",

    def __init__(self, path: Path) -> None:
        self._path = path
        self._functions: Dict[str, FunctionInfo] = {}

    def lazy_load(self):
        """
		Lazy loading should check if the path exists and figure out what the lib type is:
		 - Stand alone
		 - Source file
		 - Package

		The laxy load should also index the file and see what functions exist, so if a
		user references an external function we can instantly verifiy if it exists or not,
		loading the file will only happen when the file explicitly needs to be fully
		loaded or when an external function is called (read ahead).

		If a function is called from a stand alone compiled file, the function header should
		be loaded and the function found, then execution of the function should start.

		If the function is a source file the file should be converted to an ast and the
		function be found and executed, to remove potential scoping problems the whole file
		is only run if the function references anything (including other imports) at
		execution time.

		If the function is in a pcakage the function should be found in the `~MASTER` file
		if it isn't the program raises an error saing it can't find the function, else the
		file is loaded and the header is parsed.
		"""

        if zipfile.is_zipfile(self._path.absolute()):
            self._parse_zip()

    def _parse_zip(self):
        from pickle import load

        with zipfile.ZipFile(self._path.absolute(), mode="r") as pack:
            with pack.open("~MASTER") as master:
                data = load(master)

                for path in data["files"]:
                    # path = str path to current file

                    for name, pos in self._get_funcs_from_bin(pack.read(path)):
                        self._functions[name] = FunctionInfo(name=name, start=pos, origin=path)

    def _get_funcs_from_bin(self, data: bytes) -> Dict[str, int]:
        ...
