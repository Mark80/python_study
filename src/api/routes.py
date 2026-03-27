from fastapi import FastAPI
from pydantic import BaseModel

from src.data_models import User
from src.api.lifespan import init_server


class CreateUserRequest(BaseModel):
    name: str
    email: str


app = FastAPI(lifespan=init_server)


class Routes:
    def __init__(self, app: FastAPI):
        self.app = app
        self.register_routes()

    def register_routes(self):

        @self.app.get("/users")
        async def get_all_users():
            return await self.app.state.user_service.get_all()

        @self.app.post("/users")
        async def create_user(payload: CreateUserRequest):
            return await self.app.state.user_service.create(
                User(id=0, name=payload.name, email=payload.email)
            )


Routes(app)
