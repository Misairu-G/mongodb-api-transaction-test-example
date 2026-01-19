from typing import Optional
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

import app.beanie_patch  # noqa: F401 - patches Document to auto-inject session
from app.models import User

_client: Optional[AsyncIOMotorClient] = None
_db: Optional[AsyncIOMotorDatabase] = None

async def init_db(uri: str, db_name: str) -> None:
    global _client, _db
    _client = AsyncIOMotorClient(uri)
    _db = _client[db_name]
    await init_beanie(database=_db, document_models=[User])

def get_client() -> AsyncIOMotorClient:
    assert _client is not None
    return _client
