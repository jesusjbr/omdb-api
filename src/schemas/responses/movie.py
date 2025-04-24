from schemas.responses.pagination_response import PaginationResponse
from schemas.shared.movie import MovieGet


class MoviesResponse(PaginationResponse):
    movies: list[MovieGet]


SingleMovieResponse = MovieGet
