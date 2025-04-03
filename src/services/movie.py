from repositories.external.omdb import OmdbRepository
from schemas.responses.omdb_by_search import Movie


class MovieService:
    """

    """
    @staticmethod
    async def get_movies(search_term: str) -> list[Movie]:
        """

        :param search_term:
        :return:
        """
        return await OmdbRepository.get_movies_by_search(search_term=search_term)