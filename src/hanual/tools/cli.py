from __future__ import annotations

from hanual.compile.options import CompilerOptions
from typing_extensions import Self
from sys import argv
import re


class HanualCli:
    __slots__ = ("kwargs",)

    def __init__(self: Self) -> None:
        self.kwargs = {}
        self.parse_argv()

    def parse_argv(self: Self):
        command = " ".join(argv)

        arg_fmt = re.compile(r"--[a-zA-Z_,]*=[a-zA-Z0-9.]*")
        for arg in arg_fmt.findall(command):
            name, val = arg.removeprefix("--").split("=", 1)
            self.kwargs[name] = val

    @property
    def options(self: Self) -> CompilerOptions:
        return CompilerOptions(**self.kwargs)


HanualCli()
