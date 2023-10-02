from __future__ import annotations

from hanual.lang.errors import ErrorType, HanualError, TraceBack
from .base_builtin import hl_builtin, BaseBuiltinLibrary
from hanual.lang.errors.trace_back import Frame
from hanual.exec.wrappers import LiteralWrapper
from hanual.exec.result import Result
from hanual.lang.lexer import Token
from hanual.exec.scope import Scope
from typing import Dict, Any, Union


class IOBuiltinLibrary(BaseBuiltinLibrary):
    @hl_builtin("x", name="println")
    def hl_println(self, scope: Scope, args: Dict[str, LiteralWrapper]) -> Result:
        res = Result()

        if isinstance(args["x"], Token):
            if args["x"].type == "ID":
                val, err = res.inherit_from(scope.get(str(args["x"].value), res=True))

                if err:
                    return res

                print(val)

                return res.success(None)

            elif isinstance(args["x"].value, LiteralWrapper):
                print(args["x"].value.to_str())

                return res.success(None)

            else:
                raise NotADirectoryError

        else:
            print(args["x"].to_str(scope, args))
            return res.success(None)

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
