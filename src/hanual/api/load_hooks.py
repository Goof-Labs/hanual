from __future__ import annotations

from hanual.api.hooks import PreProcessorHook, TokenHook, RuleHook
from typing import List, Tuple, TypeVar
import importlib.util
import logging

_H = TypeVar("_H", PreProcessorHook, TokenHook, RuleHook)


class HookLoader:
    def __init__(self):
        self._pp_hooks: List[PreProcessorHook] = []  # pre-processor hooks
        self._tk_hook: List[TokenHook] = []  # token hooks
        self._rl_hook: List[RuleHook] = []  # rule hooks

    def load_modules(self, files: List[Tuple[str, str]]) -> None:
        for py_path, path in files:
            self.load_module(py_path, path)

    def load_module(self, py_path, path):
        logging.debug(f"Loading module: {py_path!r}")

        spec = importlib.util.spec_from_file_location(py_path, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        assert hasattr(module, "get_hooks"), AttributeError(f"{py_path!r} must have function 'get_hooks'")

        hooks: List[_H] = module.get_hooks()

        for hook in hooks:
            if issubclass(type(hook), PreProcessorHook):
                self._pp_hooks.append(hook)

            elif issubclass(type(hook), TokenHook):
                self._tk_hook.append(hook)

            elif issubclass(type(hook), RuleHook):
                self._rl_hook.append(hook)

            else:
                raise Exception(f"{hook.__name__!r} from {py_path!r} does not inherit from a hook")

    @property
    def preproc(self):
        return self._pp_hooks

    @property
    def tokens(self):
        return self._tk_hook

    @property
    def rules(self):
        return self._rl_hook
