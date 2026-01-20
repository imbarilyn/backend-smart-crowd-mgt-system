import asyncpg
from asyncpg.pool import Pool
from app.core.settings import DB_NAME, DB_PASSWORD, DB_PORT, DB_USER, DB_HOST
from urllib.parse import quote_plus

ENCODED_DB_PASSWORD = quote_plus(DB_PASSWORD)
DATABASE_URL = f"postgresql://{DB_USER}:{ENCODED_DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


class Postgres:
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.pool: Pool | None = None

    async def connect(self):
        """Create a database pool connection for the application startup"""
        if self.pool is None:
            self.pool = await asyncpg.create_pool(self.database_url)
            print("Database connection pool created successfully.")

    async def disconnect(self):
        """Close the database pool connection for the application shutdown"""
        if self.pool:
            await self.pool.close()
            print("Database connection pool closed successfully.")


db = Postgres(DATABASE_URL)
