from typing import Optional
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from src.config import MONGO_URI, MONGO_DB
from src.users.models import User

_client: Optional[AsyncIOMotorClient] = None
_db: Optional[AsyncIOMotorDatabase] = None

async def init_db(uri: str = MONGO_URI, db_name: str = MONGO_DB) -> None:
    global _client, _db
    _client = AsyncIOMotorClient(uri)
    _db = _client[db_name]
    await init_beanie(database=_db, document_models=[User])

def get_client() -> AsyncIOMotorClient:
    assert _client is not None
    return _client
