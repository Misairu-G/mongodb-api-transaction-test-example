import pytest
from src.users.models import User


@pytest.mark.asyncio
async def test_get_users_non_empty(client, rollback):
    await User(name="alice").insert()
    await User(name="bob").insert()
    r = await client.get("/users")
    assert len(r.json()) == 2


@pytest.mark.asyncio
async def test_rollback(client, rollback):
    r = await client.get("/users/count")
    assert r.json()["count"] == 0
