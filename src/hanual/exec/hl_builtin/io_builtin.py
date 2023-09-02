from __future__ import annotations

from .base_builtin import hl_builtin, BaseBuiltinLibrary
from hanual.exec.wrappers import LiteralWrapper
from hanual.exec.result import Result
from hanual.exec.scope import Scope
from typing import Dict, Any, Union


class IOBuiltinLibrary(BaseBuiltinLibrary):
    @hl_builtin("x", name="println")
    def hl_println(self, scope: Scope, args: Dict[str, Union[LiteralWrapper, Any]]) -> Result:
        print(args["x"].as_string(scope))
        return Result().success(None)
