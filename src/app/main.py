from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from starlette.responses import JSONResponse

from exceptions.omdb_repository_exceptions import OmdbRepositoryException
from logger import logger
from routers.movie import router


@asynccontextmanager
async def startup(app: FastAPI):
    """App startup logic"""
    logger.info("Starting the app...")
    yield

app = FastAPI(lifespan=startup)
app.include_router(router)


@app.exception_handler(OmdbRepositoryException)
async def omdb_repository_exception_handler(request: Request, exc: OmdbRepositoryException):
    """
    Global handler for all OmdbRepositoryExceptions.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )