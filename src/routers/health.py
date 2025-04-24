from fastapi import APIRouter, status

from config import TAG_HEALTHCHECK
from core.deps import SessionDep
from services.health import HealthService

router = APIRouter()


@router.post("/", tags=[TAG_HEALTHCHECK], status_code=status.HTTP_200_OK)
async def healthcheck(session: SessionDep):
    """
    Checks the health status.
    :param session: A database session
    :return: 200 OK
    """
    return await HealthService.healtcheck(session=session)
