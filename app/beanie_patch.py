"""
Monkey-patch Beanie Document to auto-inject session from context.
Import this module once at startup before using any Document.
"""
import functools
import inspect
from beanie import Document
from app.context import get_current_session

# Methods that accept a 'session' parameter
PATCHED_METHODS = [
    # Instance methods
    "insert",
    "save",
    "replace",
    "delete",
    # Class methods
    "find",
    "find_one",
    "find_all",
    "get",
    "insert_many",
    "delete_all",
    "count",
]

def _wrap_method(original):
    """Wrap a method to auto-inject session from context if not provided."""
    @functools.wraps(original)
    async def wrapper(*args, session=None, **kwargs):
        session = session or get_current_session()
        return await original(*args, session=session, **kwargs)
    return wrapper

def patch_beanie_document():
    """Apply session auto-injection to Document methods."""
    for method_name in PATCHED_METHODS:
        original = getattr(Document, method_name, None)
        if original is None:
            continue
        
        # Skip if already patched
        if getattr(original, "_session_patched", False):
            continue
        
        if isinstance(original, classmethod):
            # Unwrap classmethod, wrap the function, re-wrap as classmethod
            wrapped = _wrap_method(original.__func__)
            wrapped._session_patched = True
            setattr(Document, method_name, classmethod(wrapped))
        elif inspect.iscoroutinefunction(original):
            wrapped = _wrap_method(original)
            wrapped._session_patched = True
            setattr(Document, method_name, wrapped)

# Auto-patch on import
patch_beanie_document()
