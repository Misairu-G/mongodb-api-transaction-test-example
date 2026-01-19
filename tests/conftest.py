import os
from contextlib import asynccontextmanager
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from pymongo.read_concern import ReadConcern
from pymongo.write_concern import WriteConcern
from pymongo.read_preferences import ReadPreference
from app.context import session_context
from app.db import get_client, init_db
from app.main import app

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/?replicaSet=rs0")
MONGO_DB = os.getenv("MONGO_DB", "test_db")

@pytest_asyncio.fixture(scope="session", autouse=True)
async def _init_beanie_once():
    await init_db(MONGO_URI, MONGO_DB)

@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c

@asynccontextmanager
async def rollback_session():
    client = get_client()
    async with await client.start_session() as session:
        session.start_transaction(
            read_concern=ReadConcern("snapshot"),
            write_concern=WriteConcern("majority"),
            read_preference=ReadPreference.PRIMARY,
        )
        async with session_context(session):
            try:
                yield session
            finally:
                await session.abort_transaction()
