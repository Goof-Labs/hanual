from __future__ import annotations

from hanual.lang.errors import ProjectTomlNotFound
from typing import NamedTuple, List, Dict
from pprint import pprint
from tomllib import load


class CompilerSettings(NamedTuple):
    packeages: Dict[str, str]
    mappings: Dict[str, str]
    definitions: List[str]
    packall: bool
    target: str
    name: str
    main: str
    file: str


if __name__ == "__main__":
    from hanual.lang.builtin_wrapper import BuiltinWrapper

    default = {
        "name": "hello_world",
        "entery": "main",
        "preprocessers": {
            "prefix": "@",
            "nif": "nif",
            "end": "end",
            "def": "def",
            "if": "if",
        },
        "predefs": {
            "predefinitions": [],
        },
        "packets": {
            "std": "@latest",
        },
        "warnif": {
            "macro_substitution": False,
            "shoutkw": False,
        },
        "target": {
            "target": "bundle",
            "packall": False,
        },
    }

    try:
        with open("project.toml", "rb") as f:
            data = {**load(f), **default}

    except FileNotFoundError:
        ProjectTomlNotFound().be_raised()

    settings = CompilerSettings(
        definitions=data["predefs"]["predefinitions"],
        packall=data["target"]["packall"],
        target=data["target"]["target"],
        mappings=data["preprocessers"],
        packeages=data["packets"],
        name=data["name"],
        main=data["entery"],
        file=data["file"],
    )

    bw = BuiltinWrapper()

    with open(settings.file, "r") as f:
        ast = bw.parse(f.read(), settings)

        for line in ast:
            pprint(line.as_dict(), indent=2, width=100)
