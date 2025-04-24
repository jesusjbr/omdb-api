import pytest
from fastapi import status

from schemas.requests.insert_movies import InsertTitleBody
from schemas.shared.pagination_filter import Pagination
from tests.unit_tests.fixtures.client import (
    override_get_user_admin,
    override_get_user_regular,
    override_session_dependency,
    mock_session,
    fake_regular_user,
    fake_admin_user,
    fake_client_admin_user,
    fake_client_regular_user,
    fake_client_without_user,
)
from tests.unit_tests.fixtures.movie_router import (
    mock_delete_movie,
    mock_movie_id,
    mock_get_single_movie,
    mock_single_movie_response,
    mock_get_movies,
    mock_get_movies_response,
    mock_insert_movie_by_title,
)


def test_delete_movie_ok(fake_client_admin_user, mock_session, mock_delete_movie, mock_movie_id):
    """Admin users are authorized to use this endpoint."""
    response = fake_client_admin_user.delete(f"/api/v1/movies/{mock_movie_id}")
    mock_delete_movie.assert_awaited_once_with(session=mock_session, id=mock_movie_id)
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_movie_forbidden_user(fake_client_regular_user, mock_delete_movie, mock_movie_id):
    """A regular user is not authorized to use this endpoint."""
    response = fake_client_regular_user.delete(f"/api/v1/movies/{mock_movie_id}")
    mock_delete_movie.assert_not_awaited()
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_delete_without_user(fake_client_without_user, mock_delete_movie, mock_movie_id):
    """Unauthenticated users cant access this endpoint"""
    response = fake_client_without_user.delete(f"/api/v1/movies/{mock_movie_id}")
    mock_delete_movie.assert_not_awaited()
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_get_single_movie(
    fake_client_regular_user,
    mock_get_single_movie,
    mock_movie_id,
    mock_single_movie_response,
    mock_session,
):
    """Any authenticated user can access this endpoint"""
    response = fake_client_regular_user.get(f"/api/v1/movies/{mock_movie_id}")
    mock_get_single_movie.assert_awaited_once_with(session=mock_session, id=mock_movie_id)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == mock_single_movie_response.model_dump(mode="json")


def test_get_single_movie_without_user(
    fake_client_without_user, mock_get_single_movie, mock_movie_id
):
    """Unauthenticated users cant access this endpoint"""
    response = fake_client_without_user.get(f"/api/v1/movies/{mock_movie_id}")
    mock_get_single_movie.assert_not_awaited()
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.parametrize(
    "title, page, page_size, expected_pagination",
    [
        (None, None, None, Pagination(page=1, page_size=10)),
        ("Avengers", None, None, Pagination(page=1, page_size=10)),
        (None, 2, None, Pagination(page=2, page_size=10)),
        (None, None, 5, Pagination(page=1, page_size=5)),
        (None, 3, None, Pagination(page=3, page_size=10)),
        (None, 1, 20, Pagination(page=1, page_size=20)),
        (None, 2, 10, Pagination(page=2, page_size=10)),
    ],
)
def test_get_movies(
    fake_client_regular_user,
    mock_get_movies,
    mock_get_movies_response,
    mock_session,
    title,
    page,
    page_size,
    expected_pagination,
):
    """Any authenticated user can access this endpoint"""
    params = {}
    if title:
        params["title"] = title
    if page:
        params["page"] = page
    if page_size:
        params["page_size"] = page_size
    response = fake_client_regular_user.get(f"/api/v1/movies", params=params)
    mock_get_movies.assert_awaited_once_with(
        session=mock_session, title=title, pagination=expected_pagination
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == mock_get_movies_response.model_dump(mode="json")


def test_get_movies_without_user(fake_client_without_user, mock_get_movies):
    """Unauthenticated users cant access this endpoint"""
    params = {}
    response = fake_client_without_user.get(f"/api/v1/movies", params=params)
    mock_get_movies.assert_not_awaited()
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_insert_movie_by_title(
    fake_client_regular_user, mock_insert_movie_by_title, mock_single_movie_response, mock_session
):
    """Any authenticated user can access this endpoint"""
    body = {"title": "The Avengers"}
    response = fake_client_regular_user.post(f"/api/v1/movies", json=body)
    mock_insert_movie_by_title.assert_awaited_once_with(session=mock_session, title=body["title"])
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == mock_single_movie_response.model_dump(mode="json")


def test_insert_movie_by_title_without_user(fake_client_without_user, mock_insert_movie_by_title):
    """Unauthenticated users cant access this endpoint"""
    params = {}
    response = fake_client_without_user.post(f"/api/v1/movies", params=params)
    mock_insert_movie_by_title.assert_not_awaited()
    assert response.status_code == status.HTTP_403_FORBIDDEN
