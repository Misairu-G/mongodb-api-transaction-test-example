import sys
from pathlib import Path

import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from pymongo.read_concern import ReadConcern
from pymongo.write_concern import WriteConcern
from pymongo.read_preferences import ReadPreference
from src.context import session_context
from src.database import get_client, init_db
from src.config import MONGO_URI, MONGO_DB
from src.main import app

_TESTS_DIR = Path(__file__).resolve().parent
if str(_TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(_TESTS_DIR))

import beanie_patch  # noqa: F401 - test-only: patches Document to auto-inject session

TEST_DB = f"test_{MONGO_DB}"

@pytest_asyncio.fixture(scope="session", autouse=True)
async def _init_beanie_once():
    await init_db(MONGO_URI, TEST_DB)

@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c

@pytest_asyncio.fixture
async def rollback():
    """Wraps test in a transaction that rolls back after completion."""
    mongo_client = get_client()
    async with await mongo_client.start_session() as session:
        session.start_transaction(
            read_concern=ReadConcern("snapshot"),
            write_concern=WriteConcern("majority"),
            read_preference=ReadPreference.PRIMARY,
        )
        async with session_context(session):
            try:
                yield
            finally:
                await session.abort_transaction()
