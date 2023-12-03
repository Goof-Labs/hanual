from __future__ import annotations


from typing import Self


# A response is given to the gen
class Response[T]:
    def __init__(self, requests: T) -> None:
        self._response = requests

    @property
    def response(self) -> T:
        return self._response

    @response.setter
    def response(self, val: T) -> None:
        self._response = val
