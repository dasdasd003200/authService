# src/core/infrastructure/web/strawberry/decorators.py
import functools
from typing import Callable, Any


def async_to_sync(func: Callable) -> Callable:
    """Decorator to convert async functions to sync for Strawberry"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        import asyncio

        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        return loop.run_until_complete(func(*args, **kwargs))

    return wrapper


def safe_resolver(default_value: Any = None):
    """Decorator to safely handle resolver errors"""

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception:
                return default_value

        return wrapper

    return decorator
