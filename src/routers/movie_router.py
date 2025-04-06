from fastapi import APIRouter, Path, status

from config import TAG_MOVIE
from core.deps import SessionDep
from schemas.requests.insert_movies_request import InsertTitleBody
from schemas.responses.movie_responses import MoviesResponse, SingleMovieResponse
from schemas.shared.pagination_filter import Pagination
from services.movie_service import MovieService

router = APIRouter(prefix="/api/{version}/movies")


@router.post("", tags=[TAG_MOVIE])
async def insert_movie_by_title(session: SessionDep, body: InsertTitleBody) -> SingleMovieResponse:
    """
    Searches movies with given title in OMDB and stores them in our database.
    :param session: A database session.
    :param body: The title that movies should match exactly.
    :return: The inserted movies if there is some.
    """

    return await MovieService.insert_movie_by_title(session=session, title=body.title)


@router.get("", tags=[TAG_MOVIE])
async def get_movies(
    session: SessionDep,
    title: str | None = None,
    page: int = 1,
    page_size: int = 10,
) -> MoviesResponse:
    """
    Retrieves a paginated list of movies, filtered by title if provided.
    Default ordering is by title if not provided, or else by id.

    :param session: A database session.
    :param title: Filter to get only movies whose title matches exactly this.
    :param page: Page number for pagination.
    :param page_size: Size of the page for pagination.
    :return: Response including paginated and ordered movies.
    """
    return await MovieService.get_movies(
        session=session, title=title, pagination=Pagination(page=page, page_size=page_size)
    )


@router.get("/{id}", tags=[TAG_MOVIE])
async def get_single_movie(session: SessionDep, id: int = Path()) -> SingleMovieResponse:
    """
    Retrieves a movie by id.
    :param session: A database session
    :param id: id of the movie to retrieve
    :return: Response including the movie if found
    """
    return await MovieService.get_single_movie(session=session, id=id)


@router.delete("/{id}", tags=[TAG_MOVIE], status_code=status.HTTP_204_NO_CONTENT)
async def delete_movie(session: SessionDep, id: int = Path()):
    """
    Delete a movie by id.
    :param session: A database session
    :param id: id of the movie to delete
    """
    return await MovieService.delete_movie(session=session, id=id)
