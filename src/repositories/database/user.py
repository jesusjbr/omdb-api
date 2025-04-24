from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.database.models.user import User
from schemas.shared.user_schema import UserData


class UserDatabaseRepository:
    """Handles database operations for User objects"""

    @staticmethod
    async def create(session: AsyncSession, user: UserData) -> User:
        """
        Inserts a new user in the database.
        :param session: The database session to use for the query.
        :param user: The user to insert.
        """
        user_to_create: User = User(**user.model_dump())
        session.add(user_to_create)
        await session.commit()
        query = select(User).where(User.username == user.username)
        return (await session.execute(query)).scalar_one_or_none()

    @staticmethod
    async def get_by_username(session: AsyncSession, username: str) -> User | None:
        """
        Retrieves a user by its username.
        :param session: The database session to use for the query.
        :param username: username of the user
        :return: If found, returns the user, otherwise returns None.
        """
        query = select(User).where(User.username == username)
        return (await session.execute(query)).scalar_one_or_none()
