from __future__ import annotations

from typing import TYPE_CHECKING, Generator, Optional

from bytecode import Instr, Label

if TYPE_CHECKING:
    from hanual.util.protocalls import Reply, Request, Response

type REQUEST_TYPE = int

type GENCODE_RET = Generator[
    Response[Instr] | Response[Label] | Request[REQUEST_TYPE],  # yield
    Optional[Reply],  # send type
    None  # return type
]
type PREPARE_RET = Generator[
    Request[object],  # yield
    Reply[object] | None,  # send type
    None  # return type
]
