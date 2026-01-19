from contextvars import ContextVar
from typing import Optional
from pymongo.client_session import ClientSession

_current_session: ContextVar[Optional[ClientSession]] = ContextVar("_current_session", default=None)

def get_current_session() -> Optional[ClientSession]:
    return _current_session.get()

class session_context:
    def __init__(self, session: ClientSession):
        self._session = session
        self._token = None

    async def __aenter__(self):
        self._token = _current_session.set(self._session)
        return self._session

    async def __aexit__(self, exc_type, exc, tb):
        _current_session.reset(self._token)
        return False
