from datetime import datetime
from unittest.mock import AsyncMock

import pytest

from config import ORDER_TYPE_ASC, ORDER_BY_ID
from repositories.database.models.rating import Rating
from schemas.responses.movie import SingleMovieResponse, MoviesResponse


@pytest.fixture(scope="function")
def mock_delete_movie(monkeypatch):
    mock = AsyncMock(return_value=None)
    monkeypatch.setattr(
        "services.movie_service.MovieService.delete_movie",
        mock,
    )
    return mock


@pytest.fixture(scope="function")
def mock_get_single_movie(monkeypatch, mock_single_movie_response):
    mock = AsyncMock(return_value=mock_single_movie_response)
    monkeypatch.setattr(
        "services.movie_service.MovieService.get_single_movie",
        mock,
    )
    return mock


@pytest.fixture(scope="function")
def mock_get_movies(monkeypatch, mock_get_movies_response):
    mock = AsyncMock(return_value=mock_get_movies_response)
    monkeypatch.setattr(
        "services.movie_service.MovieService.get_movies",
        mock,
    )
    return mock


@pytest.fixture(scope="function")
def mock_insert_movie_by_title(monkeypatch, mock_single_movie_response):
    mock = AsyncMock(return_value=mock_single_movie_response)
    monkeypatch.setattr(
        "services.movie_service.MovieService.insert_movie_by_title",
        mock,
    )
    return mock


@pytest.fixture(scope="function")
def mock_movie_id():
    """Fixture to create a"""
    return 1


@pytest.fixture(scope="function")
def mock_single_movie_response(mock_movie_id):
    """Fixture to create a"""
    return SingleMovieResponse(
        id=mock_movie_id,
        title="Avengers: Endgame",
        year=2019,
        rated="PG-13",
        released=datetime.strptime("04 May 2012", "%d %b %Y").date(),
        runtime="181 min",
        genre="Action, Adventure, Sci-Fi",
        director="Anthony Russo, Joe Russo",
        writer="Christopher Markus, Stephen McFeely, Stan Lee",
        actors="Robert Downey Jr., Chris Evans, Mark Ruffalo",
        plot=(
            "After the devastating events of Avengers: Infinity War (2018), the universe is in ruins. "
            "With the help of remaining allies, the Avengers assemble once more in order to reverse "
            "Thanos' actions and restore balance to the universe."
        ),
        language="English, Japanese, Xhosa, German",
        country="United States",
        awards="Nominated for 1 Oscar. 71 wins & 133 nominations total",
        poster="https://m.media-amazon.com/images/M/MV5BMTc5MDE2ODcwNV5BMl5BanBnXkFtZTgwMzI2NzQ2NzM@._V1_SX300.jpg",
        ratings=[
            Rating(source="Internet Movie Database", value="8.4/10"),
            Rating(source="Rotten Tomatoes", value="94%"),
            Rating(source="Metacritic", value="78/100"),
        ],
        metascore=78,
        imdb_rating=8.4,
        imdb_votes=1339749,
        imdb_id="tt4154796",
        type="movie",
        dvd=None,
        box_office="$858,373,000",
        production=None,
        website=None,
    )


@pytest.fixture(scope="function")
def mock_get_movies_response(mock_single_movie_response):
    """Fixture to create a"""
    return MoviesResponse(
        movies=[mock_single_movie_response],
        page=1,
        page_size=10,
        order_by=ORDER_BY_ID,
        order_type=ORDER_TYPE_ASC,
        total=1,
    )
