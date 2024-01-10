from __future__ import annotations

from typing import Literal


def parse_doc_string(
    text: str | Literal[None],
) -> tuple[str | None, str, list[list[str]]] | None:
    if text is None:
        return

    summary: str | None = None
    long: str = ""
    params: list[list[str]] = []

    for line in text.split("\n"):
        line = line.strip()

        if not line:
            continue

        if line[0] not in ">@" and summary is None:
            summary = line

        elif line[0] == ">":
            long += line.lstrip(">") + "\n"

        elif line[0] == "@":
            name, *rest = line[1:].split("^")
            data_type, *desc = "^".join(rest).split(">")
            params.append([name, data_type, ">".join(desc), ""])

        elif line[0] == "|":
            params[-1][3] += line.lstrip("| ") + " "

    return summary, long, params
