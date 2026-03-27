from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.repository.migrate import Migration
from src.repository.pg import PG
from src.repository.repository import Repository
from src.service.user import UserService


@asynccontextmanager
async def init_server(app: FastAPI):
    pg = PG(
        {
            "user": "test",
            "password": "test",
            "database": "postgres",
            "host": "localhost",
            "port": 55432,
        }
    )

    await pg.get_pool()
    await Migration(pg, "sql").execute()

    repository = Repository(pg)
    app.state.user_service = UserService(repository)

    yield

    if pg.pool is not None:
        await pg.pool.close()
