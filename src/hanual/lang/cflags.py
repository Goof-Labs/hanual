# COMPILER FLAGS
from __future__ import annotations

from typing import NamedTuple, List


class CompilerFlags(NamedTuple):
    warn_kwords: List[str]  # warn if we are still using shout
