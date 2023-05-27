from __future__ import annotations

from typing import (
    List,
    Dict,
    Tuple,
    Generator,
    Any,
    Optional,
    TypeVar,
    Type,
)
from .productions import DefaultProduction
from copy import deepcopy
from .proxy import Proxy
from .lexer import Token
import logging


T = TypeVar("T")


class PParser:
    """
    The PParser class is used to create a parser.
    The class is initialised with no params. A
    decorator syntax is then used to create new
    rules for the parser. Finally, parser function
    is called to parse the input.
    """

    def __init__(self) -> None:
        self.rules: Dict[str, Tuple[str, Proxy]] = {}
        self._always: List = []
        self.debug = False

        logging.basicConfig(level=logging.DEBUG)

    def toggle_debug_messages(self: PParser, setting: Optional[bool] = None) -> None:
        """
        This will toggle debug messages on or off.
        The user should explicitly provide what the
        setting should be.
        """

        if setting is None:
            self.debug = not self.debug

        elif setting is False or setting is True:
            self.debug = setting

        else:
            self.debug = bool(setting)

    def check_redundancy(self: PParser) -> None:
        """
        This function checks for redundancy. It
        will warn the user about any tokens not
        used, this can be used to keep the
        codebase clean.
        """
        def_tokens = []  # tokens defined by the user
        use_tokens = []  # tokens actually used

        for token in self.rules:
            def_tokens.extend(token.split(" "))

        for rule in self.rules:
            use_tokens.extend(rule.split(" "))

        unused_tokens = set(use_tokens) - set(def_tokens)
        undef_tokens = set(def_tokens) - set(use_tokens)
        remainder = []
        remainder.extend(undef_tokens)
        remainder.extend(unused_tokens)

        if not set(remainder):
            logging.debug("No clashes found :)")

        elif unused_tokens and undef_tokens:
            logging.warning("unused tokens: %s", unused_tokens)
            logging.critical("undefined tokens: %s", undef_tokens)

    def rule(
        self: PParser,
        *rules,
        prod: Optional[Type] = DefaultProduction,
        types: Optional[Dict[str, T]] = None,
        unless_starts: Optional[str] = None,
        unless_ends: Optional[str] = None,
    ):
        """
        This function is a decorator, so it can be used with the following syntax:

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

        The unless kwarg is a dict with two keys `start` and `end` this means that
        if we find a pattern, but we want to skip over it if and only if the next
        token is a specific value, or a token at the start of the pattern is preasent.
        Lets say we have a rule [B C] and we want it only to be formed if it is not
        prefixed with an A or the next token would be a D, so if we have the pattern
        [A B C] {next token D} this pattern would not be formed because the pattern is
        next to an A, also because the next token would be a D. Lets say we are making
        a function definition rule, but it conflicts with a function call rule. This is
        because a function call sort of exists within the function definition e.g.

        FN NAME LPAR RPAR
        END

        The [NAME LPAR RAPR] would be reduced as a function call, but by using an
        unless we can write the following.

        >>> @par.rule("NAME LPAR RPAR", unless={"start": "FN"})
        >>> def function_call(ts):
        >>>     return ...

        This rule will now evaluate [NAME LPAR RPAR] to a function call if and only
        if the pattern is not prefixed with a FN, else it will skip this pattern
        and a different rule can take care of it.
        """

        def inner(func):
            prox = Proxy(func, types, prod, unless_starts, unless_ends)
            # expand all rules, so they have their own individual function associated
            for rule in rules:
                self.rules[rule] = func.__name__, prox

        return inner

    def always(self: PParser):
        """
        This will always run on each reduction of the stack or after every check.
        This is verry usefull when you want to change the tokens while the code is
        represented as a partial tree or stream of rokens.

        WARNING: this can really mess up the stack if you are not carefull so be carefull
        """

        def inner(func):
            self._always.append(func)

        return inner

    ######################
    # PARSING THE TOKENS #
    ######################

    def parse(self: PParser, stream: Generator[Token, None, None]) -> List[Any]:
        change = True
        stack = []

        while True:
            # get next token, default is None
            next_token: Token = next(stream, None)

            # flags
            change = False
            if not (next_token is None):
                change = True

            # reductions
            for pattern, (reducer, proxy) in self.rules.items():
                # pattern is what we need to reduce the stack
                # reducer is what we reduce the pattern to
                # proxy is a wrapper around a function

                pattern_lst = pattern.split(" ")

                # compare the stack from top to bottom so we need to reverse
                stk_coppy = deepcopy(stack)
                stk_coppy.reverse()

                pattern_lst.reverse()

                # would not zip up nicely
                if len(pattern_lst) > len(stk_coppy):
                    continue

                # compare
                broke_out = False

                for debth, (left, right) in enumerate(zip(stk_coppy, pattern_lst)):
                    if left[0] != right:
                        broke_out = True
                        break

                # goto next if we broke out
                if broke_out:
                    continue

                # the contense of this function need to know the token but nothing else so this is ok
                if not next_token is None:
                    # check if next is an unless
                    if next_token.type in proxy.unless_end:
                        continue

                # create arguments for proxy
                p_args = []

                for _ in range(debth + 1):
                    p_args.append(stack.pop()[1])

                # make normal
                pattern_lst.reverse()
                p_args.reverse()

                # actually run it
                res = proxy.call(p_args, pattern_lst)
                stack.append((reducer, res))

                # there has be a reduction aka change so set flag to true
                change = True

            if (next_token is None) and (change is False):
                break

            if not (next_token is None):
                stack.append((next_token.type, next_token))

        return stack
