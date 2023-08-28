from __future__ import annotations

from typing import Dict, Generator, Mapping, Optional, Set, Union, List
from hanual.api.hooks import PreProcessorHook


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
            pre_defs: Optional[List[str]] = (),
            prefix: Optional[str] = "@",
            hooks: Optional[List[PreProcessorHook]] = ()
    ) -> None:
        self._hooks: List[PreProcessorHook] = hooks
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

    @staticmethod
    def _skip_lines(text: list[str], ignore: list[str]) -> Generator[str, None, None]:
        for line in text:
            if line in ignore:
                continue

            yield line

    def process_hooks(self, text: Union[str, List[str]]):
        if isinstance(text, str):
            text = text.split("\n")

        for hook in self._hooks:
            # same function
            ignore = hook.props.get("skip", ())

            text = hook.scan_lines(self._skip_lines(text, ignore))

        return text

    def add_hook(self, hook: PreProcessorHook) -> None:
        self._hooks.append(hook)

    def process(
            self,
            text: str,
            prefix: Optional[str] = None,
            starting_defs: Optional[List[str]] = None,
            mappings: Optional[Mapping[str, str]] = None,
    ) -> Generator[str, None, None]:
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

        # run our own preprocessors
        for line in self.process_hooks(text):
            # each preprocessor starts with a prefix
            if line.startswith(self.prefix):

                # check all pre procs both possible aliases and run a corresponding function
                for orig, alias in mappings.items():
                    if line.startswith((self.prefix + orig, self.prefix + alias)):
                        getattr(self, f"get_{orig}")(line)
                        break

                else:
                    raise ValueError(f"{line!r} is not a pre processor")

            elif not self._ignore_code:
                yield line + "\n"

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
