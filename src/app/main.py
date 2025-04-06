from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.initialization import populate_data
from exceptions.omdb_repository_exceptions import OmdbRepositoryException
from logger import logger
from repositories.database.session_factory import get_session
from routers.movie_router import router as movie_router
from routers.user_router import router as user_router


@asynccontextmanager
async def startup(app: FastAPI):
    """App startup logic"""
    logger.info("Starting the app.")
    async for session in get_session():
        await populate_data(session=session)
    yield


app = FastAPI(lifespan=startup)
app.include_router(movie_router)
app.include_router(user_router)


# Middlewares
@app.exception_handler(OmdbRepositoryException)
async def omdb_repository_exception_handler(request: Request, exc: OmdbRepositoryException):
    """
    Global handler for all OmdbRepositoryExceptions.
    """
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})
