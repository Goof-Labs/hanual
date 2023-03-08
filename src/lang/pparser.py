class Parser:
    def __init__(self):
        self._rules = {}
        self._stream = []
        self._backup = None

    def rule(self, *rules, carry: bool = False, allow_jump: bool = False):
        """
        This function is a decorator and can be used with the decorator syntax.

        The rules are the cases in wich the function should be used.

        >>> @par.rule("some rule", "another rule")
        """

        def decor(fn):
            fn._carry = carry
            self._rules[rules] = fn

        return decor

    def parse(self, stream) -> None:
        self._tree = []
        self.stream = stream

        self._parse()

        return self._tree

    def _parse(self):
        pattern = ""
        t_patern = []

        while True:
            for matches, fn in self._rules.items():
                if pattern.strip() in matches:
                    res = fn(t_patern)

                    if fn._carry:
                        pattern = fn.__name__
                        t_patern = [res]

                    else:
                        pattern = ""
                        t_patern = []
                        self._tree.append(res)

            else:
                next_token = next(self.stream, None)

                if not next_token:

                    if pattern: #  if there is still stuff to parse
                        for matches, fn in self._rules.items():
                            if pattern.strip() in matches:
                                res = fn(t_patern)

                            if fn._carry:
                                pattern = fn.__name__
                                t_patern = [res]

                            else:
                                pattern = ""
                                t_patern = []
                                self._tree.append(res)

                    return

                t_patern.append(next_token)
                pattern += " " + next_token.type
