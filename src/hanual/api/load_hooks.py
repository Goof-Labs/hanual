from __future__ import annotations

import importlib.util
import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hanual.api.hooks import PreProcessorHook, RuleHook, TokenHook


class HookLoader[P: PreProcessorHook, T: TokenHook, R: RuleHook]:
    def __init__(self):
        self._pp_hooks: list[P] = []  # pre-processor hooks
        self._tk_hook: list[T] = []  # token hooks
        self._rl_hook: list[R] = []  # rule hooks

    def load_modules(self, files: list[tuple[str, str]]) -> None:
        for py_path, path in files:
            self.load_module(py_path, path)

    def load_module(self, py_path, path):
        from hanual.api.hooks import PreProcessorHook, RuleHook, TokenHook

        logging.debug(f"Loading module: {py_path!r}")

        spec = importlib.util.spec_from_file_location(py_path, path)

        if spec is None:
            raise Exception(f"spec is None")

        if spec.loader is None:
            raise Exception(f"spec.loader is None")

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        assert hasattr(module, "get_hooks"), AttributeError(
            f"{py_path!r} must have function 'get_hooks'"
        )

        hooks: list = module.get_hooks()

        for hook in hooks:
            if issubclass(type(hook), PreProcessorHook):
                self._pp_hooks.append(hook)

            elif issubclass(type(hook), TokenHook):
                self._tk_hook.append(hook)

            elif issubclass(type(hook), RuleHook):
                self._rl_hook.append(hook)

            else:
                raise Exception(
                    f"{type(hook).__name__!r} from {py_path!r} does not inherit from a hook"
                )

    @property
    def preproc(self) -> list[P]:
        return self._pp_hooks

    @property
    def tokens(self) -> list[T]:
        return self._tk_hook

    @property
    def rules(self) -> list[R]:
        return self._rl_hook
