from __future__ import annotations

from typing import Dict, Iterable, Mapping, Optional, Set, Union, List
from hanual.api.hooks import PreProcessorHook
from io import StringIO


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
            pre_defs: Optional[Iterable[str]] = (),
            prefix: Optional[str] = "@",
            hooks: Optional[Iterable[PreProcessorHook]] = ()
    ) -> None:
        self._hooks: Iterable[PreProcessorHook] = hooks
        self._definitions: Set[str] = set(pre_defs)
        self._ignore_code: bool = False
        self._prefix: str = prefix

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

        self._definitions.add(name)

    def process_hooks(self, text: Union[str, List[str]]):
        if isinstance(text, str):
            text = text.split("\n")

        for hook in self._hooks:
            # same function
            ignore = hook.props.get("skip", ())
            lines = []

            for line in text:
                if line not in ignore:
                    lines.append(line)

            text = hook.scan_lines(lines)

        return text

    def process(
            self,
            text: str,
            prefix: Optional[str] = None,
            starting_defs: Optional[Iterable[str]] = None,
            mappings: Optional[Mapping[str, str]] = None,
    ) -> str:
        if mappings is None:
            mappings = {}

        mappings: Dict[str, str] = {  # TODO: make this modifiable too
            "def": "def",
            "end": "end",
            "nif": "nif",
            "if": "if",
            **mappings,
        }

        if prefix is not None:
            self.prefix = prefix

        if starting_defs is not None:
            [self._definitions.add(n) for n in starting_defs]

        out = StringIO()

        for line in self.process_hooks(text):
            if line.startswith(self.prefix):
                type_ = None

                for pos in mappings.keys():
                    if line.startswith(self.prefix + pos):
                        type_ = pos

                if type_ is None:
                    raise ValueError(f"{line!r} is not a pre processor")

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
