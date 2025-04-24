from core.deps import SessionDep
from services.start import StartService


async def populate_data(session: SessionDep):
    await StartService.save_initial_data(session=session)
