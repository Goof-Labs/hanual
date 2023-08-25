from hanual.api.hook import PreProcessorHook, props
from typing import List, Generator


@props(skip=[""])
class MyPreProc(PreProcessorHook):
    def scan_lines(self, lines: List[str]) -> Generator[str, None, None]:
        for line in lines:
            if line[0] == ".":
                continue

            yield line


def get_hooks():
    return [MyPreProc()]
