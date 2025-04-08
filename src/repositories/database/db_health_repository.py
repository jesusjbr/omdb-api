from sqlalchemy import select

from core.deps import SessionDep


class HealthRepository:
    """Checks the connectivity to the database"""

    @staticmethod
    async def get(session: SessionDep) -> int:
        """
        Checks the status of the connection to the database
        :param session: database session
        :return: health status
        """

        health = await session.scalar(select(1))
        return health
