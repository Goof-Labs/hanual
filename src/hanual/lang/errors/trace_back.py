from __future__ import annotations


class Frame:
    def __init__(self, name: str, line_num: int = None, line: str = None):
        self._line_num = line_num
        self._name = name
        self._line = line

    @property
    def summery(self):
        if self._line_num is None:
            return self._name

        return f"{self._name} {str(self._line_num).zfill(5)} | {self._line}"


class TraceBack:
    def __init__(self):
        self._frames: list[Frame] = []

    def add_frame(self, frame: Frame):
        self._frames.append(frame)
        return self

    @property
    def frames(self):
        return self._frames
