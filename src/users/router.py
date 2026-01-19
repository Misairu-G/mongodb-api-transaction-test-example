from typing import Optional
from fastapi import APIRouter, Depends
from pymongo.client_session import ClientSession

from src.dependencies import get_mongo_session
from src.users import service
from src.users.schemas import CreateUserIn, UserOut, UserCountOut

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserOut)
async def create_user(
    payload: CreateUserIn,
    session: Optional[ClientSession] = Depends(get_mongo_session),
):
    user = await service.create_user(payload.name, session)
    return UserOut(id=str(user.id), name=user.name)


@router.get("", response_model=list[UserOut])
async def list_users(
    session: Optional[ClientSession] = Depends(get_mongo_session),
):
    users = await service.list_users(session)
    return [UserOut(id=str(u.id), name=u.name) for u in users]


@router.get("/count", response_model=UserCountOut)
async def count_users(
    session: Optional[ClientSession] = Depends(get_mongo_session),
):
    count = await service.count_users(session)
    return UserCountOut(count=count)
