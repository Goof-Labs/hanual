from __future__ import annotations


from hanual.lang.util.line_range import LineRange
from io import StringIO
from sys import exit


class HanualError:
    """Represents an error in the hanual language
    """
    def __init__(self, line_str: str, line_range: LineRange, hint: str="") -> None:
        self.line_str = line_str
        self.line_range = line_range
        self.error_name = type(self).__name__.replace("Hanual", "")
        self.hint = hint
        self.traceback = []

    def display(self):
        print(self)
        exit(1)

    def __str__(self) -> str:
        err = StringIO()
        err.write(("-" * 50) + self.error_name + ("-" * 50) + "\n")

        if self.traceback:
            err.write(("-" * 50) + "TRACEBACK" + ("-" * 50) + "\n")

            for trace in reversed(self.traceback):
                err.write(str(trace))

            err.write(("-" * 50) + "END TRACEBACK" + ("-" * 50) + "\n")
        
        else:
            err.write(("-" * 50) + "NO TRACEBACK" + ("-" * 50) + "\n")

        for line_num, line in zip(
            self.line_range.to_range(),
            self.line_str.splitlines()
        ):
            err.write(f"{str(line_num).zfill(5)} | {line}\n")

        if self.hint:
            err.write("HINT: "+self.hint + "\n")

        err.write(("-" * 50) + "END ERROR" + ("-" * 50) + "\n")

        return err.getvalue()

    def __repr__(self) -> str:
        return str(self)


class HanualSyntaxError(HanualError):
    ...
