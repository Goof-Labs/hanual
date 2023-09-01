from __future__ import annotations

from .base_builtin import hl_builtin, BaseBuiltinLibrary
from hanual.exec.result import Result
from hanual.exec.scope import Scope
from typing import Dict, Any


class IOBuiltinLibrary(BaseBuiltinLibrary):
    @hl_builtin("x", name="println")
    def hl_println(self, scope: Scope, args: Dict[str, Any]) -> Result:
        print("P:", args["x"])
        return Result().success(None)
