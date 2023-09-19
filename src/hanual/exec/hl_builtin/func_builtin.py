from __future__ import annotations

from hanual.lang.errors import ErrorType, HanualError, TraceBack
from .base_builtin import hl_builtin, BaseBuiltinLibrary
from hanual.exec.wrappers import LiteralWrapper
from hanual.exec.result import Result
from hanual.exec.scope import Scope
from typing import Dict


class FuncBuiltinLibrary(BaseBuiltinLibrary):
	@hl_builtin("x", name="int")
	def hl_int(self, scope: Scope, args: Dict[str, LiteralWrapper]) -> Result:
		try:
			return Result().success(int(args["x"].value))

		except ValueError:
			return Result().fail(err=HanualError(
				pos=(-1, 0, 0),
				line="",
				name=ErrorType.value_error,
				reason="The value passed to `int` func can't be parsed",
				tb=TraceBack(),
				tip="Validate your inputs",
			))
