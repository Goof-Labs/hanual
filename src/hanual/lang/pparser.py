from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, Generator, NamedTuple, Optional, Type

from .util.compileable_object import CompilableObject
from .util.proxy import Proxy
from .productions import DefaultProduction

class _StackFrame[T: CompilableObject](NamedTuple):
    name: str
    value: T
    lines: str


class PParser:
    """
    The PParser class is used to create a parser.
    The class is initialized with no params.
    A decorator syntax is then used to create new rules for the parser.
    Finally, parser function is called to parse the input.
    """

    def __init__(self) -> None:
        self.rules: dict[str, tuple[str, Proxy]] = {}
        self._always: list = []
        self.debug = False

    def rule(
        self: PParser,
        *rules,
        prod: Optional[Type] = DefaultProduction,
        types: Optional[dict[str, Any]] = None,
        unless_starts: Optional[list[str]] = None,
        unless_ends: Optional[list[str]] = None,
    ) -> Callable:
        """
        This function is a decorator, so it can be used with the following syntax

        >>> parser = PParser()
        >>> ...
        >>> @parser.rule("rule_1", "rule_2")
        >>> def my_rule(*token_stream):
        >>>     return "whatever I feel like"
        >>> ...

        The types keyword argument is used to show what type of rules we have used,
        this is something usefull because if we have multiple rules defined to point
        to one function, it can get messy tring to figure out which case caused the
        function to be called.

        >>> ...
        >>> @parser.rule("rule_1", "rule_2", "rule_3", types={
        >>>     "rule_1": 1, "rule_2": 2, "rule_3": 3
        >>> })
        >>> def some_rule(*ts, case: int):
        >>>     if case == 1: # do some stuff for the first case
        >>>     elif case == 2: # other stuff for second case
        >>>     elif case == 3: # third case

        The unless kwarg is a dict with two keys `start` and `end`, this means that
        if we find a pattern, but we want to skip over it if and only if the next
        token is a specific value, or a token at the start of the pattern is present.
        Lets say we have a rule [B C] and we want it only to be formed if it is not
        prefixed with an A or the next token would be a D, so if we have the pattern
        [A B C] {next token D} this pattern would not be formed because the pattern is
        next to an A, also because the next token would be a D. Lets say we are making
        a function definition rule, but it conflicts with a function call rule. This is
        because a function call sort of exists within the function definition, e.g.

        FN NAME LPAR RPAR
        END

        The [NAME LPAR RAPR] would be reduced as a function call, but by using an
        unless we can write the following.

        >>> @par.rule("NAME LPAR RPAR", unless={"start": "FN"})
        >>> def function_call(ts):
        >>>     return ...

        This rule will now evaluate [NAME LPAR RPAR] to a function call if and only
        if the pattern is not prefixed with an FN, else it will skip this pattern
        and a different rule can take care of it.
        """

        def inner(func):
            prox = Proxy(func, types, prod, unless_starts, unless_ends)
            # expand all rules, so they have their own individual function associated
            for rule in rules:
                self.rules[rule] = func.__name__, prox

        return inner

    def parse(self: PParser, stream: Generator[CompilableObject, None, None]):
        stack: list[_StackFrame[CompilableObject]] = []

        while True:
            # get next token, default is None
            next_token: CompilableObject | None = next(stream, None)

            # flags
            change: bool = False
            if not (next_token is None):
                change = True

            # reductions
            for pattern, (reducer, proxy) in self.rules.items():
                # pattern is what we need to reduce the stack
                # reducer is what we reduce the pattern to
                # proxy is a wrapper around a function

                pattern_lst: list[str] = pattern.split(" ")

                # compare the stack from top to bottom, so we need to reverse
                stk_coppy: list[_StackFrame[CompilableObject]] = stack.copy()
                stk_coppy.reverse()
                pattern_lst.reverse()

                depth: int = pattern.count(" ")

                # would not zip up nicely
                if depth > len(stack):
                    continue

                # the following two lines are an optimized version of the old for loop
                broke_out: bool = (
                    not list(map(lambda x: x.name, stk_coppy[: depth + 1]))
                    == pattern_lst
                )

                # old method
                # =============================
                # for depth, (left, right) in enumerate(zip(stk_coppy, pattern_lst)):
                #    if left[0] != right:
                #        broke_out = True
                #        break
                # =============================

                # goto next if we broke out
                if broke_out:
                    continue

                # the content of this function needs to know the token but nothing else so this is ok
                if not (next_token is None):
                    # check if next is an unless
                    if next_token.token_type in proxy.unless_end:
                        continue

                # create arguments for proxy

                if stack[len(stack) - 2 - depth].name in proxy.unless_start:
                    continue

                if (next_token is not None) and (
                    next_token.token_type in proxy.unless_end
                ):
                    continue

                p_args: list[_StackFrame[CompilableObject]] = []

                for _ in range(depth + 1):
                    p_args.append(stack.pop())

                # make normal
                p_args.reverse()

                # actually run it
                res: CompilableObject = proxy.call(p_args)

                stack.append(
                    _StackFrame(
                        name=reducer,
                        value=res,
                        lines=res.lines,
                    )
                )

                # there has been a reduction aka change so set a flag to true
                change = True

            if (next_token is None) and (change is False):
                break

            if not (next_token is None):
                stack.append(
                    _StackFrame[CompilableObject](
                        name=next_token.token_type,
                        value=next_token,
                        lines=next_token.lines,
                    )
                )

        return stack
