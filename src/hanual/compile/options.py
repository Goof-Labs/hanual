from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CompilerOptions:
    # required stuff
    files: tuple[str] = ()
    out: tuple[str] = ()

    # injection
    inject: tuple[str] = ()

    # remove useless stuff
    purge_functions: bool = False
    purge_imports: bool = True

    # pre-compute operations
    precomp_math: bool = True
    precomp_concat: bool = True
    precomp_funcs: bool = False

    # misc
    loose_args: tuple[str] = ()
