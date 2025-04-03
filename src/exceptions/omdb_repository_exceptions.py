from http import HTTPStatus

from fastapi import HTTPException

from logger import  logger


class OmdbRepositoryException(HTTPException):
    """Base exception class for OmdbRepository errors."""
    pass


class OmdbRepositoryUnauthorizedException(OmdbRepositoryException):
    def __init__(self, detail: dict | None = None):
        logger.warning(f"Invalid API key: {detail}")
        super().__init__(detail=detail, status_code=HTTPStatus.UNAUTHORIZED.value)


class OmdbRepositoryBadRequestException(OmdbRepositoryException):
    def __init__(self, detail: dict | None = None):
        logger.warning(f"Invalid or missing parameters: {detail}")
        super().__init__(detail=detail, status_code=HTTPStatus.BAD_REQUEST.value)


class OmdbRepositoryNotFoundException(OmdbRepositoryException):
    def __init__(self, detail: dict | None = None):
        logger.info(f"No results found for the search term: {detail}")
        super().__init__(detail=detail, status_code=HTTPStatus.NOT_FOUND.value)


class OmdbRepositoryInternalServerErrorException(OmdbRepositoryException):
    def __init__(self, detail: dict | None = None):
        logger.error(f"Unexpected repository error: {detail}")
        super().__init__(detail=detail, status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value)


class OmdbRepositoryInvalidResponseFormatException(OmdbRepositoryException):
    def __init__(self, detail: dict | None = None):
        logger.error(f"Invalid response format: {detail}")
        super().__init__(detail=detail, status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value)
