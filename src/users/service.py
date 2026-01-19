from src.users.models import User


async def create_user(name: str) -> User:
    user = User(name=name)
    await user.insert()
    return user


async def list_users() -> list[User]:
    return await User.find_all().to_list()


async def count_users() -> int:
    return await User.find_all().count()
