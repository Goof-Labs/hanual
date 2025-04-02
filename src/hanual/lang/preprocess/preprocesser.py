from __future__ import annotations

from typing import TYPE_CHECKING, Generator, Optional


class Preprocessor:
    """
    What is a preprocessor, so pre means before and processes refers to the compiler, this means that
    the code is put through this class before being lexed and tokenized. This lets us use some magic
    that C and C++ users are familiar with. This means that we can conditionally include code. For
    example, we may want to verify that the Hanual version is greater than some value this opens the
    doors to lots of backwards compatability. All Preprocessors are, by default, prefixed with an `@`
    but this behavior can be altered with the config file.

    The preprocessors are:
    @def => For defining replaceable
    @if => For conditional includes
    @end => Ending an if
    """

    def __init__(
        self,
        pre_defs: Optional[list[str]] = None,
        prefix: Optional[str] = "@",
    ) -> None:
        self._definitions: list[str] = pre_defs or []
        self._prefix: str = prefix or "@"

        self._ignore_code: bool = False

    @property
    def prefix(self: Preprocessor) -> str:
        return self._prefix

    @prefix.setter
    def prefix(self: Preprocessor, prefix: str) -> None:
        assert isinstance(prefix, str), ValueError(
            f"Prefix must be of type str not {type(prefix).__name__!r}"
        )
        self._prefix = prefix

    @prefix.setter
    def prefix(self: Preprocessor, new: str) -> None:
        assert isinstance(new, str)
        self._prefix = new

    def add_definition(self: Preprocessor, name: str) -> None:
        assert isinstance(name, str), ValueError(
            f"Name must be of type str not {type(name).__name__}"
        )

        self._definitions.append(name)

    def process(
        self,
        text: str,
        prefix: Optional[str] = None,
        starting_defs: Optional[list[str]] = None,
        # mappings: Optional[Mapping[str, str]] = None,
    ) -> Generator[str, None, None]:
        # if mappings is None:
        #    mappings = {}

        mappings: dict[str, str] = {  # TODO: make this modifiable too
            "def": "def",
            "end": "end",
            "nif": "nif",
            "if": "if",
            # **mappings,
        }

        if prefix is not None:
            self.prefix = prefix

        if starting_defs is not None:
            self._definitions.extend(starting_defs)

        # run our own preprocessors
        for line in text.splitlines():
            # each preprocessor starts with a prefix
            if line.startswith(self.prefix):
                # check all pre procs both possible aliases and run a corresponding function
                for orig, alias in mappings.items():
                    if line.startswith((self.prefix + orig, self.prefix + alias)):
                        getattr(self, f"_get_{orig}")(line)
                        break

                else:
                    raise ValueError(f"{line!r} is not a pre processor")

            elif not self._ignore_code:
                yield line + "\n"

    def _get_def(self, line: str) -> None:
        # TODO use lexer
        name: str = line.split(" ")[1]  # Get the definition name

        self._definitions.append(name)

    def _get_end(self, line: str) -> None:
        # We will just reset it
        self._ignore_code = False

    def _get_nif(self, line) -> None:
        # TODO: add better support for this stuff
        self._ignore_code = not (line.split(" ")[1] in self._definitions)

    def _get_if(self, line: str) -> None:
        # TODO: add better support for this stuff
        self._ignore_code = line.split(" ")[1] in self._definitions
