from fastapi import APIRouter

from src.users import service
from src.users.schemas import CreateUserIn, UserOut, UserCountOut

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserOut)
async def create_user(payload: CreateUserIn):
    user = await service.create_user(payload.name)
    return UserOut(id=str(user.id), name=user.name)


@router.get("", response_model=list[UserOut])
async def list_users():
    users = await service.list_users()
    return [UserOut(id=str(u.id), name=u.name) for u in users]


@router.get("/count", response_model=UserCountOut)
async def count_users():
    count = await service.count_users()
    return UserCountOut(count=count)
