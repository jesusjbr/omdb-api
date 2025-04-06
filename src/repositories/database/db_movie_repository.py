from sqlalchemy import select, func, delete, Function, Select
from sqlalchemy.orm import selectinload

from core.deps import SessionDep
from repositories.database.models.movie import Movie
from repositories.database.models.rating import Rating
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
        movies_to_insert: list[Movie] = MovieDatabaseRepository._map_schema_to_model(movies)
        session.add_all(movies_to_insert)
        await session.commit()

    @staticmethod
    def _map_schema_to_model(movies: list[MovieCreate]):
        """
        A manual mapping of types that highlights the impedance mismatch between schemas and models.
        :param movies: Movies to map from list[MovieCreate] to list[Movie]
        :return: Transformed movies as list[Movie]
        """
        movies_to_insert: list[Movie] = []
        for movie_create in movies:
            movie_data: dict = movie_create.model_dump(exclude={"ratings"})
            movie: Movie = Movie(**movie_data)

            if movie_create.ratings:
                for rating_create in movie_create.ratings:
                    rating: Rating = Rating(**rating_create.model_dump())
                    movie.ratings.append(rating)

            movies_to_insert.append(movie)
        return movies_to_insert

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
        movie_to_create: Movie = MovieDatabaseRepository._map_schema_to_model([movie])[0]
        session.add(movie_to_create)
        await session.commit()

    @staticmethod
    async def get(session: SessionDep, id: int) -> Movie | None:
        """
        Retrieves a movie by id.
        :param session: The database session to use for the query.
        :param id: Id of the movie to retrieve, do not confuse with imdb_id
        :return: If found, returns the movie, otherwise returns None.
        """
        query = select(Movie).where(Movie.id == id).options(selectinload(Movie.ratings))
        return (await session.execute(query)).scalar_one_or_none()

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
        query: Select[tuple[Movie, int]] = select(Movie, count).options(selectinload(Movie.ratings))
        if not title:
            query = query.order_by(Movie.title)
        if title:
            query = query.where(Movie.title == title).order_by(Movie.id)
        if limit is not None and offset is not None:
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
