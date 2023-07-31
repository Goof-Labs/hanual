from __future__ import annotations

from colorama import init, Fore


def raise_error(trace, error, hint):
    init(autoreset=True)
    print(f"{Fore.RED}{trace}")
    print(f"{Fore.RED}{error}")
    print(f"{Fore.YELLOW}HINT: {hint}")
