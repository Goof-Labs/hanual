from __future__ import annotations

from typing import TYPE_CHECKING, Generator

from bytecode import Instr, Label

if TYPE_CHECKING:
    from hanual.util.protocalls import Reply, Request, Response
    from hanual.lang.util.node_utils import Intent
    from hanual.util.equal_list import ItemEqualList


type REQUEST_TYPE = int

type GENCODE_RET = Generator[
    Response[Instr] | Response[Label],  # yield
    Reply | None,  # send type
    None,  # return type
]
type PREPARE_RET = Generator[
    Request[object], Reply[object] | None, None  # yield  # send type  # return type
]

type GENCODE_INTENTS = ItemEqualList[Intent]
