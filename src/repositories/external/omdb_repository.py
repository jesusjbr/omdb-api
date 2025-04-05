import asyncio
import math
from typing import Type, TypeVar

from fastapi import status
from httpx import Response, AsyncClient
from pydantic import BaseModel

from config import OMDB_API_URL, OMDB_API_KEY, MAX_TOTAL_PAGES, RESULTS_PER_PAGE, TYPE_MOVIE
from exceptions.omdb_repository_exceptions import (
    OmdbRepositoryUnauthorizedException,
    OmdbRepositoryBadRequestException,
    OmdbRepositoryNotFoundException,
    OmdbRepositoryInternalServerErrorException,
    OmdbRepositoryInvalidResponseFormatException,
)
from schemas.responses.omdb_responses import MovieSearchResponse, MovieImdbResponse

T = TypeVar("T", bound=BaseModel)


class OmdbRepository:
    """Repository to make requests to the OMDB API"""

    # Since most of the methods here are intended only to be used at the start of the application
    # they can share one client. Only one method will use its own client.
    # The purpose of this client is to make asynchronous HTTP requests.
    client: AsyncClient

    @classmethod
    def set_client(cls, client: AsyncClient):
        """Sets the AsyncClient for the repository."""
        cls.client = client

    @classmethod
    def get_client(cls) -> AsyncClient:
        """Gets the AsyncClient of the repository."""
        if cls.client is None:
            raise ValueError("Client has not been set.")
        return cls.client

    @staticmethod
    async def get_movies_by_imdb_ids(imdb_ids: list[str]) -> list[MovieImdbResponse]:
        """
        Fetches all the movies data using imdb_ids

        :param imdb_ids: list of imdb_id
        :return: List of movies
        """
        client = OmdbRepository.get_client()
        tasks = [
            OmdbRepository._fetch_movie_by_imdb_id(client=client, imdb_id=imdb_id)
            for imdb_id in imdb_ids
        ]
        movies_responses: list[MovieImdbResponse] = await asyncio.gather(*tasks)
        return movies_responses

    @staticmethod
    async def get_movies_by_search(search_term: str) -> list[str]:
        """
        Fetches multiple pages (up to 100 results) asynchronously and returns a list of
        imdb_ids for these movies.
        :param search_term: The term to search within movie titles.
        :return: List of imdb_ids
        """
        client = OmdbRepository.get_client()
        first_page_results: MovieSearchResponse = await OmdbRepository._fetch_page_by_search_term(
            client=client, search_term=search_term, page=1
        )

        # Extract total number of results and calculate number of pages needed
        total_results: int = int(first_page_results.total_results)
        # Ensure we fetch at most 10 pages
        total_pages: int = int(min(math.ceil(total_results / RESULTS_PER_PAGE), MAX_TOTAL_PAGES))

        # Fetch remaining pages concurrently
        tasks = [
            OmdbRepository._fetch_page_by_search_term(
                client=client, search_term=search_term, page=page
            )
            for page in range(2, total_pages + 1)
        ]
        movies_responses: list[MovieSearchResponse] = await asyncio.gather(*tasks)

        # Flatten the results lists
        imdb_ids: list[str] = [movie.imdb_id for movie in first_page_results.movies]
        for response in movies_responses:
            imdb_ids.extend([movie.imdb_id for movie in response.movies])

        return imdb_ids

    @staticmethod
    async def _fetch_page_by_search_term(search_term: str, page: int) -> MovieSearchResponse:
        """
        Fetch a concrete page of results by search term.
        :param search_term: The term to search within movie titles.
        :param page: The page to request among the results.
        :return: Response given by OMDB.
        """
        """Fetches a single page of results and returns a structured response."""
        client = OmdbRepository.get_client()
        params = {"s": search_term, "apikey": OMDB_API_KEY, "page": page, "type": TYPE_MOVIE}
        response: Response = await client.get(url=OMDB_API_URL, params=params)
        response_body = response.json()
        validated_movies_response = await OmdbRepository._validate_response(
            response.status_code, response_body, MovieSearchResponse
        )
        return validated_movies_response

    @staticmethod
    async def _fetch_movie_by_imdb_id(imdb_id: str) -> MovieImdbResponse:
        """
        Fetch a movie by its imdb_id
        :return: Response given by OMDB.
        """
        client = OmdbRepository.get_client()
        params = {"i": imdb_id, "apikey": OMDB_API_KEY, "type": TYPE_MOVIE}
        response: Response = await client.get(url=OMDB_API_URL, params=params)
        response_body = response.json()
        validated_movie_response = await OmdbRepository._validate_response(
            response.status_code, response_body, MovieImdbResponse
        )

        return validated_movie_response

    @staticmethod
    def _validate_response(status_code: int, response_body: dict, model: Type[T]) -> T:
        """
        Validates a response using the given Pydantic model and the status code.
        :param status_code: status code of the response
        :param response_body: Parsed JSON body.
        :param model: Pydantic model to validate the response against.
        :return: Parsed and validated Pydantic model instance.
        """
        if status_code == status.HTTP_200_OK:
            try:
                return model.model_validate(response_body)
            except ValueError as e:
                raise OmdbRepositoryInvalidResponseFormatException(detail={"error": str(e)})
        elif status_code == status.HTTP_401_UNAUTHORIZED:
            raise OmdbRepositoryUnauthorizedException(detail=response_body)
        elif status_code == status.HTTP_400_BAD_REQUEST:
            raise OmdbRepositoryBadRequestException(detail=response_body)
        elif status_code == status.HTTP_404_NOT_FOUND:
            raise OmdbRepositoryNotFoundException(detail=response_body)
        else:
            raise OmdbRepositoryInternalServerErrorException(detail=response_body)
