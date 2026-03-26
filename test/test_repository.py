import pytest
import pytest_asyncio

from src.data_models import User
from src.repository.repository import Repository
from src.repository.migrate import Migration
from src.repository.pg import PG


@pytest_asyncio.fixture
async def connection():
    cfg = {
        "user": "test",
        "password": "test",
        "database": "postgres",
        "host": "localhost",
        "port": 55432,
    }

    pg = PG(cfg)

    migration = Migration(pg, "sql")
    await migration.execute()
    try:
        yield pg
    finally:
        await pg.execute("TRUNCATE TABLE users RESTART IDENTITY CASCADE;")


@pytest.mark.asyncio
async def test_get_all_users(connection):

    repository = Repository(connection)
    user = User(id=0, name="John Doe", email="email@example.com")
    await repository.insert_user(user)
    users = await repository.get_all_users()

    assert len(users) == 1
    assert users[0].name == "John Doe"
    assert users[0].email == "email@example.com"
