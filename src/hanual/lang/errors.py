from __future__ import annotations

from colorama import init, Fore
from typing import NoReturn
from sys import exit


def iota() -> int:
    iota.i += 1
    return iota.i


iota.i = 0


class Error:
    stage = None
    id = None

    def be_raised(
        self: Error,
        sample_code: str,
        line: int,  # line number
        col: int,
        explain: str,
        stage: str = None,
    ) -> NoReturn:
        init(autoreset=True)

        code = sample_code.strip(" ")

        print(
            f"{Fore.RED}{self.stage if not stage else stage}-ERROR: {type(self).__name__.removeprefix('HNL')}, at line {line}"
        )
        print()
        print(f"{Fore.YELLOW}{'-'*50}")
        print(f"|{str(line).zfill(5)}> {Fore.YELLOW}{code}")
        print(f"^".rjust(col + 8))
        print(f"{Fore.YELLOW}{'-'*50}")
        print()

        print(explain)
        print(f"ERROR CODE : {self.id}")

        exit()


class HNLRuntimeError(Error):
    in_code: bool

    def be_raised(
        self: HNLRuntimeError,
        sample_code: str,
        line: int,
        col: int,
        explain: str,
        stage: str = None,
    ) -> NoReturn:
        super().be_raised(sample_code, line, col, explain, stage)

    def be_raised_runtime(self: HNLRuntimeError, explain: str) -> NoReturn:
        init(autoreset=True)
        print(f"{Fore.RED}{self.stage}-ERROR: {type(self).__name__} , {explain}")
        exit()


class HNLIligalCharacterError(Error):
    id = iota()

    stage = "lexing"

    """
    Overview: The character you used is not recognised by the hanual language, you may have made a typo
    
    ::Details::
    ===========
    
    When a language wants to read your source code the first course of action is tokenizing, this breaks
    the source code down into more digestible tokens. This is a common aproch in programming languages
    this means that if you got this error you have used some character or invalid sequence of characters
    in your source code.
    
    ::Fix this::
    ============
    
    You may want to start removing unicode characters in the code or other unrecognised symbols.
    """


class HNLNameNotFoundError(Error):
    id = iota()

    stage = "compiling"

    """
    Overview: Some name or variable name has not been recognised you may have made a typo in a var name
    
    ::Details::
    ===========
    
    The language is stack based so if the compiler needs to load a name but can't find it in the stack then
    it has probably not found a variable name you have used in your code. This error is raised when that
    happens.
    
    ::Fix this::
    ============
    
    This error has been caused by a name not being found, to fix this you will want to fix the outlined name
    because you may have made a typo.
    """


class HNLFileNotFound(Error):
    id = iota()

    stage = "running"

    """
    Overview: When the program tries to load a dependany that does not exist or read/write to a non existant file.
    
    ::Details::
    
    When the language tries to read a file that does not exist, weather by loading a dependancy or performing
    an I/O operation, this error is raised. This is a safer option then making any assumsions about the contense
    of the file.
    
    ::Fix this::
    
    You may want to check if the file you want to open exists. If you are using an external libruary make sure
    that it is in your system path or in your project directory. Also check for any typoes.
    """
