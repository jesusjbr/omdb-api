from fastapi import APIRouter
from fastapi.params import Query

from config import TAG_MOVIE
from services.movie import MovieService

router = APIRouter(prefix='/api/{version}/movies')

@router.get("", tags=[TAG_MOVIE])
async def get_movies(search_term: str = Query(...)):
    return await MovieService.get_movies(search_term=search_term)