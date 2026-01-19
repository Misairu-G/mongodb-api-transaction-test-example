# MongoDB Transaction Test Example

Demonstrates transaction rollback for isolated testing with FastAPI + Beanie + MongoDB.

## Quick Start

```bash
# Start MongoDB (replica set auto-initialized)
docker compose up -d mongo

# Run tests
MONGO_URI="mongodb://localhost:27017/?replicaSet=rs0" MONGO_DB="myapp" pytest -v

# Run full stack (app + mongo)
docker compose up -d
```

## Project Structure

```
src/
├── config.py           # Environment variables
├── database.py         # MongoDB connection
├── context.py          # Session context (ContextVar)
├── beanie_patch.py     # Auto-inject session into Beanie methods
├── dependencies.py     # FastAPI dependencies
├── main.py             # FastAPI app
└── users/
    ├── models.py       # Beanie Document models
    ├── schemas.py      # Pydantic schemas
    ├── service.py      # Business logic
    └── router.py       # API endpoints
tests/
├── conftest.py         # Test fixtures with rollback_session
└── test_users.py       # Tests
```
