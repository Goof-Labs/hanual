from __future__ import annotations

from dataclass import dataclass
from typing import Tuple, List, TYPE_HINTING


if TYPE_HINTING:
    from hanual.jit.constant import Constant
    from hanual.jit.instruction import Instruction


@dataclass
class FileFormat:
    magic: Tuple[byte, byte, byte]
    hash: str
    major: int
    minor: int
    micro: int
    file_deps: List[str]
    fn_table: Dict[str, int]
    constant_pool: List[Constant]
    instructions: List[Instruction]

