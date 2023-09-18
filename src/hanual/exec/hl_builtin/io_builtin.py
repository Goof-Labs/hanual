from __future__ import annotations

from hanual.lang.errors import ErrorType, HanualError, TraceBack
from .base_builtin import hl_builtin, BaseBuiltinLibrary
from hanual.exec.wrappers import LiteralWrapper
from hanual.exec.result import Result
from hanual.exec.scope import Scope
from typing import Dict, Any, Union


class IOBuiltinLibrary(BaseBuiltinLibrary):
    @hl_builtin("x", name="println")
    def hl_println(self, scope: Scope, args: Dict[str, LiteralWrapper]) -> Result:
        print(args["x"].to_str(scope, args))
        return Result().success(None)

    @hl_builtin("prompt", name="input")
    def hl_input(self, scope: Scope, args: Dict[str, LiteralWrapper]):
        res = Result()

        try:
            inp = input(args["prompt"].to_str(scope, None))

        except KeyboardInterrupt:
            return res.fail(err=HanualError(
                pos=(-1, 0, 0),
                line="",
                name=ErrorType.keyboard_interupt,
                reason="The user pressed ^C (Ctrl+C)",
                tb=TraceBack()
            ))

        return res.success(LiteralWrapper[str](inp))
