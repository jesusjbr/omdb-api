import pytest
from sqlalchemy.exc import IntegrityError

from config import IMDB_ID_UNIQUE_CONSTRAINT
from exceptions.movie_exceptions import MovieNotFoundException, MovieAlreadyExistsException
from schemas.shared.pagination_filter import Pagination
from services.movie import MovieService
from tests.unit_tests.fixtures.client import mock_session
from tests.unit_tests.fixtures.movie_service import (
    mock_omdb_repository_get_movie_by_title,
    mock_movie_database_repository_create,
    mock_movie_to_create,
    mock_insert_by_title_response,
    mock_movie_imdb_response,
    mock_movie_from_database,
    mock_movie_database_repository_get_all_paginated,
    mock_get_movies_response,
    mock_movie_database_repository_get,
    mock_get_single_movie_movie_response,
    mock_movie_database_repository_delete,
)


@pytest.mark.asyncio
async def test_insert_movie_by_title(
    mock_session,
    mock_omdb_repository_get_movie_by_title,
    mock_movie_database_repository_create,
    mock_movie_to_create,
    mock_insert_by_title_response,
):
    """Checks that this service method works like intended."""
    title = "Batman"
    response = await MovieService.insert_movie_by_title(session=mock_session, title=title)
    mock_omdb_repository_get_movie_by_title.assert_awaited_once_with(title=title)
    mock_movie_database_repository_create.assert_awaited_once_with(
        session=mock_session, movie=mock_movie_to_create
    )
    assert response == mock_insert_by_title_response


@pytest.mark.asyncio
async def test_insert_movie_by_title_movie_not_found(
    mock_session, mock_omdb_repository_get_movie_by_title, mock_movie_database_repository_create
):
    """Checks that MovieNotFoundException is raised when omdb_repository returns nothing.."""
    title = "Batman"
    mock_omdb_repository_get_movie_by_title.return_value = None
    with pytest.raises(MovieNotFoundException):
        _ = await MovieService.insert_movie_by_title(session=mock_session, title=title)
    mock_omdb_repository_get_movie_by_title.assert_awaited_once_with(title=title)
    mock_movie_database_repository_create.assert_not_awaited()


@pytest.mark.asyncio
async def test_insert_movie_by_title_already_exists(
    mock_session,
    mock_omdb_repository_get_movie_by_title,
    mock_movie_database_repository_create,
    mock_movie_to_create,
    mock_insert_by_title_response,
):
    """Checks that MovieNotFoundException is raised when omdb_repository returns nothing.."""
    title = "Batman"
    mock_movie_database_repository_create.side_effect = IntegrityError(
        statement="INSERT INTO movie...",
        params={"imdb_id": "tt1234567"},
        orig=Exception(IMDB_ID_UNIQUE_CONSTRAINT),
    )
    with pytest.raises(MovieAlreadyExistsException):
        _ = await MovieService.insert_movie_by_title(session=mock_session, title=title)
    mock_omdb_repository_get_movie_by_title.assert_awaited_once_with(title=title)
    mock_movie_database_repository_create.assert_awaited_once_with(
        session=mock_session, movie=mock_movie_to_create
    )


@pytest.mark.asyncio
async def test_get_movies(
    mock_session, mock_movie_database_repository_get_all_paginated, mock_get_movies_response
):
    """Checks that this service method works like intended."""
    title = "Batman"
    pagination = Pagination(page=1, page_size=10)
    response = await MovieService.get_movies(
        session=mock_session, title=title, pagination=pagination
    )
    limit, offset = MovieService._calculate_limit_offset(pagination=pagination)
    mock_movie_database_repository_get_all_paginated.assert_awaited_once_with(
        session=mock_session, title=title, limit=limit, offset=offset
    )

    assert response == mock_get_movies_response


@pytest.mark.asyncio
async def test_get_single_movie(
    mock_session, mock_movie_database_repository_get, mock_get_single_movie_movie_response
):
    """Checks that this service method works like intended."""
    id = 1
    response = await MovieService.get_single_movie(session=mock_session, id=id)
    mock_movie_database_repository_get.assert_awaited_once_with(session=mock_session, id=id)

    assert response == mock_get_single_movie_movie_response


@pytest.mark.asyncio
async def test_get_single_movie_not_found(
    mock_session, mock_movie_database_repository_get, mock_get_single_movie_movie_response
):
    """Checks that this service method works like intended."""
    id = 1
    mock_movie_database_repository_get.return_value = None
    with pytest.raises(MovieNotFoundException):
        _ = await MovieService.get_single_movie(session=mock_session, id=id)


@pytest.mark.anyo
async def test_delete_movie(
    mock_session, mock_movie_database_repository_delete, mock_get_single_movie_movie_response
):
    """Checks that this service method works like intended."""
    id = 1
    await MovieService.delete_movie(session=mock_session, id=id)
    mock_movie_database_repository_delete.assert_awaited_once_with(session=mock_session, id=id)


@pytest.mark.anyo
async def test_delete_movie_not_found(mock_session, mock_movie_database_repository_delete):
    """Checks that MovieNotFoundException is raised"""
    id = 1
    mock_movie_database_repository_delete.return_value = None
    with pytest.raises(MovieNotFoundException):
        await MovieService.delete_movie(session=mock_session, id=id)
