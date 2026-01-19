from beanie import Document
from pydantic import Field


class User(Document):
    name: str = Field(min_length=1)

    class Settings:
        name = "users"
