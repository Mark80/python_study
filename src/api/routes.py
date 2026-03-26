from contextlib import asynccontextmanager
from fastapi import FastAPI
from pydantic import BaseModel

from src.data_models import User
from src.repository.migrate import Migration
from src.repository.repository import Repository
from src.repository.pg import PG


@asynccontextmanager
async def init(app: FastAPI):
    pg = PG(
        {
            "user": "test",
            "password": "test",
            "database": "postgres",
            "host": "localhost",
            "port": 55432,
        }
    )

    await Migration(pg, "sql").execute()

    app.state.repository = Repository(pg)
    Routes(app, app.state.repository)

    yield


class CreateUserRequest(BaseModel):
    name: str
    email: str


app = FastAPI(lifespan=init)


class Routes:
    def __init__(self, app: FastAPI, repository: Repository):
        self.app = app
        self.repository = repository
        self.register_routes()

    def register_routes(self):

        @self.app.get("/users")
        async def get_all_users():
            users = await self.repository.get_all_users()
            return users

        @self.app.post("/users")
        async def create_user(payload: CreateUserRequest):
            return await self.repository.insert_user(
                User(id=0, name=payload.name, email=payload.email)
            )
