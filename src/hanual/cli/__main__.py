from __future__ import annotations

from typing import NamedTuple, List, Dict
from tomllib import load


class CompilerSettings(NamedTuple):
    packeages: Dict[str, str]
    mappings: Dict[str, str]
    definitions: List[str]
    packall: bool
    target: str
    name: str
    main: str


if __name__ == "__main__":
    from hanual.lang.builtin_wrapper import BuiltinWrapper

    with open("project.toml", "rb") as f:
        data = load(f)
        settings = CompilerSettings(
            definitions=data["predefs"]["predefinitions"],
            packall=data["target"]["packall"],
            target=data["target"]["target"],
            mappings=data["preprocessers"],
            packeages=data["packets"],
            name=data["name"],
            main=data["entery"],
        )

    bw = BuiltinWrapper()
    bw.parse()
