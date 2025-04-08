from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
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
    USE_FALLBACK,
    DEPLOY_ENVIRON,
    UNIX_SOCKET,
)

if DEPLOY_ENVIRON == "GOOGLE":
    url: str = f"postgresql+asyncpg://{DATABASE_USER}:{DATABASE_PASSWORD}@/{DATABASE_NAME}?host={UNIX_SOCKET}"
else:
    url: str = DATABASE_URL.format(
        DATABASE_USER, DATABASE_PASSWORD, DATABASE_ENDPOINT, DATABASE_PORT, DATABASE_NAME
    )
engine = (
    None
    if USE_FALLBACK
    else create_async_engine(url=url, pool_size=POOL_SIZE, max_overflow=POOL_MAX_OVERFLOW)
)

SessionMaker = sessionmaker(class_=AsyncSession, autoflush=False)


async def get_session():
    """
    Create a new session.
    :return:
    """
    async with SessionMaker(bind=engine) as session:
        yield session
