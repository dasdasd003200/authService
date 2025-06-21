# src/core/infrastructure/web/strawberry/base_query.py - SIMPLIFIED VERSION
import asyncio
from typing import TypeVar, Callable, Any
from abc import ABC

T = TypeVar("T")


def handle_async_execution(async_func: Callable, *args, **kwargs) -> Any:
    """Helper to run async functions in sync context"""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    return loop.run_until_complete(async_func(*args, **kwargs))


def safe_execute(func: Callable, default_value: Any = None) -> Any:
    """Safely execute function and return default on error"""
    try:
        return func()
    except Exception:
        return default_value


class BaseQuery(ABC):
    """Base class for all queries with common async handling - Now using functions"""

    # These are now available as module-level functions:
    # - handle_async_execution()
    # - safe_execute()
    pass
