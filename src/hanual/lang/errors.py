from __future__ import annotations

from colorama import init, Fore
from sys import exit


class Error:
    def __init__(self: Error) -> None:
        pass

    def be_raised(self: Error, sample_code: str) -> None:
        init(autoreset=True)

        code = sample_code.strip(" ")

        print(f"{Fore.RED}ERROR: {type(self).__name__}")
        print()
        print(f"{Fore.YELLOW}{'-'*len(code)}")
        print(f"{Fore.YELLOW}{code}")
        print(f"{Fore.YELLOW}{'-'*len(code)}")
        print()

        exit()
