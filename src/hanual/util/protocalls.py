from __future__ import annotations

from typing import TypeVar, Generic


T = TypeVar("T")


# a reply is from the gen
class Reply(Generic[T]):
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

    def __init__(self, *params):
        self.params = params


# A response is given to the gen
class Response(Generic[T]):
    def __init__(self, requests: T) -> None:
        self._response = requests

    @property
    def response(self) -> T:
        return self._response

    @response.setter
    def response(self, val: T) -> None:
        self._response = val
