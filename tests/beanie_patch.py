"""Test-only monkey-patch for Beanie Document session injection.

This is intentionally located under `tests/` so production code does not
implicitly depend on session propagation logic.

Import this module once (e.g. from `tests/conftest.py`) before exercising
Beanie Document methods.
"""

import functools
import inspect

from beanie import Document

from src.context import get_current_session


# Async methods that accept a `session` parameter
ASYNC_METHODS = [
    # Instance methods
    "insert",
    "save",
    "replace",
    "delete",
    # Class methods
    "find_one",
    "get",
    "insert_many",
    "delete_all",
]

# Sync methods that return query builders (session passed to find, propagates to to_list/count)
SYNC_QUERY_METHODS = [
    "find",
    "find_all",
]


def _wrap_async_method(original):
    @functools.wraps(original)
    async def wrapper(*args, session=None, **kwargs):
        session = session or get_current_session()
        return await original(*args, session=session, **kwargs)

    return wrapper


def _wrap_sync_classmethod(original):
    @functools.wraps(original)
    def wrapper(cls, *args, session=None, **kwargs):
        session = session or get_current_session()
        return original.__func__(cls, *args, session=session, **kwargs)

    return classmethod(wrapper)


def patch_beanie_document() -> None:
    # Patch async methods
    for method_name in ASYNC_METHODS:
        original = getattr(Document, method_name, None)
        if original is None:
            continue
        if getattr(original, "_session_patched", False):
            continue

        if isinstance(original, classmethod):
            wrapped = _wrap_async_method(original.__func__)
            wrapped._session_patched = True
            setattr(Document, method_name, classmethod(wrapped))
        elif inspect.iscoroutinefunction(original):
            wrapped = _wrap_async_method(original)
            wrapped._session_patched = True
            setattr(Document, method_name, wrapped)

    # Patch sync query builder methods (classmethods)
    for method_name in SYNC_QUERY_METHODS:
        original = getattr(Document, method_name, None)
        if original is None:
            continue
        if getattr(original, "_session_patched", False):
            continue

        wrapped = _wrap_sync_classmethod(original)
        wrapped._session_patched = True
        setattr(Document, method_name, wrapped)


# Auto-patch on import
patch_beanie_document()
