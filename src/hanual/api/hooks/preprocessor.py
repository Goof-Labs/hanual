from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Callable, Generator, LiteralString

from hanual.api.hooks import GenericHook


def new_preprocessor(
    skip: list[LiteralString],
) -> Callable[[PreProcessorHook], PreProcessorHook]:
    """A decorator to define a new preprocessor Hook

    > This is a class decorator that needs to be used to define a
    > new preprocessor hook. For example,
    >
    > ```py
    > @new_preprocessor(skip=["@", "!", "banana"])
    > class MyPreprocessor(PreProcessorHook):
    >     pass
    > ```

    @skip^list[LiteralString]>A list of characters the preprocessor will skip over.
    | The preprocessor will iterate over every line in some code. If the line starts
    | with one of the elements in `skip`, the line will be skipped.
    """

    # TODO: add `only_on`

    def decor(cls: PreProcessorHook) -> PreProcessorHook:
        cls._skip = skip
        return cls

    return decor


class PreProcessorHook(GenericHook, ABC):
    """A base Class for all preprocessor hooks

    > This class is the base class for all PreProcessorHooks. This class
    > requires one method to be implemented, `scan_lines`. The Hook also
    > has a `skip` property.
    """

    __slots__ = ("_skip",)

    @abstractmethod
    def scan_lines(
        self, lines: Generator[str, None, None]
    ) -> Generator[str, None, None]:
        """A function that yields lines of code.

        > This function takes in the lines of the python file as a generator,
        > and yields lines of code. An example use case would be:
        >
        > ``` py
        > def scan_lines(self, lines):
        >     for line in lines:
        >         if "lol" in line:
        >             continue
        >
        >         yield line
        > ```
        >
        > The above example would only yeild lines without the term "lol" in
        > them. This means that all lines containing "lol" will not be included
        > in the lexed and parsed code.

        @lines^Generator[str, None, None]>The lines of source code to preprocess.
        | The function is fed the lines of source code as a generator.
        @return^Generator[str, None, None]>The function should be a gen
        | The gen should yield all lines or modified lines that it wants to be
        | lexed or parsed.
        """
        raise NotImplementedError

    @property
    def skip(self) -> list[LiteralString]:
        """A list of strings the preprocessor will step over

        > This property tells the preprocessor what lines to skip over.
        > The preprocessor will digest/process all
        """
        return self._skip
