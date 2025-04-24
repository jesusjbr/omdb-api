from config import ORDER_BY_TITLE, ORDER_TYPE_ASC, ORDER_BY_ID
from core.deps import SessionDep
from exceptions.movie_exceptions import MovieNotFoundException, MovieAlreadyExistsException
from repositories.database.movie import MovieDatabaseRepository
from repositories.database.models.movie import Movie
from repositories.external.omdb import OmdbRepository
from schemas.responses.movie import MoviesResponse, SingleMovieResponse
from schemas.responses.omdb import MovieImdbResponse
from schemas.shared.movie_schemas import MovieGet, MovieCreate
from schemas.shared.pagination_filter import Pagination


class MovieService:
    """ """

    @staticmethod
    async def insert_movie_by_title(session: SessionDep, title: str) -> SingleMovieResponse:
        """
        Searches movies with given title in OMDB and stores them in our database.
        Even if the OMDB Endpoint returns only one movie when filtering by title,
        title is not a UNIQUE field and its value is repeated. Thus, there could be multiple movies
        with the same title.
        :param session: A database session.
        :param title: The title that movies should match exactly.
        :return: The inserted movies if there is some.
        """
        movie: MovieImdbResponse = await OmdbRepository.get_movie_by_title(title=title)
        if not movie:
            raise MovieNotFoundException(detail={"title": title})
        try:
            created_movie = await MovieDatabaseRepository.create(
                session=session, movie=MovieCreate.model_validate(movie.model_dump())
            )
        except Exception as e:
            if MovieDatabaseRepository.check_already_exists(e):
                raise MovieAlreadyExistsException(detail={"title": title})
            else:
                raise e
        return MovieGet.model_validate(created_movie)

    @staticmethod
    async def get_movies(
        session: SessionDep, title: str | None, pagination: Pagination
    ) -> MoviesResponse:
        """
        Retrieves a paginated list of movies, filtered by title if provided.
        Default ordering is by title if not provided, or else by id.

        :param session: A database session
        :param title: Filter to get only movies whose title matches exactly this.
        :param pagination: Pagination to apply
        :return: Response including paginated and ordered movies.
        """
        movies: list[Movie]
        total_count: int
        limit: int
        offset: int
        limit, offset = MovieService._calculate_limit_offset(pagination=pagination)

        movies, total_count = await MovieDatabaseRepository.get_all_paginated(
            session=session, title=title, limit=limit, offset=offset
        )

        default_order = ORDER_BY_ID if title else ORDER_BY_TITLE
        return MoviesResponse(
            page=pagination.page,
            page_size=pagination.page_size,
            total=total_count,
            order_by=default_order,
            order_type=ORDER_TYPE_ASC,
            movies=[MovieGet.model_validate(movie) for movie in movies],
        )

    @staticmethod
    async def get_single_movie(session: SessionDep, id: int) -> SingleMovieResponse:
        """
        Retrieves a movie by id.
        :param session: A database session
        :param id: id of the movie to retrieve
        :return: Response including the movie if found
        """

        movie: Movie = await MovieDatabaseRepository.get(session=session, id=id)
        if not movie:
            raise MovieNotFoundException(detail={"id": id})
        return MovieGet.model_validate(movie)

    @staticmethod
    async def delete_movie(session: SessionDep, id: int):
        """
        Delete a movie by id.
        :param session: A database session
        :param id: id of the movie to delete
        """

        movie_affected: bool = await MovieDatabaseRepository.delete(session=session, id=id)
        if not movie_affected:
            raise MovieNotFoundException(detail={"id": id})

    @staticmethod
    def _calculate_limit_offset(pagination: Pagination) -> tuple[int | None, int | None]:
        """
        Calculates limit and offset from pagination
        :param pagination: Pagination object that contains page and page_size
        :return: A tuple with the limit and offset
        """
        if pagination.page and pagination.page_size:
            return pagination.page_size, (
                pagination.page * pagination.page_size
            ) - pagination.page_size
        else:
            return None, None
