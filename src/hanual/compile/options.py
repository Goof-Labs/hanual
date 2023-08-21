from __future__ import annotations

from dataclasses import dataclass

# from types import


@dataclass(frozen=True)
class CompilerOptions:
    # remove useless stuff
    purge_functions: bool = False
    purge_imports: bool = True

    # pre-compute operations
    precomp_math: bool = True
    precomp_concat: bool = True
    precomp_funcs: bool = False
