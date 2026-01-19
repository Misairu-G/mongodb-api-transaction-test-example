from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import Optional
from pymongo.client_session import ClientSession
from app.deps import get_mongo_session
from app.repo import UserRepo

app = FastAPI()

class CreateUserIn(BaseModel):
    name: str

@app.post("/users")
async def create_user(payload: CreateUserIn, session: Optional[ClientSession] = Depends(get_mongo_session)):
    u = await UserRepo.create_user(payload.name, session)
    return {"id": str(u.id), "name": u.name}

@app.get("/users")
async def list_users(session: Optional[ClientSession] = Depends(get_mongo_session)):
    users = await UserRepo.list_users(session)
    return [{"id": str(u.id), "name": u.name} for u in users]

@app.get("/users/count")
async def count_users(session: Optional[ClientSession] = Depends(get_mongo_session)):
    return {"count": await UserRepo.count_users(session)}
