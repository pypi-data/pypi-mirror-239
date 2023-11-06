import os
from typing import Any, Optional, Union, Callable, List


class ImposeType:
    def transform(self, arg) -> Any:
        pass


def _replace_args(func: Callable, *args: list, **kwargs: dict):
    print(func.__name__)
    return args, kwargs


def impose(xengines: Optional[Union[str, List[str]]] = None, shortcut: Optional[str] = None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if os.environ.get("IMPOSE_CLI_CONTEXT", False):
                args, kwargs = _replace_args(func, *args, **kwargs)
            return func(*args, **kwargs)
        return wrapper
    return decorator
