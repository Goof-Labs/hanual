from __future__ import annotations

import os
from sys import argv
from configparser import ConfigParser, ExtendedInterpolation
from typing_extensions import Self

from hanual.compile.options import CompilerOptions


class HanualCli:
    __slots__ = ("kwargs",)

    def __init__(self: Self) -> None:
        self.kwargs = {}
        self.parse_config()
        self.parse_argv()

    def parse_argv(self: Self):
        loose = []

        for arg in argv:
            if "=" in arg:
                name, val = arg.split("=", 1)
                self.kwargs[name] = tuple(val.split(",")) if "," in val else val

            else:
                loose.append(arg)

        self.kwargs["loose_args"] = loose

    def parse_config(self: Self):
        if not os.path.exists("project.toml"):
            return

        conf_parser = ConfigParser(interpolation=ExtendedInterpolation())

        with open("project.toml", "r") as f:
            self.kwargs = {**self.kwargs, **conf_parser.read_file(f)}

    @property
    def options(self: Self) -> CompilerOptions:
        return CompilerOptions(**{k: v for k, v in self.kwargs.items() if k in CompilerOptions.__dict__.keys()})


def main():
    print(HanualCli().options)


if __name__ == "__main__":
    main()
