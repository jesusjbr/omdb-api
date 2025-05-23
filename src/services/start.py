from httpx import AsyncClient

from config import (
    MOVIES_SEARCH_TERM,
    REGULAR_USER_PASSWORD,
    REGULAR_USER_IS_ADMIN,
    REGULAR_USER_USERNAME,
    ADMIN_USER_USERNAME,
    ADMIN_USER_PASSWORD,
    ADMIN_USER_IS_ADMIN,
)
from core.deps import SessionDep
from core.security import Security
from repositories.database.movie import MovieDatabaseRepository
from repositories.database.user import UserDatabaseRepository
from repositories.external.omdb import OmdbRepository
from schemas.responses.omdb import MovieImdbResponse
from schemas.shared.movie import MovieCreate
from schemas.shared.user import UserData


class StartService:
    """The purpose of this service is to fetch the data to populate the database"""

    @staticmethod
    async def save_initial_data(session: SessionDep):
        """
        Retrieves the initial movies and store them in the database.
        Create a couple of demo users to be able to test the app.
        :param session: Database session
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
            # This should be managed ideally with a transaction.
            await MovieDatabaseRepository.bulk_insert(session=session, movies=movies_to_insert)
            await UserDatabaseRepository.create(
                session=session,
                user=UserData(
                    username=REGULAR_USER_USERNAME,
                    hashed_password=Security.get_password_hash(REGULAR_USER_PASSWORD),
                    is_admin=REGULAR_USER_IS_ADMIN,
                ),
            )
            await UserDatabaseRepository.create(
                session=session,
                user=UserData(
                    username=ADMIN_USER_USERNAME,
                    hashed_password=Security.get_password_hash(ADMIN_USER_PASSWORD),
                    is_admin=ADMIN_USER_IS_ADMIN,
                ),
            )
