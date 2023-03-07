class Parser:
    def __init__(self):
        self._rules = {}
        self._stream = []

    def rule(self, *rules):
        """
        This function is a decorator and can be used with the decorator syntax.

        The rules are the cases in wich the function should be used.

        >>> @par.rule("some rule", "another rule")
        """

        def decor(fn):
            self._rules[rules] = fn

        return decor

    def parse(self, stream) -> None:
        self._tree = []
        t_patern = []
        pattern = ""
        self.stream = stream

        self._recursive_parse(t_patern, pattern)

        return self._tree

    def _recursive_parse(self, t_patern, pattern):
        for matches, fn in self._rules.items():
            if pattern.strip() in matches:
                self._tree.append(fn(t_patern))
                pattern = ""
                t_patern = []

        else:
            next_token = next(self.stream, None)
            if not next_token:
                return

            t_patern.append(next_token)
            pattern += " " + next_token.type

        return self._recursive_parse(t_patern, pattern)

