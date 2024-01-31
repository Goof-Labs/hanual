from __future__ import annotations

import re
from typing import Any, Callable, Optional, Type, overload

from hanual.lang.productions import DefaultProduction
from hanual.lang.util.proxy import HookProxy, Proxy

from .hook import GenericHook


def new_rule(
    name: str,
    *pattern,
    prod: Optional[Type] = DefaultProduction,
    types: Optional[dict[str, Any]] = None,
    unless_starts: Optional[list[str]] = None,
    unless_ends: Optional[list[str]] = None,
) -> Callable[[Type[RuleHook]], Type[RuleHook]]:
    """A class decorator for a RuleHook.

    > This is a decorator used to decorate a RuleHook. The decorator
    > takes in paramiters and sets them as attributes on the RuleHook.
    > The paramiters are verry reminicent of the ones used in the
    > `parser.rule` decorator. Example:
    >
    > @new_rule("some pattern", "pattern two")
    > class MyRule(RuleHook):
    >     pass

    @pattern^tuple[LiteralString]>Patterns that match to the rule
    | The patterns are a string that outlines what pattern the rule
    | matches up to. e.g. "thing1 thing2 thing3", in this case the
    | rule would only be run if there was a pattern on the stack
    | with [rule1 rule2 rule2].
    @prod^Optional[Type]>The production passed to the rule
    | The production is a class that prepresents elements on the
    | stack. For example, a `DefaultProduction` will be passed to
    | the rule by default, however you can use different, or your
    | own productions if you want.
    @unless_starts^Optional[Iterable[LiteralString]]>New tokens that will prevent the rule from running.
    | A list of token types. If the previous token type is listed in the
    | list then the rule will not be run. For example, if we want a
    | rule that simplifies [ A B ] => AB but only if C is not directley
    | before the match e.g. [C A B]. In this example C could be listed
    | in the unless_starts param.
    @unless_ends^Optional[Iterable[LiteralString]]>Tokens at the stack bottom that will prevent the rule from running.
    |
    |
    |
    @types^Optional[Dict[LiteralString, Any]]>The types of matches asociated.
    |
    |
    |
    @name^Optional[str]>Custom name for the rule.
    |
    |
    |
    """

    def decor(cls: Type[RuleHook]):
        cls._proxy = HookProxy(cls, types, prod, unless_starts, unless_ends)
        cls._pattern = pattern
        cls._name = name
        return cls

    return decor


class RuleHook(GenericHook):
    __slots__ = "_proxy", "_pattern", "_name"

    @overload
    def create_rule(self, ts: DefaultProduction, types: dict[str, Any]): ...

    @overload
    def create_rule(self, ts: DefaultProduction): ...

    def create_rule(self, *args, **kwargs):
        raise NotImplementedError

    @property
    def proxy(self) -> Proxy:
        return self._proxy

    @property
    def patterns(self):
        return self._pattern

    @property
    def name(self):
        # SET A NAME, OR YOU WILL FEEL PAIN
        # also if the name is empty, the default if one is not given, then the class name is converted to snake case
        # and that is used. THX to: vvvvvvv
        # <https://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-snake-case>
        return (
            self._name
            or re.sub(r"(?<!^)(?=[A-Z])", "_", self.__class__.__name__).lower()
        )
