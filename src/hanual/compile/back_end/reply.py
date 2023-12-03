from __future__ import annotations


# a reply is from the gen
class Reply[A]:
    def __init__(self, response: A) -> None:
        self._response = response

    @property
    def response(self) -> A:
        return self._response
