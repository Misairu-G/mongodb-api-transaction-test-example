from typing import Optional
from pymongo.client_session import ClientSession
from src.users.models import User
from src.context import get_current_session


async def create_user(name: str, session: Optional[ClientSession] = None) -> User:
    user = User(name=name)
    await user.insert(session=session)
    return user


async def list_users(session: Optional[ClientSession] = None) -> list[User]:
    session = session or get_current_session()
    return await User.find_all(session=session).to_list()


async def count_users(session: Optional[ClientSession] = None) -> int:
    session = session or get_current_session()
    return await User.find_all(session=session).count()
