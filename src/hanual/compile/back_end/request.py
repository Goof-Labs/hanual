class Request:
    MAKE_CONSTANT = 0
    MAKE_REGISTER = 1

    def __init__(self, *params):
        self.params = params
