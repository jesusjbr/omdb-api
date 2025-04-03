import asyncio
import math
from http import HTTPStatus

import httpx

from config import OMDB_API_URL, OMDB_API_KEY, MAX_TOTAL_PAGES, RESULTS_PER_PAGE, TYPE_MOVIE
from exceptions.omdb_repository_exceptions import OmdbRepositoryUnauthorizedException, \
    OmdbRepositoryBadRequestException, OmdbRepositoryNotFoundException, OmdbRepositoryInternalServerErrorException, \
    OmdbRepositoryInvalidResponseFormatException
from schemas.responses.omdb_by_search import Movie, MovieSearchResponse


class OmdbRepository:
    """

    """
    @staticmethod
    async def fetch_page(search_term: str, page: int) -> MovieSearchResponse:
        """Fetches a single page of results and returns a structured response."""
        params = {
            "s": search_term,
            "apikey": OMDB_API_KEY,
            "page": page,
            "type": TYPE_MOVIE
        }
        async with httpx.AsyncClient() as client:
            response = await client.get(url=OMDB_API_URL, params=params)

        response_body = response.json()
        # Raise the proper exception if needed
        if response.status_code == HTTPStatus.OK.value:
            try:
                validated_movies_response: MovieSearchResponse = MovieSearchResponse.model_validate(response_body)
            except ValueError as e:
                raise OmdbRepositoryInvalidResponseFormatException(detail={'error': str(e)})
        elif response.status_code == HTTPStatus.UNAUTHORIZED.value:
            raise OmdbRepositoryUnauthorizedException(detail=response_body)
        elif response.status_code == HTTPStatus.BAD_REQUEST.value:
            raise OmdbRepositoryBadRequestException(detail=response_body)
        elif response.status_code == HTTPStatus.NOT_FOUND.value:
            raise OmdbRepositoryNotFoundException(detail=response_body)
        else:
            raise OmdbRepositoryInternalServerErrorException(detail=response_body)

        return validated_movies_response

    @staticmethod
    async def get_movies_by_search(search_term: str) -> list[Movie]:
        """Fetches multiple pages (up to 100 results) asynchronously and returns a list of Movie objects."""
        first_page_results: MovieSearchResponse = await OmdbRepository.fetch_page(search_term, page=1)

        # Extract total number of results and calculate number of pages needed
        total_results: int = int(first_page_results.total_results)
        # Ensure we fetch at most 10 pages
        total_pages: int = int(min(math.ceil(total_results / RESULTS_PER_PAGE), MAX_TOTAL_PAGES))

        # Fetch remaining pages concurrently
        tasks = [OmdbRepository.fetch_page(search_term, page) for page in range(2, total_pages + 1)]
        movies_responses: list[MovieSearchResponse] = await asyncio.gather(*tasks)

        # Flatten the results lists
        all_movies: list[Movie] = first_page_results.movies
        for response in movies_responses:
            all_movies.extend(response.movies)

        return all_movies