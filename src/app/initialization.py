from core.deps import SessionDep
from services.start_service import StartService


async def populate_data(session: SessionDep):
    await StartService.save_initial_movies(session=session)
