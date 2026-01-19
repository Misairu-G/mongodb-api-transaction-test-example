from typing import Optional
from pymongo.client_session import ClientSession
from app.context import get_current_session

async def get_mongo_session() -> Optional[ClientSession]:
    return get_current_session()
