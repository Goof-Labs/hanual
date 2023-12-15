from __future__ import annotations


from typing import Self


# a reply is from the gen
class Reply[T]:
    SUCCESS = 0

    def __init__(self, response: T) -> None:
        self._response = response

    @property
    def response(self) -> T:
        return self._response


class Request:
    ADD_CONSTANT = 0
    ADD_NAME = 1
    GET_MEM_LOCATION = 2
    GET_LAST_CONTEXT = 3

    def __init__(self, *params):
        self.params = params
        self._is_lazy: bool = False

    def make_lazy(self) -> Self:
        self._is_lazy = True
        return self

    @property
    def lazy(self) -> bool:
        return self._is_lazy


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
