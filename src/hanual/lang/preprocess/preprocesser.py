from __future__ import annotations

from io import StringIO
from typing import Dict, List, Optional, Set


class PrePeoccesser:
    """
    What is a preproccesser, so pre means before and proccess refers to the compiler, this means that
    the code is put through this class before being lexed and tokenized. This lets us use some magic
    that C and C++ users are farmiliar with. This means that we can conditionally include code. For
    example, we may want to verifiy that the Hanual version is greater than some value this opens the
    doors to lots of backwads compatability. All Preprocessers are, by default, prefixed with an `@`
    but this behaviour can be altered with the config file.
    NOTE all preprocessers are removed after processing so using a `"` is perfectely fine, it won't raise any syntax
    errors
    NOTE preprocessers can have their names changed, so `mcr` and be changed to `macro`

    The preprocessers are:
    @def => For defining replaceables
    @mcr => For creating macros
    @if  => For conditional includes
    @end => Ending an if

    + def
    This creates a definition, this is just a name that can not be used in the code, the only point
    of this is to check something.

    + mcr
    Macros are replaced at lexing time, these can replace a symbol with another. Let's say we want to
    create a new keyword "contains", that takes a symbol on the left and right, we can create a macro
    mcr "<L> contains <R>" "<R> in <L>", do note that the strings are important in this, we surround
    tokens we want to replace in angel brackets <>
    """

    def __init__(self) -> None:
        self._definitions: Set[str] = set()
        self._ignore_code: bool = False
        self._prefix: str = "@"
        self._macros = []

    @property
    def prefix(self: PrePeoccesser) -> str:
        return self._prefix

    @prefix.setter
    def prefix(self: PrePeoccesser, new: str) -> None:
        assert isinstance(new, str)
        self._prefix = new

    def add_definition(self: PrePeoccesser, name: str) -> None:
        assert isinstance(name, str)

        self._definitions.add(name)

    def process(
        self,
        text: str,
        prefix: Optional[str] = None,
        starting_defs: Optional[List[str]] = None,
    ) -> str:
        mappings: Dict[str, str] = {  # TODO: make this modifiable too
            "def": "def",
            "end": "end",
            "nif": "nif",
            "if": "if",
        }

        if not prefix is None:
            self.prefix = prefix

        if not starting_defs is None:
            [self._definitions.add(n) for n in starting_defs]

        out = StringIO()

        for line in text.split("\n"):
            if line.startswith(self.prefix):
                type_ = None

                for pos in mappings.keys():
                    if line.startswith(self.prefix + pos):
                        type_ = pos

                if type_ is None:
                    raise ValueError(f"{line!r} is not a pre processer")

                # get class function
                getattr(self, f"get_{mappings[type_]}")(line)

            elif not self._ignore_code:
                out.write(line + "\n")

        return out.getvalue()

    def get_def(self, line: str) -> None:
        # TODO use lexer
        name: str = line.split(" ")[1]  # Get the definition name

        self._definitions.add(name)

    def get_end(self, line: str) -> None:
        # We will just reset it
        self._ignore_code = False

    def get_nif(self, line) -> None:
        # TODO: add better support for this stuff
        self._ignore_code = line.split(" ")[1] in self._definitions

    def get_if(self, line: str) -> None:
        # TODO: add better support for this stuff
        self._ignore_code = not (line.split(" ")[1] in self._definitions)
