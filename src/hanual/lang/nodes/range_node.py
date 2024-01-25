from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Self
from bytecode import Instr
from hanual.lang.util.type_objects import GENCODE_RET, PREPARE_RET, GENCODE_INTENTS
from hanual.lang.lexer import Token
from hanual.util.protocalls import Response
from .base_node import BaseNode

if TYPE_CHECKING:
    pass


class RangeNode(BaseNode):
    __slots__ = (
        "_from",
        "_to",
        "_lines",
        "_line_range",
    )

    def __init__(
        self: Self,
        start: Optional[Token] = None,
        end: Optional[Token] = None,
    ) -> None:
        self._start = start
        self._end = end

    @property
    def start(self) -> Token | None:
        return self._start

    @property
    def end(self) -> Token | None:
        return self._end

    def gen_code(self, intents: GENCODE_INTENTS, **options) -> GENCODE_RET:
        yield Response(Instr("PUSH_NULL"))
        yield Response(Instr("LOAD_NAME", "range"))

        match self._start, self._end:
            case None, None:
                raise NotImplementedError

            case None, Token():
                raise NotImplementedError

            case Token(), None:
                raise NotImplementedError

            case Token(), Token():
                yield from self._start.gen_code(self.CAPTURE_RESULT)
                yield from self._end.gen_code(self.CAPTURE_RESULT)

            case _:
                raise NotImplementedError

        yield Response(Instr("CALL", 2))
        yield Response(Instr("GET_ITER"))

    def prepare(self) -> PREPARE_RET:
        if self._start is not None:
            yield from self._start.prepare()

        if self._end is not None:
            yield from self._end.prepare()
