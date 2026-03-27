from src.data_models import User
from src.repository.pg import PG


class Repository:
    def __init__(self, pg: PG):
        self.pg = pg

    async def insert_user(self, user: User):
        await self.pg.execute(
            "INSERT INTO users (name, email) VALUES ($1, $2) RETURNING id, name, email",
            user.name,
            user.email,
        )

    async def get_all_users(self) -> list[User]:
        rows = await self.pg.fetch("SELECT * FROM users")
        return [User.from_dict(record) for record in rows]

    async def get_by_id(self, user_id: int) -> User:
        rows = await self.pg.fetch("SELECT * FROM users WHERE id = $1", user_id)
        if not rows:
            raise RuntimeError("User not found")
        return User.from_record(rows[0])
