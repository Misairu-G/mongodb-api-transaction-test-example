from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.database import init_db, _client
from src.users.router import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Skip init if already initialized (e.g., by tests)
    if _client is None:
        await init_db()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(users_router)
