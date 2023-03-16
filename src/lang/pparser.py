from typing import Dict, Callable


class Rule:
    def __init__(self: "Rule", rules, fn) -> None:
        self.rules = []

        rule: str
        for rule in rules:
            s_rule = rule.split(" ")
            s_rule.reverse()
            self.rules.append(s_rule)

        self._fn = fn

    def match(self: "Rule", pattern: list[str]) -> bool:
        p = pattern.copy()
        p.reverse()

        max_deb = 0

        rule: str
        for rule in self.rules:
            debth = 0
            for j, k in zip(p, rule):
                if j != k:
                    break

                debth += 1

            max_deb = debth if debth > max_deb else max_deb

        return max_deb

    def call(self: "Rule", rgs):
        return self._fn(rgs)

    @property
    def name(self: "Rule") -> None:
        return self._fn.__name__


class Parser:
    def __init__(self: "Parser"):
        self._rules = []
        self._stream = []
        self._backup = None

    def rule(self: "Parser", *rules):
        """
        This function is a decorator and can be used with the decorator syntax.

        The rules are the cases in wich the function should be used.

        >>> @par.rule("some rule", "another rule")
        """

        def decor(fn: Callable):
            self._rules.append(Rule(rules, fn))

        return decor

    def parse(self, stream) -> None:
        self._tree = []
        self.stream = stream

        self._parse()

        return self._tree

    def _parse(self):
        pattern = []
        t_patern = []

        while True:
            next_t = next(self.stream, None)

            if not next_t:
                break

            for rule in self._rules:
                deb = rule.match(pattern)

                if not deb > 0:
                    continue

                rgs = []
                for _ in range(deb):
                    rgs.append(t_patern.pop())
                    pattern.pop()

                pattern.append(rule.name)
                t_patern.append(rule.call(rgs))

            else:
                t_patern.append(next_t)
                pattern.append(next_t.type)
