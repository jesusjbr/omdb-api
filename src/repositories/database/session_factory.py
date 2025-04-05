from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker

from config import (
    DATABASE_URL,
    DATABASE_PASSWORD,
    DATABASE_ENDPOINT,
    DATABASE_USER,
    DATABASE_PORT,
    POOL_SIZE,
    POOL_MAX_OVERFLOW,
    DATABASE_NAME,
)

url: str = DATABASE_URL.format(
    DATABASE_USER, DATABASE_PASSWORD, DATABASE_ENDPOINT, DATABASE_PORT, DATABASE_NAME
)

engine: AsyncEngine = create_async_engine(
    url=url, pool_size=POOL_SIZE, max_overflow=POOL_MAX_OVERFLOW
)

SessionMaker = sessionmaker(class_=AsyncSession, autoflush=False)


async def get_session():
    """
    Create a new session.
    :return:
    """
    async with SessionMaker(bind=engine) as session:
        yield session
