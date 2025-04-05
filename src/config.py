from os import environ

OMDB_API_KEY: str = environ.get("OMDB_API_KEY")
OMDB_API_URL: str = environ.get("OMDB_API_URL", default="https://www.omdbapi.com/")
DATABASE_ENDPOINT: str = environ.get("DATABASE_ENDPOINT")
DATABASE_USER: str = environ.get("DATABASE_USER")
DATABASE_PASSWORD: str = environ.get("DATABASE_PASSWORD")
DATABASE_PORT: str = environ.get("DATABASE_PORT")
DATABASE_NAME: str = environ.get("DATABASE_NAME")
POOL_SIZE: int = int(environ.get("POOL_SIZE", default=5))
POOL_MAX_OVERFLOW: int = int(environ.get("POOL_MAX_OVERFLOW", default=0))
DATABASE_URL: str = "postgresql+asyncpg://{}:{}@{}:{}/{}"

# Constants
TAG_MOVIE: str = "Movies"
TYPE_MOVIE: str = "movie"
MAX_TOTAL_RESULTS: int = 100
RESULTS_PER_PAGE: int = 10
MAX_TOTAL_PAGES: int = int(MAX_TOTAL_RESULTS / RESULTS_PER_PAGE)
MOVIES_SEARCH_TERM: str = "Avengers"
ORDER_BY_TITLE = "title"
ORDER_TYPE_ASC = "asc"
ORDER_BY_ID = "id"
