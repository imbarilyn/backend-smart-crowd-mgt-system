from app.core.database import db
from fastapi import Depends


async def get_db_connection():
    """Dependency to get a database connection from the pool"""
    async with db.pool.acquire() as connection:
        yield connection


sessionDependency = Depends(get_db_connection)
