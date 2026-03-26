import asyncpg
from contextlib import asynccontextmanager


@asynccontextmanager
async def connection(get_pool) -> asyncpg.Pool:
    connection_pool = await get_pool()
    async with connection_pool.acquire() as conn:
        yield conn

class AsyncPGConnection:
    def __init__(self, get_pool):
        self.get_pool = get_pool

    async def __aenter__(self):
        self.pool = await self.get_pool()
        self.conn = await self.pool.acquire()
        return self.conn

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.pool.release(self.conn)


class PG:
    def __init__(
        self,
        connection_params: dict,
    ):
        self.connection_params = connection_params
        self.pool = None

    async def get_pool(self):
        if not self.pool:
            connection_pool = await asyncpg.create_pool(
                user=self.connection_params.get("user"),
                password=self.connection_params.get("password"),
                database=self.connection_params.get("database"),
                host=self.connection_params.get("host"),
                port=self.connection_params.get("port"),
            )
            self.pool = connection_pool
        return self.pool

    async def execute(self, query: str, *args, **kwargs):
        async with connection(self.get_pool) as conn:
            record = await conn.fetchrow(query, *args, **kwargs)
            return dict(record) if record is not None else None       
    

    async def fetch(self, query: str, *args, **kwargs):
        async with connection(self.get_pool) as conn:
            async with conn.transaction():
                records = await conn.fetch(query, *args, **kwargs)
                result = [dict(r) for r in records]
            return result
