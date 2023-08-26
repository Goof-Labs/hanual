from hanual.api.hooks import RuleHook, new_rule


@new_rule("BNG NUM", name="line")
class UseLessRule(RuleHook):

    def create_rule(self, ts):
        return ["INC", ts[1]]

    def __call__(self, ts):
        return self.create_rule(ts)

def get_hooks():
    return [UseLessRule()]
