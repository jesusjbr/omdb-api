from fastapi import HTTPException, status

from logger import logger


class OmdbRepositoryException(HTTPException):
    """Base exception class for OmdbRepository errors."""

    pass


class OmdbRepositoryUnauthorizedException(OmdbRepositoryException):
    def __init__(self, detail: dict | None = None):
        logger.warning(f"Invalid API key: {str(detail)}")
        super().__init__(detail=detail, status_code=status.HTTP_401_UNAUTHORIZED)


class OmdbRepositoryBadRequestException(OmdbRepositoryException):
    def __init__(self, detail: dict | None = None):
        logger.warning(f"Invalid or missing parameters: {str(detail)}")
        super().__init__(detail=detail, status_code=status.HTTP_400_BAD_REQUEST)


class OmdbRepositoryNotFoundException(OmdbRepositoryException):
    def __init__(self, detail: dict | None = None):
        logger.info(f"No results found for the search term or imdb_id: {str(detail)}")
        super().__init__(detail=detail, status_code=status.HTTP_404_NOT_FOUND)


class OmdbRepositoryInternalServerErrorException(OmdbRepositoryException):
    def __init__(self, detail: dict | None = None):
        logger.error(f"Unexpected repository error: {str(detail)}")
        super().__init__(detail=detail, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OmdbRepositoryInvalidResponseFormatException(OmdbRepositoryException):
    def __init__(self, detail: dict | None = None):
        logger.error(f"Invalid response format: {str(detail)}")
        super().__init__(detail=detail, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
