from src.repository.repository import Repository
from src.data_models import User


class UserService:
    def __init__(self, reposotiry: Repository):
        self.repository = reposotiry

    async def get_all(self) -> list[User]:
        return await self.repository.get_all_users()

    async def create(self, user: User):
        return await self.repository.insert_user(user)
