from hanual.api.hooks import TokenHook, new_token
from hanual.lang.lexer import rx


@new_token(
    name="BNG",
    regex=rx(r"\!")
)
class ExclamationMark(TokenHook):
    ...


def get_hooks():
    return [ExclamationMark()]
