from fastapi import HTTPException, status

from logger import logger


class MovieNotFoundException(HTTPException):
    def __init__(self, detail: dict | None = None):
        logger.warning(f"Movie not found in the database: {str(detail)}")
        super().__init__(detail=detail, status_code=status.HTTP_404_NOT_FOUND)


class MovieAlreadyExistsException(HTTPException):
    def __init__(self, detail: dict | None = None):
        logger.warning(f"Movie already exists in the database: {str(detail)}")
        super().__init__(detail=detail, status_code=status.HTTP_409_CONFLICT)
