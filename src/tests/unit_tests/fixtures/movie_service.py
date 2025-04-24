from unittest.mock import AsyncMock

import pytest

from config import ORDER_TYPE_ASC, ORDER_BY_ID
from repositories.database.movie import MovieDatabaseRepository
from schemas.responses.movie import MoviesResponse
from schemas.responses.omdb import MovieImdbResponse
from schemas.shared.movie import MovieCreate, MovieGet
from schemas.shared.pagination_filter import Pagination


@pytest.fixture(scope="function")
def mock_movie_imdb_response():
    return MovieImdbResponse.model_validate(
        {
            "Actors": "N/A",
            "Awards": "N/A",
            "BoxOffice": "N/A",
            "Country": "Switzerland",
            "DVD": "N/A",
            "Director": "Christian Davi",
            "Genre": "Short",
            "Language": "German",
            "Metascore": "N/A",
            "Plot": "N/A",
            "Poster": "N/A",
            "Production": "N/A",
            "Rated": "N/A",
            "Ratings": [{"Source": "Internet Movie Database", "Value": "5.6/10"}],
            "Released": "N/A",
            "Response": "True",
            "Runtime": "5 min",
            "Title": "Spiderman",
            "Type": "movie",
            "Website": "N/A",
            "Writer": "N/A",
            "Year": "1990",
            "imdbID": "tt0100669",
            "imdbRating": "5.6",
            "imdbVotes": "97",
        }
    )


@pytest.fixture(scope="function")
def mock_omdb_repository_get_movie_by_title(monkeypatch, mock_movie_imdb_response):
    mock = AsyncMock(return_value=mock_movie_imdb_response)
    monkeypatch.setattr(
        "repositories.external.omdb.OmdbRepository.get_movie_by_title",
        mock,
    )
    return mock


@pytest.fixture(scope="function")
def mock_movie_database_repository_create(monkeypatch, mock_movie_from_database):
    mock = AsyncMock(return_value=mock_movie_from_database)
    monkeypatch.setattr(
        "repositories.database.movie.MovieDatabaseRepository.create",
        mock,
    )
    return mock


@pytest.fixture(scope="function")
def mock_movie_to_create(mock_movie_imdb_response):
    return MovieCreate.model_validate(mock_movie_imdb_response.model_dump())


@pytest.fixture(scope="function")
def mock_movie_from_database(mock_movie_to_create):
    movie = MovieDatabaseRepository._map_schema_to_model([mock_movie_to_create])[0]
    movie.id = 1
    return movie


@pytest.fixture(scope="function")
def mock_insert_by_title_response(mock_movie_from_database):
    return MovieGet.model_validate(mock_movie_from_database)


@pytest.fixture(scope="function")
def mock_get_single_movie_movie_response(mock_movie_from_database):
    return MovieGet.model_validate(mock_movie_from_database)


@pytest.fixture(scope="function")
def mock_movie_database_repository_get_all_paginated(monkeypatch, mock_movie_from_database):
    mock = AsyncMock(return_value=([mock_movie_from_database], 1))
    monkeypatch.setattr(
        "repositories.database.movie.MovieDatabaseRepository.get_all_paginated",
        mock,
    )
    return mock


@pytest.fixture(scope="function")
def mock_get_movies_response(mock_movie_from_database):
    pagination = Pagination(page=1, page_size=10)
    return MoviesResponse(
        page=pagination.page,
        page_size=pagination.page_size,
        total=1,
        order_by=ORDER_BY_ID,
        order_type=ORDER_TYPE_ASC,
        movies=[MovieGet.model_validate(movie) for movie in [mock_movie_from_database]],
    )


@pytest.fixture(scope="function")
def mock_movie_database_repository_get(monkeypatch, mock_movie_from_database):
    mock = AsyncMock(return_value=(mock_movie_from_database))
    monkeypatch.setattr(
        "repositories.database.movie.MovieDatabaseRepository.get",
        mock,
    )
    return mock


@pytest.fixture(scope="function")
def mock_movie_database_repository_delete(monkeypatch):
    mock = AsyncMock(return_value=True)
    monkeypatch.setattr(
        "repositories.database.movie.MovieDatabaseRepository.delete",
        mock,
    )
    return mock
