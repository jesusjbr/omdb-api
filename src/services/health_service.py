from fastapi import HTTPException, status

from core.deps import SessionDep
from repositories.db_health_repository import HealthRepository


class HealthService:
    """Performs Healthchecks"""

    @staticmethod
    async def healtcheck(session: SessionDep):
        """
        Healthcheck
        :param session: Database session
        """
        health_ok = await HealthRepository.get(session=session)
        if not health_ok:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Healthcheck failed",
            )
