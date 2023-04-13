from __future__ import annotations

from colorama import init, Fore
from sys import exit


class Error:
    def be_raised(
        self: Error, stage: str, sample_code: str, line: int, col: int, explain: str
    ) -> None:
        init(autoreset=True)

        code = sample_code.strip(" ")

        print(f"{Fore.RED}{stage}-ERROR: {type(self).__name__}, at line {line}")
        print()
        print(f"{Fore.YELLOW}{'-'*50}")
        print(f"|{str(line).zfill(5)}> {Fore.YELLOW}{code}")
        print(f"^".rjust(col + 9))
        print(f"{Fore.YELLOW}{'-'*50}")
        print()

        print(explain)

        exit()


class IligalCharacterError(Error):
    ...
