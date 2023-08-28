from __future__ import annotations

import logging

from hanual.compile.h_compile import hl_compile
from hanual.api.load_hooks import HookLoader
from hanual.tools.cli import HanualCli

logging.basicConfig(level=logging.DEBUG)

options = HanualCli().options
hl = HookLoader()

if "compile" in options.loose_args:
    hl_compile()

elif "pack" in options.loose_args:
    ...

else:
    print(f"One of {options.loose_args!r} is not recognised as a mode")
