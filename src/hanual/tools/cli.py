from __future__ import annotations

from configparser import ConfigParser, ExtendedInterpolation
from hanual.compile.options import CompilerOptions
from typing import TYPE_CHECKING
from sys import argv
import os


if TYPE_CHECKING:
    from typing_extensions import Self


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

    def parse_config(self: Self) -> Self:
        cfg = self.kwargs.get("cfg", None)

        # no configuration passed
        if not cfg:
            return self

        # check if cfg exists
        if not os.path.exists(cfg):
            raise Exception(f"{cfg!r} does not exist")

        conf_parser = ConfigParser(interpolation=ExtendedInterpolation())
        conf_parser.read(cfg)

        for k, v in conf_parser["cli-options"].items():
            if "," in v:
                v = v.split(",")

            self.kwargs[k] = v

        return self

    @property
    def options(self: Self) -> CompilerOptions:
        return CompilerOptions(**{k: v for k, v in self.kwargs.items() if k in CompilerOptions.__dict__.keys()})


def main():
    print(HanualCli().options)


if __name__ == "__main__":
    main()
