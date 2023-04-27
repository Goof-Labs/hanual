from typing import NamedTuple
from tomllib import load
from sys import exit


class CompilerSettings(NamedTuple):
    definitions: list[str]
    search_dirs: list[str]
    packeages: list[str]
    mode: str
    name: str


with open("prodject.toml", "rb") as f:
    data = load(f)
    settings = CompilerSettings(data[""])

