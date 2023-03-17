"""
This is a temporary file created to thest parsing
"""

from typing import List, Dict, Tuple, Callable, Generator, NamedTuple, Any, Optional


class PParser:
    """
    The PParser class is used to create a parser.
    The class is initialised with no params. A
    decorator syntax is then used to create new
    rules for the parser. Finally parser function
    is called to parse the input.
    """

    def __init__(self) -> None:
        self.rules: Dict[str, Tuple[str, Callable[..., Any]]] = {}
        self.debug = False

    def tougle_debug_messages(self: "PParser", setting: Optional[bool] = None) -> None:
        """
        This will tougle debug messages on or off.
        The user should explicitly provide what the
        setting should be.
        """

        if setting is None:
            self.debug = not self.debug

        elif not setting is True or not setting is False:
            # Although setting should be a boolean The user
            self.debug = setting

        else:
            self.debug = bool(setting)

    def rule(self, *rules):
        """
        This function is a decorator so it can be used with the following syntax:
        >>> ...
        >>> @parser.parse("rule_1", "rule_2")
        >>> def my_rule(*token_stream):
        >>>     return "whatever I feel like"
        >>> ...
        """

        def inner(func):
            # expand all rules so they have their own individual function asociated
            for rule in rules:
                self.rules[rule] = (func.__name__, func)

        return inner

    def parse(
        self,
        stream: Generator[NamedTuple, None, None],
    ) -> List[str]:
        if self.debug:
            print("__RULES__")
            for rule, (reducer, reducer_fn) in self.rules.items():
                print(rule.ljust(100), " =>", reducer)

            print("__END_RULES__\n")

        tree = []
        stk = []

        while True:
            token = next(stream, None)

            if not token:
                break

            stk.append(token)

            if self.debug:
                print(" ".join(stk).ljust(100), " # pushed new token")

            pattern = stk.copy()
            pattern.reverse()

            for rule, (reducer, reducer_fn) in self.rules.items():
                rule = rule.split(" ")

                rule.reverse()

                max_deb = 0
                for i, (left, right) in enumerate(zip(rule, pattern)):
                    max_deb = i

                    if left != right:
                        break

                else:  # The pattern matched perfectly
                    if self.debug:
                        print(
                            " ".join(stk).ljust(50),
                            " => ",
                            reducer,
                            " # Stack reduction",
                        )

                    tree.append(reducer_fn(*[stk.pop() for _ in range(max_deb + 1)]))
                    # The list comp removes
                    stk.append(reducer)

        return tree
