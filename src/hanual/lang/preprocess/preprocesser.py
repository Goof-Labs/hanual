from typing import Union, List, Tuple, Dict, TypeVar
from .preproc_lexer import generate_lexer, Lexer
from dataclasses import dataclass, field
from io import TextIOWrapper, StringIO


L = TypeVar("L", bound=Lexer)


@dataclass()
class _MettaData:
    definitions: List[str] = field(default=[])  # definitions
    macros: List[str] = field(default=[])  # any macros we have
    ignore: bool = field(default=False)  # If we are ignoring the code


class PrePeoccesser:
    """
    What is a preproccesser, so pre means before and proccess refers to the compiler, this means that
    the code is put through this class before being lexed and tokenized. This lets us use some magic
    that C and C++ users are farmiliar with. This means that we can conditionally include code. For
    example, we may want to verifiy that the Hanual version is greater then some value this opens the
    doors to lots of backwads compatability. All Preprocessers are, by default, prefixed with an `@`
    but this behaviour can be altered with the config file.
    NOTE all preprocessers are removed after processing so using a `"` is perfectely fine, it wont raise any syntax errors
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
    Macros are replaced at lexing time, these can replace a symbol with another. Lets say we want to
    create a new keyword "contains", that takes a symbol on the left and right, we can create a macro
    mcr "<L> contains <R>" "<R> in <L>", do note that the strings are important in this, we surround
    tokens we want to replace in angel brackets <>
    """

    def __init__(self, file: Union[TextIOWrapper, str, List[str], Tuple[str]]) -> None:
        self._flags: _MettaData = _MettaData()
        self._file: Tuple[str] = ()

        if isinstance(file, str):
            self._file = open(file, "r").readlines()

        elif isinstance(file, list):
            self._file = tuple(file)

        elif isinstance(file, tuple):
            self._file = file

        elif isinstance(file, str):
            self._file = tuple(file.split("\n"))

        else:
            raise TypeError(
                "Expected one of str list[str] tuple[str] got %s",
                (type(file).__name__,),
            )

    def process(self) -> str:
        if not self._file:
            raise ValueError("self._file is falsy")

        prefix: str = "@"
        names: Dict[str, str] = {
            "def": "def",
            "mcr": "mcr",
            "end": "end",
            "if": "if",
        }

        lexer = generate_lexer(prefix, names.keys())

        # This is more suited for what we are doing
        final_code = StringIO()

        for line in self._file:
            # we only want to check the code if it starts with the prefix or we will be looking at quadratic time, not good
            if line.startswith(prefix):

                for k, v in names.items():
                    # The line begins with a preprocesser
                    if line.startswith(prefix + k):
                        getattr(self, f"dispatch_{v}", self.dispatch_default)(
                            line, lexer
                        )

            elif not self._flags.ignore:
                final_code.write(line)

        return final_code.close()

    def dispatch_def(self, line: str, lexer: L) -> None:
        # The definition is only a name that we append onto a list
        stream = tuple(lexer.tokenize(line))

        if stream[1].type != "ID":
            raise TypeError("should be a name got %s", (stream[1].type,))

        self._flags.definitions.append(stream[1].value)

    def dispatch_mcr(self, line: str, lexer: L) -> None:
        ...

    def dispatch_end(self, line: str, lexer: L) -> None:
        ...

    def dispatch_if(self, line: str, lexer: L) -> None:
        ...

    def dispatch_default(self, line: str, lexer: L) -> None:
        ...
