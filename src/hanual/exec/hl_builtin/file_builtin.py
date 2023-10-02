from __future__ import annotations
from typing import Dict

from hanual.exec.hl_builtin.base_builtin import BaseBuiltinLibrary, hl_builtin
from hanual.exec.wrappers.literal import LiteralWrapper
from hanual.exec.wrappers.hl_struct import HlStruct
from hanual.exec.result import Result
from hanual.exec.scope import Scope


class FileBuiltin(BaseBuiltinLibrary):
    @hl_builtin("fp", name="fopen")
    def hl_fopen(self, scope: Scope, args: Dict[str, LiteralWrapper]) -> Result:
        return Result().success(None)
