from __future__ import annotations


class Frame:
    def __init__(self, origin: str):
        self._summery = origin

    @property
    def summery(self):
        return self._summery


class TraceBack:
    def __init__(self):
        self._frames = []

    def add_frame(self, frame: Frame):
        self._frames.append(frame)
        return self

    @property
    def frames(self):
        return self._frames
