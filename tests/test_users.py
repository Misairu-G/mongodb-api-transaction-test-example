import pytest
from src.users.models import User


def user_json(user: User) -> dict:
    """Convert User document to expected API response JSON."""
    return {"id": str(user.id), **user.model_dump(exclude={"id", "created_at", "updated_at"})}


@pytest.mark.asyncio
async def test_get_users_non_empty(client, rollback):
    alice = await User(name="alice").insert()
    bob = await User(name="bob").insert()
    response = await client.get("/users")

    assert response.status_code == 200
    assert response.json() == [user_json(alice), user_json(bob)]


@pytest.mark.asyncio
async def test_rollback(client, rollback):
    # Create within the rollback transaction
    temp_user = await User(name="temp").insert()

    # Within the same transaction/session context, it should be visible
    response = await client.get("/users")
    assert response.status_code == 200
    assert response.json() == [user_json(temp_user)]


@pytest.mark.asyncio
async def test_rollback_does_not_persist_between_tests(client):
    # This test does not use the rollback fixture, so it observes the committed state.
    # The previous test's insert should have been aborted.
    response = await client.get("/users")
    assert response.status_code == 200
    assert response.json() == []
