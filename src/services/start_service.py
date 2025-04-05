from httpx import AsyncClient

from config import MOVIES_SEARCH_TERM
from core.deps import SessionDep
from repositories.database.db_movie_repository import MovieDatabaseRepository
from repositories.external.omdb_repository import OmdbRepository
from schemas.shared.movie_schemas import MovieCreate


class StartService:
    """The purpose of this service is to fetch the data to populate the database"""

    @staticmethod
    async def save_initial_movies(session: SessionDep):
        """
        Retrieves the initial movies and store them in the database
        """
        number_of_movies = await MovieDatabaseRepository.count(session=session)
        if number_of_movies == 0:
            async with AsyncClient() as client:
                imdb_ids: list[str] = await OmdbRepository.get_movies_by_search(
                    client=client, search_term=MOVIES_SEARCH_TERM
                )
            await MovieDatabaseRepository.bulk_insert(session=session, movies=movies)
