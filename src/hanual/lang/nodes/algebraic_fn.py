from __future__ import annotations

from typing import TYPE_CHECKING

from hanual.lang.nodes.algebraic_expr import AlgebraicExpression
from hanual.lang.nodes.base_node import BaseNode
from hanual.lang.util.type_objects import GENCODE_RET, PREPARE_RET
from hanual.lang.util.node_utils import Intent

if TYPE_CHECKING:
    from hanual.lang.util.line_range import LineRange


class AlgebraicFunc(BaseNode):
    r"""
    An Algebraic function is an algebraic operation that has a given name. An algebraic function is defined
    by a variable asinment where the value is an algebraic expression.

    ```
    let add1 = \n + 1
    ```

    The following function is implied to take one aregument "n" and can be invoked with the function call
    notation. The call also returns the value to the caller.

    ```
    add1(5)
    ```

    In the above example the result of the call to `add1` would be 6.
    """

    __slots__ = (
        "_name",
        "_expr",
        "_lines",
        "_line_range",
    )

    def __init__(
        self, name: str, expr: AlgebraicExpression
    ) -> None:
        self._name = name
        self._expr = expr

    def prepare(self) -> PREPARE_RET:
        raise NotImplementedError

    def gen_code(self, *intents: Intent, **options) -> GENCODE_RET:
        raise NotImplementedError
