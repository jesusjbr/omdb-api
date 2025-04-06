from httpx import AsyncClient

from config import MOVIES_SEARCH_TERM
from core.deps import SessionDep
from repositories.database.db_movie_repository import MovieDatabaseRepository
from repositories.external.omdb_repository import OmdbRepository
from schemas.responses.omdb_responses import MovieImdbResponse
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
                OmdbRepository.set_client(client=client)
                imdb_ids: list[str] = await OmdbRepository.get_movies_by_search(
                    search_term=MOVIES_SEARCH_TERM
                )
                movies: list[MovieImdbResponse] = await OmdbRepository.get_movies_by_imdb_ids(
                    imdb_ids=imdb_ids
                )

                movies_to_insert = [
                    MovieCreate.model_validate(movie.model_dump()) for movie in movies
                ]
            await MovieDatabaseRepository.bulk_insert(session=session, movies=movies_to_insert)
