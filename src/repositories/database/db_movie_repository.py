from sqlalchemy import select, func, delete, Function, Select

from core.deps import SessionDep
from repositories.database.models.movie import Movie
from schemas.shared.movie_schemas import MovieCreate


class MovieDatabaseRepository:
    """Handles database operations for Movie objects"""

    @staticmethod
    async def bulk_insert(session: SessionDep, movies: list[MovieCreate]):
        """
        Inserts in bulk a group of movies.
        :param session: The database session to use for the query.
        :param movies: A list of movies to insert.
        """
        movies_to_save = [Movie(**movie.model_dump()) for movie in movies]
        session.add_all(movies_to_save)
        await session.commit()

    @staticmethod
    async def count(session: SessionDep) -> int:
        """
        Retrieves the total count of movies.
        :param session: The database session to use for the query.
        :return: Total count of movies.
        """
        count_query = select(func.count(Movie.id))
        return await session.scalar(count_query)

    @staticmethod
    async def create(session: SessionDep, movie: MovieCreate):
        """
        Inserts a new movie in the database.
        :param session: The database session to use for the query.
        :param movie: The movie to insert.
        """
        session.add(movie)
        await session.commit()

    @staticmethod
    async def get(session: SessionDep, id: int) -> Movie | None:
        """
        Retrieves a movie by id.
        :param session: The database session to use for the query.
        :param id: Id of the movie to retrieve, do not confuse with imdb_id
        :return: If found, returns the movie, otherwise returns None.
        """
        query = select(Movie).where(Movie.id == id)
        return await session.scalar(query)

    @staticmethod
    async def get_all_paginated(
        session: SessionDep, title: str | None, limit: int | None = None, offset: int | None = None
    ) -> tuple[list[Movie], int]:
        """
        Retrieves a list of movies. If title is provided the movies are ordered by title,
        otherwise by id.
        :param session: The database session to use for the query.
        :param title: Filter to get only movies whose title matches exactly this.
        :param limit: Limit for this query (optional). If not provided, returns all results.
        :param offset: Offset for this query (optional). If not provided, returns all results.
        returns all results.
        :return: Tuple containing a list of movies, and total count of movies.
        """
        count: Function = func.count().over().label("total_count")
        query: Select[tuple[Movie, int]] = select(Movie, count)
        if not title:
            query = query.order_by(Movie.title)
        if title:
            query = query.where(Movie.title == title).order_by(Movie.id)
        if limit and offset:
            query = query.limit(limit).offset(offset)
        rows: list[tuple[Movie, int]] = list((await session.execute(query)).all())
        # It would have been cleaner to use a separate count query, but in terms of performance
        # it is better to avoid duplicated database round-trips.
        movies: list[Movie] = []
        total: int = 0
        if rows:
            _, total = rows[0]
            movies = [movie for movie, _ in rows]

        return movies, total

    @staticmethod
    async def delete(session: SessionDep, id: int) -> bool:
        """
        Delete a movie by its id if exists.
        :param session: The database session to use for the query.
        :param id: Id of the movie to delete, do not confuse with imdb_id
        :return: Number of rows affected.
        """
        query = delete(Movie).where(Movie.id == id)
        result = await session.execute(query)
        await session.commit()
        return result.rowcount == 1
