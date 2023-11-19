from __future__ import annotations

import logging
import sys
from argparse import ArgumentParser, Namespace

from hanual.lang import compile_code


def main():
    logging.basicConfig(level=logging.DEBUG)

    cli = ArgumentParser("Hanual programming language")

    cli.add_argument(
        "script",
        nargs="*",
        help="The file you want to run",
    )

    cli.add_argument(
        "-repl",
        action="store_true",
        help="Run a repl after the program has executed",
    )

    cli.add_argument(
        "-keep",
        action="store_true",
        help="Outputs the executed code as a file",
    )

    cli.add_argument(
        "-asm",
        action="store_true",
        help="Print the asembely of the code",
    )

    namespace = cli.parse_args(sys.argv)

    with open(namespace.script[1], "r") as f:
        compile_code(f.read())


if __name__ == "__main__":
    main()
