from __future__ import annotations

from io import StringIO
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing_extensions import Self

    from hanual.lang.util.line_range import LineRange


class Frame:
    __slots__ = (
        "_line_range",
        "_name",
        "_line",
    )

    def __init__(self, name: str, line_range: LineRange, line: str = ""):
        self._line_range = line_range
        self._name = name
        self._line = line

    @property
    def summery(self) -> str:
        tb = StringIO()
        tb.write(f"{self._name}:")
        for line, i in zip(
            self._line.split("\n"),
            range(self._line_range.start, self._line_range.end + 1),
        ):
            tb.write(f" {str(i).zfill(5)} | {line}")
        return tb.getvalue()

    @property
    def name(self) -> str:
        return self._name


class TraceBack:
    def __init__(self):
        self._frames: list[Frame] = []

    def add_frame(self, frame: Frame):
        self._frames.append(frame)
        return self

    def add_frames(self, frames: list[Frame]) -> Self:
        self._frames.extend(frames)
        return self

    @property
    def frames(self):
        return self._frames
