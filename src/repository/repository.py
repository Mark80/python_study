import asyncpg
from src import data_models
from src.repository.pg import PG


class Repository:
    def __init__(self, pg: PG):
        self.pg = pg

    async def insert_user(self, user: data_models.User) -> data_models.User:
        record = await self.pg.execute(
            "INSERT INTO users (name, email) VALUES ($1, $2) RETURNING id, name, email",
            user.name,
            user.email,
        )
        if record is None:
            raise RuntimeError("INSERT INTO users returned no row")
        return data_models.User.from_dict(record)

    async def get_all_users(self) -> list[data_models.User]:
        rows = await self.pg.fetch("SELECT * FROM users")
        return [data_models.User.from_dict(record) for record in rows]
