from __future__ import annotations

from typing import TYPE_CHECKING

from hanual.lang.nodes.base_node import BaseNode
from hanual.lang.util.type_objects import GENCODE_RET, PREPARE_RET
from hanual.lang.util.node_utils import Intent

if TYPE_CHECKING:
    from hanual.lang.lexer import Token
    from hanual.lang.util.line_range import LineRange


class AlgebraicExpression(BaseNode):
    r"""
    The algebraic expression is similar to a normal binop node; however this node includes an algebraic symbol.
    This node too has a left and right operator.

    ```
    let expression = \x + 1
    ```

    In this example the left node is an algebraic symbol, `\x`, the right operator is `1`, and the operator is
    a `+`. Also note how the left and right values of the operator can also be other expressions.
    """

    __slots__ = (
        "_op",
        "_left",
        "_right",
        "_lines",
        "_line_range",
    )

    def __init__(
        self,
        operator: Token,
        left: AlgebraicExpression | Token,
        right: AlgebraicExpression | Token,
    ) -> None:
        self._op: Token = operator
        self._left = left
        self._right = right

    def gen_code(self, *intents: Intent, **options) -> GENCODE_RET:
        raise NotImplementedError

    def prepare(self) -> PREPARE_RET:
        raise NotImplementedError
