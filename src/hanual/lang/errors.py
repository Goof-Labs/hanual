from __future__ import annotations

from colorama import init, Fore
from sys import exit


def iota():
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
    ) -> None:
        init(autoreset=True)

        code = sample_code.strip(" ")

        print(
            f"{Fore.RED}{self.stage if not stage else stage}-ERROR: {type(self).__name__}, at line {line}"
        )
        print()
        print(f"{Fore.YELLOW}{'-'*50}")
        print(f"|{str(line).zfill(5)}> {Fore.YELLOW}{code}")
        print(f"^".rjust(col + 9))
        print(f"{Fore.YELLOW}{'-'*50}")
        print()

        print(explain)
        print(f"ERROR CODE : {self.id}")

        exit()


class IligalCharacterError(Error):
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


class NameNotFoundError(Error):
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
