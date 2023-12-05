from __future__ import annotations

from typing import Literal


def get_long_description(lines: list[str]):
    while lines:
        line: str = lines[0].lstrip()

        if not line:
            lines.pop(0)
            continue

        if line[0] != ">":
            break

        lines.pop(0)
        yield line.lstrip(" >")


def get_parameters(text: list[str]):
    while text:
        line: str = text[0].lstrip()

        if line[0] == "@":  # new parameter doc
            p_name, *rest = line[1:].split("^")
            p_type, *doc = "^".join(rest).split(">")

            text.pop(0)

            buildup = ""
            while text:
                ln: str = text[0].lstrip()

                if not ln:
                    text.pop(0)
                    continue

                if ln[0] == "|":
                    buildup += text.pop(0).lstrip(" |")

                else:
                    break

            yield p_name, p_type, ">".join(doc), buildup

        else:
            raise Exception


def parse_doc_string(text: str | Literal[None]):
    if text is None:
        raise Exception("doc string is None")

    lines: list[str] = text.split("\n")
    return {"desc": get_long_description(lines), "params": get_parameters(lines)}
