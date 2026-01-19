from typing import Optional
from pymongo.client_session import ClientSession
from app.models import User

class UserRepo:
    @staticmethod
    async def create_user(name: str, session: Optional[ClientSession]):
        u = User(name=name)
        await u.insert(session=session)
        return u

    @staticmethod
    async def list_users(session: Optional[ClientSession]):
        return await User.find_all(session=session).to_list()

    @staticmethod
    async def count_users(session: Optional[ClientSession]) -> int:
        return await User.find_all(session=session).count()
