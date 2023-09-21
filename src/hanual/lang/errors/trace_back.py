from __future__ import annotations


from typing import TYPE_CHECKING, List


if TYPE_CHECKING:
    from typing_extensions import Self


class Frame:
    __slots__ = "_line_num", "_name", "_line",

    def __init__(self, name: str, line_num: int=-1, line: str=""):
        self._line_num = line_num
        self._name = name
        self._line = line

    @property
    def summery(self):
        if self._line_num is None:
            return self._name

        return f"{self._name} {str(self._line_num).zfill(5)} | {self._line}"

    @property
    def name(self) -> str:
        return self._name


class TraceBack:
    def __init__(self):
        self._frames: list[Frame] = []

    def add_frame(self, frame: Frame):
        self._frames.append(frame)
        return self

    def add_frames(self, frames: List[Frame]) -> Self:
        self._frames.extend(frames)
        return self

    @property
    def frames(self):
        return self._frames
