"""Database module for the FastAPI application"""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine
from sqlalchemy.orm import sessionmaker

from config import DATABASE_URL


engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=True)
async_session: sessionmaker = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Async generator for getting a session"""
    async with async_session() as session:
        yield session
