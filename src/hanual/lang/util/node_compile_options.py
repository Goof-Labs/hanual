from __future__ import annotations


from typing import TypedDict, Unpack, NotRequired, TypeAlias

from bytecode import Label


class IfStatementCompArgs(TypedDict):
    end_jump: NotRequired[Label]
    true_jump: NotRequired[Label]


IF_STATEMENT_KWARGS: TypeAlias = Unpack[IfStatementCompArgs]
