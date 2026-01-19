from pydantic import BaseModel


class CreateUserIn(BaseModel):
    name: str


class UserOut(BaseModel):
    id: str
    name: str


class UserCountOut(BaseModel):
    count: int
